"""Offline EA staging configuration review; NEVER executes Azure operations.

This validator is deliberately NOT a deployment authorizer. Every run returns
deployment_authorized=False, even if a JSON file claims approval: actual Azure
RBAC, account owner, itemized retail quote and explicit out-of-band operator
authorization require independent verification by an authorized deployment
controller. Safe to run on public-repository synthetic configuration.
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_DECISION = ROOT / "deployment" / "EA_STAGING_DECISION_WE_EUR20_20261013.json"

class StagingDecisionError(ValueError):
    """Unsafe or malformed EA staging proposal."""


def review_decision(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise StagingDecisionError("Decision must be a JSON object")
    budget = data.get("budget", {})
    region = data.get("region", {})
    tenant = data.get("tenant", {})
    group = data.get("resource_group", {})
    safety = data.get("safety", {})
    auth = data.get("auth", {})
    gates = data.get("predeploy_gates", {})

    if data.get("cloud_provider") != "azure":
        raise StagingDecisionError("Only the approved Azure design is allowed")
    if region.get("azure_location") != "westeurope":
        raise StagingDecisionError("Location must remain West Europe")
    if budget.get("currency") != "EUR" or budget.get("monthly_ceiling") != 20:
        raise StagingDecisionError("Budget constraint must remain EUR 20/month")
    if not group.get("dedicated") or not group.get("name"):
        raise StagingDecisionError("A dedicated EA resource group must be planned")
    if tenant.get("mode") != "single_private_ea_tenant":
        raise StagingDecisionError("Only one private EA tenant is authorized")
    if tenant.get("family_atlasorbit_reuse_allowed") is not False:
        raise StagingDecisionError("Do not reuse AtlasOrbit/family resources")
    if tenant.get("data_scope") != "synthetic_only_until_separate_authorization":
        raise StagingDecisionError("Only synthetic data is allowed at this stage")
    if budget.get("azure_budget_is_hard_stop") is not False:
        raise StagingDecisionError("Azure budgets do not hard-stop charging")
    if any(safety.get(key) is not False for key in (
        "paid_resource_creation_enabled", "live_provider_sync_enabled",
        "level_2b_enabled", "level_2c_enabled",
        "external_email_send_enabled", "external_calendar_write_enabled",
        "customer_data_export_enabled",
    )):
        raise StagingDecisionError("A safety hold was altered without approval")

    blockers = []
    # Public source must not contain cloud account identifiers; a protected
    # GitHub environment variable is the approved storage boundary.
    subref = data.get("subscription_reference", {})
    if not data.get("subscription_id") and not subref.get("operator_provided"):
        blockers.append("Azure subscription unavailable")
    elif subref.get("cloud_identity_and_rbac_verified") is not True:
        blockers.append("Azure subscription ownership/RBAC unverified")
    if subref.get("actual_subscription_id_committed") is True:
        raise StagingDecisionError("Never commit the subscription ID to the public repository")
    if region.get("service_sku_availability_verified") is not True:
        blockers.append("West Europe SKUs unverified for subscription")
    if budget.get("estimate_verified") is not True:
        blockers.append("Subscription-specific itemized all-in price unverified")
    cost = budget.get("subscription_specific_all_in_estimate_eur")
    if isinstance(cost, bool) or not isinstance(cost, (int, float)) or cost < 0:
        blockers.append("Valid numeric EUR/month quote missing")
    elif cost > budget["monthly_ceiling"]:
        blockers.append("Estimated Azure spend exceeds EUR 20/month")
    for k, label in (
        ("cloud_resource_management_grant_verified", "Cloud RBAC not independently verified"),
        ("operator_deployment_approval", "Explicit deployment authorization missing"),
        ("google_backend_oauth_verified", "Independent Google backend OAuth not granted"),
        ("github_app_installation_verified", "GitHub App installation not verified"),
    ):
        if auth.get(k) is not True:
            blockers.append(label)
    for k, label in (
        ("azure_subscription_selected", "Subscription selection not completed"),
        ("resource_group_creation_authorized", "Resource group not authorized"),
        ("all_in_cost_quote_verified", "Full cost quote not accepted"),
        ("quote_within_budget", "EUR 20 quote check not accepted"),
        ("private_database_design_verified", "Private database design not verified"),
        ("legacy_tables_isolated_or_single_tenant", "Legacy tenant isolation unresolved"),
        ("restricted_postgres_role_verified", "Restricted database role not proven"),
        ("provider_oauth_scope_approved", "Provider OAuth scopes not approved"),
        ("explicit_deployment_approval", "Deployment approval gate not passed"),
    ):
        if gates.get(k) is not True:
            blockers.append(label)
    return {
        "design_valid": True,
        "deployment_authorized": False,
        "requires_external_authorization_and_cloud_cost_quote": True,
        "blockers": blockers,
        "status": "DESIGN_VALID_DEPLOYMENT_BLOCKED",
    }


def main() -> int:
    data = json.loads(DEFAULT_DECISION.read_text(encoding="utf-8"))
    result = review_decision(data)
    print(json.dumps(result, indent=2, sort_keys=True))
    # Exit code 2 deliberately signals that deployment cannot proceed.
    return 2


if __name__ == "__main__":
    sys.exit(main())
