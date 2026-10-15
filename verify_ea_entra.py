from pathlib import Path
import sys
import msal

sys.path.insert(
    0, str(Path("level-2/backend/src").resolve())
)

from ea_backend.entra_access_token import EntraAccessTokenVerifier

# Replace these placeholders with Entra Overview values.
TENANT_ID = "b45a5a5d-82ab-4ca4-95e2-5e3fa57320b5"
API_CLIENT_ID = "5a1d0761-8ebb-46c6-849f-43b48be6c535"
DESKTOP_CLIENT_ID = "f8361933-4d09-422c-818b-817255c58b41"

app = msal.PublicClientApplication(
    client_id=DESKTOP_CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
)

scope = f"api://{API_CLIENT_ID}/bring.tracking.read"

result = app.acquire_token_interactive(scopes=[scope])

if "access_token" not in result:
    raise SystemExit(
        "EA_ENTRA_VALIDATION=TOKEN_ISSUANCE_FAILED"
    )

verifier = EntraAccessTokenVerifier(
    tenant_id=TENANT_ID,
    api_audience=API_CLIENT_ID,
    authorized_client_ids=(DESKTOP_CLIENT_ID,),
)

try:
    verified = verifier.verify(
        result["access_token"],
        expected_audience=API_CLIENT_ID,
    )
except Exception:
    raise SystemExit(
        "EA_ENTRA_VALIDATION=TOKEN_REJECTED"
    ) from None

print("EA_ENTRA_VALIDATION=PASS")
print("ISSUER=VERIFIED")
print("AUDIENCE=VERIFIED")
print("SIGNATURE_AND_SCOPE=VERIFIED")
