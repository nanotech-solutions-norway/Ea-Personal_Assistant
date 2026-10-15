#!/usr/bin/env python3
"""Read-only EUR retail rate discovery for EA West Europe staging.

Never treats retail rates as contract-specific quotes, resource capacity,
Azure budget enforcement, or authorization to provision.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

API = "https://prices.azure.com/api/retail/prices"
SERVICES = [
    "Azure Database for PostgreSQL",
    "Azure Container Apps",
    "Azure DNS",
    "Azure Private Link",
    "Key Vault",
    "Log Analytics",
    "Container Registry",
]

def get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "EA-pricing-readonly/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=50) as resp:
                return json.load(resp)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 2)

def meters(service):
    expr = f"armRegionName eq 'westeurope' and serviceName eq '{service}' and priceType eq 'Consumption'"
    params = urllib.parse.urlencode({"currencyCode": "EUR", "$filter": expr})
    url = API + "?" + params
    out = []
    for _ in range(12):
        response = get_json(url)
        out.extend(response.get("Items", []))
        url = response.get("NextPageLink")
        if not url:
            return out
    raise RuntimeError("Unexpected pagination depth; incomplete retail price collection")

def slim(v):
    return {k: v.get(k) for k in ("armSkuName", "skuName", "meterName", "productName", "retailPrice", "unitOfMeasure", "effectiveStartDate", "meterId")}

def relevant(service, v):
    s = " ".join(str(v.get(k, "")) for k in ("armSkuName", "skuName", "meterName", "productName")).lower()
    if service == SERVICES[0]:
        return ("b1ms" in s or "flex server storage" in s or "storage data stored" in s or "backup" in s)
    if service == "Azure Container Apps":
        return any(q in s for q in ["vCPU", "vcpu", "memory", "request", "management", "private"])
    if service == "Azure DNS":
        return "private" in s
    if service == "Azure Private Link":
        return "endpoint" in s or "private link" in s or "processed" in s
    if service == "Key Vault":
        return "operation" in s or "transaction" in s
    if service == "Log Analytics":
        return "data ingestion" in s or "pay-as-you-go" in s
    if service == "Container Registry":
        return "basic" in s
    return False

def main():
    report = {}
    for service in SERVICES:
        items = meters(service)
        selected = [slim(i) for i in items if relevant(service, i)]
        report[service] = selected
        print(f"## {service}: {len(items)} total, {len(selected)} matched", flush=True)
        for i in selected[:65]:
            print("RETAIL_METER " + json.dumps({"service":service, **i}, sort_keys=True), flush=True)
    with open("ea_azure_retail_eur_westeurope.json","w",encoding="utf-8") as f:
        json.dump({"currency":"EUR","region":"westeurope","source":API,"meters":report,"note":"Retail reference rates, not subscription-specific quotes, taxes, quotas or Azure spend limits."},f,indent=2)
    pg = report.get(SERVICES[0], [])
    b1 = [i for i in pg if str(i.get("armSkuName","")).lower() in ("b1ms","standard_b1ms") and "1 Hour" in str(i.get("unitOfMeasure",""))]
    storage = [i for i in pg if str(i.get("meterName","")).lower() == "storage data stored" and "flex server storage" in str(i.get("productName","")).lower()]
    print("B1MS_CANDIDATES "+json.dumps(b1),flush=True)
    print("STORAGE_CANDIDATES "+json.dumps(storage),flush=True)
    if len(b1)==1 and len(storage)==1:
        b,h=b1[0]["retailPrice"],storage[0]["retailPrice"]
        print(f"PG_B1MS_COMPUTE_730H_EUR={b*730:.3f}",flush=True)
        print(f"PG_32GIB_STORAGE_EUR={h*32:.3f}",flush=True)
        print(f"PG_B1MS_32GIB_BASE_730H_EUR={b*730+h*32:.3f}",flush=True)
        print(f"PG_B1MS_32GIB_BASE_120H_EUR={b*120+h*32:.3f}",flush=True)
        registry=[i for i in report.get("Container Registry",[]) if i.get("meterName")=="Basic Registry Unit" and i.get("unitOfMeasure")=="1/Day"]
        private=[i for i in report.get("Azure Container Apps",[]) if i.get("meterName")=="Environment Private Endpoint" and i.get("unitOfMeasure")=="1 Hour"]
        if len(registry)==1:
            cost=registry[0]["retailPrice"]*(730/24)
            print(f"ACR_BASIC_730H_EUR={cost:.3f}",flush=True)
            print(f"PG_B1MS_PLUS_ACR_730H_EUR={b*730+h*32+cost:.3f}",flush=True)
        if len(private)==1:
            rate=private[0]["retailPrice"]
            print(f"ACA_ENV_PRIVATE_ENDPOINT_730H_EUR={rate*730:.3f}",flush=True)
            print(f"PG_B1MS_PLUS_ACA_ENDPOINT_730H_EUR={b*730+h*32+rate*730:.3f}",flush=True)
    else:
        print("PRICE_TOTAL_NOT_COMPUTED: ambiguous/missing metering; inspect candidates",flush=True)
    print("NOTE: private network, Container Apps, logs, backup, DNS, registry, tax and quota require explicit separate verification.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"PRICE_API_ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
