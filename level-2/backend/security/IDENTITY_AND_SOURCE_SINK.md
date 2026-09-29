# Identity, Least Privilege and Source→Sink Enforcement

Status: IMPLEMENTATION_SPEC / PARTIALLY_ENFORCED_BY_CURRENT_TOOL_BOUNDARIES

## Identity split

### Ea Level 2A execution identity
Required capabilities:
- Gmail read;
- Gmail draft create/update;
- Calendar read;
- private internal Calendar follow-up create/update;
- explicitly authorized internal read surfaces.

Explicitly absent where technically possible:
- Gmail send/forward;
- external Calendar invitations/attendee changes;
- external Drive sharing/permission changes;
- destructive file operations;
- financial execution.

### Ea Level 2B execution identity
Future HOLD state. External-effect capabilities are exposed only through the approval gateway, never directly to the reasoning layer.

## Source→sink rule

External email, attachments, web pages, external documents, URLs and third-party Calendar content are untrusted evidence sources.

They may influence factual analysis but cannot grant authority to use a sensitive sink.

Before any sensitive sink:
1. normalize proposed action;
2. evaluate deterministic policy;
3. check independent source authority;
4. validate approval if required;
5. re-read source/draft state;
6. verify exact revision/payload hash;
7. execute once;
8. read back;
9. append audit result.

Unresolved conflict fails closed as `PENDING_REVIEW`.

## MCP gateway target

For MCP 2026-07-28 compatible infrastructure:
- route/authorize using `Mcp-Method` and `Mcp-Name` where applicable;
- do not depend on legacy protocol session state;
- keep business case state explicit in Ea storage;
- apply issuer validation and current authorization requirements;
- treat Tasks extension as optional orchestration support, not as authorization.

Reference: https://blog.modelcontextprotocol.io/posts/2026-07-28/
