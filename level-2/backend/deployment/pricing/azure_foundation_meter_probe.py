#!/usr/bin/env python3
"""Unauthenticated Azure EUR meter discovery for the *mandatory* ACA VNet infrastructure.

Only catalogue rates. This does not deploy Azure resources or accept quotations.
Filters retain meter region/tier, because Azure price tiers and units matter.
"""
from __future__ import annotations
import datetime
import json
import time
import urllib.parse
import urllib.request

URL = "https://prices.azure.com/api/retail/prices"
QUERIES = {
  "IP Addresses": ("ip address", "ipv4", "static"),
  "Load Balancer": ("standard", "rule", "data processed"),
  "Virtual Network": ("standard private endpoint", "data processed", "peering"),
  "Azure Container Apps": ("environment management hour", "environment private endpoint", "standard memory", "standard vcpu", "standard requests"),
  "Azure DNS": ("private zone", "private queries"),
}
FIELDS = ("serviceName","productName","skuName","meterName","retailPrice",
          "unitOfMeasure","tierMinimumUnits","armRegionName","effectiveStartDate",
          "meterId","skuId","isPrimaryMeterRegion")
def get(url):
    for n in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(
                url,headers={"Accept":"application/json","User-Agent":"EA-Staging-Retail-Recon/1.0"}),timeout=60) as rsp:
                return json.load(rsp)
        except Exception:
            if n==2: raise
            time.sleep(n+2)
def collect(service):
    q=urllib.parse.urlencode({"currencyCode":"EUR","$filter":f"serviceName eq '{service}' and priceType eq 'Consumption'"})
    url=URL+"?"+q
    rows=[]
    for _ in range(25):
        page=get(url)
        rows+=page.get("Items",[])
        url=page.get("NextPageLink")
        if not url:
            return rows,True
    return rows,False
def include(service,row):
    if str(row.get("armRegionName","")).lower() not in ("westeurope","global",""): return False
    text=" ".join(str(row.get(k) or "") for k in ("productName","skuName","meterName")).lower()
    return any(s in text for s in QUERIES[service])
def main():
    report={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "source":URL,"currency":"EUR","region":"westeurope","cost_authorized":False,
      "warning":"Public retail catalogue candidate rates, no discounts/taxes/tier choice/actual Azure account charges.",
      "services":{}}
    for service in QUERIES:
        try:
            all_rows,complete=collect(service)
            rows=[{k:r.get(k) for k in FIELDS} for r in all_rows if include(service,r)]
            report["services"][service]={"query_ok":True,"pagination_complete":complete,
                                         "matched":rows,"total_catalog_rows":len(all_rows)}
            print(f"SERVICE {service} MATCHES={len(rows)} TOTAL={len(all_rows)} COMPLETE={complete}",flush=True)
            for row in rows[:35]:
                print("EVIDENCE "+json.dumps(row,sort_keys=True),flush=True)
            if len(rows)>35: print("EVIDENCE_EXTRA_IN_ARTIFACT",flush=True)
        except Exception as exc:
            report["services"][service]={"query_ok":False,"error_type":type(exc).__name__,"matched":[]}
            print(f"SERVICE {service} INCONCLUSIVE: {type(exc).__name__}",flush=True)
    with open("ea_azure_foundation_eur_catalog_20261015.json","w",encoding="utf8") as f:
        json.dump(report,f,indent=2)
    print("ALL_IN_QUOTE_VERIFIED=False")
    print("DEPLOYMENT_AUTHORIZED=False")
    print("MANDATORY_ACA_VNET_MANAGED_IP_LOAD_BALANCER_USAGE_NOT_YET_SCOPED")
if __name__=="__main__":
    main()
