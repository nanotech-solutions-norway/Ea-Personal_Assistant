# EA local Entra access-token validation (Windows)

Status: LOCAL_OPERATOR_TEST_PENDING. Never run interactive login from hosted CI.

## Prerequisites

- In Entra, EA-Personal-Assistant-API-Staging exposes an ENABLED delegated permission bring.tracking.read.
- EA-Personal-Assistant-Desktop-Test has that permission with admin consent.
- The Desktop-Test app has Mobile and desktop applications platform, redirect URI http://localhost, and is configured as a public client.
- Use the Windows development computer's interactive desktop and the correct Entra tenant.

## Local PowerShell commands

From an updated Ea-Personal_Assistant repository clone:

    git switch main
    git pull --ff-only
    py -m pip install --upgrade msal "PyJWT[crypto]>=2.10,<3"

Set these environment variables to the exact IDs from the two Entra application Overviews (do not commit real environment settings):

    $env:EA_ENTRA_TENANT_ID = "PASTE_DIRECTORY_TENANT_ID"
    $env:EA_API_CLIENT_ID = "PASTE_API_APPLICATION_CLIENT_ID"
    $env:EA_AUTHORIZED_CLIENT_ID = "PASTE_DESKTOP_APPLICATION_CLIENT_ID"

Run interactively:

    py verify_ea_entra.py

The script opens browser-based MSAL sign-in, requests the delegated scope for the EA API, and checks the returned JWT using the tenant-pinned signature/issuer/audience verifier.

Expected sanitized output:

    EA_ENTRA_VALIDATION=PASS
    ISSUER=VERIFIED
    AUDIENCE=VERIFIED
    SIGNATURE_AND_SCOPE=VERIFIED

If not accepted, report ONLY the marker: BLOCKED_INVALID_CONFIG, BLOCKED_MISSING_DEPENDENCIES, TOKEN_ISSUANCE_FAILED, or TOKEN_REJECTED. Do not send access tokens, user claims, screenshots containing raw tokens or secrets.

Optionally clear process variables after testing:

    Remove-Item Env:EA_ENTRA_TENANT_ID,Env:EA_API_CLIENT_ID,Env:EA_AUTHORIZED_CLIENT_ID -ErrorAction SilentlyContinue

## Trust boundaries

- API audience = EA API Application (client) ID GUID.
- Requested delegated scope = api://<EA_API_CLIENT_ID>/bring.tracking.read.
- The Desktop-Test app client ID identifies the calling public client, never the API audience.
- Source is intended to run locally; hosted GitHub Actions cannot complete a user's browser sign-in.
- No Bring provider request, persistent token cache, account mutation, production synchronization, deployment or paid Azure resource creation is included.
- Current EA Bring read policy remains PROHIBIT.

Historical note: The original PR #67 included non-secret Entra tenant and app identifiers. This amendment removes them from CURRENT source, not from immutable Git commit history. No access token or client secret appeared in the reviewed upload.
