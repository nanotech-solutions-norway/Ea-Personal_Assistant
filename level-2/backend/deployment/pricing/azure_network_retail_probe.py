#!/usr/bin/env python3
"""Discover public EUR Azure networking and support meters for EA 48h staging.

READ ONLY: Microsoft's public retail API; no Azure subscription credentials,
resource writes or deployment approval. Missing/unmatched costs stay UNKNOWN.
"""
from __future__ import annotations

import datetime
import json
import time
import urllib.parse
import urllib.request

BASE="https://prices.azure.com/api/retail/prices"
SERVICES=(
    "Virtual Network", "Azure DNS", "Azure Private Link", "NAT Gateway",
    "Bandwidth", "Container Apps", "Container Registry", "Key Vault",
    "Log Analytics", "Azure Database for PostgreSQL",
)
TERMS={
    "Virtual Network": ("gateway","peering","nat","private"),
    "Azure DNS": ("private","zone","query"),
    "Azure Private Link": ("endpoint","link","data processed"),
    "NAT Gateway": ("nat","gateway","data processed"),
    "Bandwidth": ("inter region","outbound","data transfer","internet"),
    "Container Apps": ("environment","vcpu","memory","request"),
    "Container Registry": ("basic registry unit","data stored"),
    "Key Vault": ("operations","transaction"),
    "Log Analytics": ("data ingestion","analytics logs"),
    "Azure Database for PostgreSQL": ("b1ms","storage data stored","backup storage"),
}
FIELDS=("serviceName","productName","skuName","meterName","armRegionName","retailPrice","unitOfMeasure","effectiveStartDate","meterId")

def read_json(url):
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"ea-azure-retail-analysis/1.0","Accept":"application/json"})
            with urllib.request.urlopen(req,timeout=45) as rsp:
                return json.load(rsp)
        except Exception:
            if attempt==2: raise
            time.sleep(2*(attempt+1))

def retrieve(service, max_pages=25):
    q=urllib.parse.urlencode({"currencyCode":"EUR","$filter":f"serviceName eq '{service}' and priceType eq 'Consumption'"})
    next_url=BASE+"?"+q
    rows=[]
    for _ in range(max_pages):
        page=read_json(next_url)
        rows.extend(page.get("Items",[]))
        next_url=page.get("NextPageLink")
        if not next_url:
            return rows, True
    return rows, False

def candidate(service,row):
    if str(row.get("armRegionName","")).lower() not in ("westeurope","","global"): return False
    text=" ".join(str(row.get(k,"")) for k in ("productName","skuName","meterName")).lower()
    return any(term in text for term in TERMS[service])

def safe_row(row):
    return {key:row.get(key) for key in FIELDS}

def main():
    data={"as_of_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "currency":"EUR","region":"westeurope","source":BASE,
          "warning":"Public retail meters, NOT an itemized topology quote, negotiated Azure bill, quota, or deployment authorization.",
          "services":{}}
    for service in SERVICES:
        try:
            items,complete=retrieve(service)
            matches=[safe_row(row) for row in items if candidate(service,row)]
            # Keep full matched evidence in artifact; only bounded output to public CI logs.
            data["services"][service]={"query_ok":True,"complete":complete,
                "returned_count":len(items),"candidate_count":len(matches),"candidate_meters":matches}
            print(f"SERVICE {service}: returned={len(items)} candidates={len(matches)} complete={complete}",flush=True)
            for row in matches[:22]:
                print("METER "+json.dumps(row,sort_keys=True),flush=True)
            if len(matches)>22: print("METER_OUTPUT_TRUNCATED: full candidates in artifact",flush=True)
        except Exception as exc:
            data["services"][service]={"query_ok":False,"complete":False,
                "candidate_count":0,"error_type":type(exc).__name__}
            print(f"SERVICE {service}: UNKNOWN ({type(exc).__name__})",flush=True)
    # Output contains exclusively public Azure catalog meters, no billing credentials.
    with open("ea_azure_network_retail_eur_westeurope.json","w",encoding="utf8") as f:
        json.dump(data,f,indent=2)
    print("DEPLOYMENT_AUTHORIZED: false")
    print("NETWORK_ALL_IN_QUOTE_VERIFIED: false")
    print("Any missing service category must remain unpriced, never zero.")
if __name__=="__main__":
    main()
