#!/usr/bin/env python3
"""Read Azure PostgreSQL West Europe quota through Reader OIDC; redact details.

Microsoft PostgreSQL Quota Usages List API version 2025-08-01.
This never interprets positive quota as regional placement capacity and
NEVER authorizes paid resource creation.
"""
import json
import os
import re
import subprocess
import sys

UUID=re.compile(r"^[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$")

def classify(payload):
    if not isinstance(payload,dict) or not isinstance(payload.get("value"),list):
        return {"quota_api":"INCONCLUSIVE","burst_family_headroom":"UNKNOWN","total_core_headroom":"UNKNOWN","capacity_guaranteed":False}
    names={}
    for record in payload["value"]:
        if not isinstance(record,dict): continue
        name=record.get("name") or {}
        if isinstance(name,dict):
            name=name.get("value","")
        if name not in ("standardBSFamily","cores"): continue
        cap=record.get("limit")
        used=record.get("currentValue")
        if (isinstance(cap,int) and not isinstance(cap,bool) and
            isinstance(used,int) and not isinstance(used,bool) and cap>=0 and used>=0 and used<=cap):
            names[name]="POSITIVE" if cap>used else "ZERO"
        else: names[name]="UNKNOWN"
    return {"quota_api":"READ_OK",
            "burst_family_headroom":names.get("standardBSFamily","UNKNOWN"),
            "total_core_headroom":names.get("cores","UNKNOWN"),
            "capacity_guaranteed":False}

def run():
    sub=os.environ.get("AZURE_SUBSCRIPTION_ID","")
    if not UUID.fullmatch(sub):
        raise SystemExit("Invalid Azure subscription identifier configuration")
    url=(f"https://management.azure.com/subscriptions/{sub}/providers/"
         "Microsoft.DBforPostgreSQL/locations/westeurope/"
         "resourceType/flexibleServers/usages?api-version=2025-08-01")
    try:
        result=subprocess.run(["az","rest","--method","get","--url",url,
                               "--only-show-errors","--output","json"],
                              capture_output=True,text=True,timeout=80,check=False)
        if result.returncode:
            finding={"quota_api":"UNAVAILABLE_OR_UNAUTHORIZED","burst_family_headroom":"UNKNOWN","total_core_headroom":"UNKNOWN","capacity_guaranteed":False}
        else:
            finding=classify(json.loads(result.stdout))
    except (OSError,subprocess.TimeoutExpired,ValueError,TypeError):
        finding={"quota_api":"INCONCLUSIVE","burst_family_headroom":"UNKNOWN","total_core_headroom":"UNKNOWN","capacity_guaranteed":False}
    print("EA Azure West Europe B-series read-only quota check (redacted):")
    for k,v in finding.items(): print(f"  {k}: {v}")
    print("  exact_B1ms_SKU_realtime_allocation: NOT_VERIFIED")
    print("  deployer_RBAC: NOT_VERIFIED")
    print("  deployment_authorized: False")
    output=os.environ.get("GITHUB_STEP_SUMMARY")
    if output:
        with open(output,"a",encoding="utf8") as out:
            out.write("### West Europe PostgreSQL quota (read-only)\n")
            for k,v in finding.items(): out.write(f"- {k}: {v}\n")
            out.write("- B1ms live placement capacity: NOT VERIFIED; cloud deployer RBAC: NOT VERIFIED\n")
            out.write("- No Azure resource creation; €20 all-in cost gate remains BLOCKED.\n")
    # Even a denial is an inconclusive discovery result, not an authorization shortcut.
    return 0

if __name__=="__main__":
    sys.exit(run())
