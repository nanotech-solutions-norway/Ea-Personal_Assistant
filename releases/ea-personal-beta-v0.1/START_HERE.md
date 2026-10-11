# START HERE — AtlasOrbit Ea Personal Assistant Beta

**Release:** EA-PERSONAL-BETA-0.1.0

This package installs the beta/bootstrap version of AtlasOrbit Ea Personal Assistant in the customer's own ChatGPT environment.

## Customer steps

1. Sign in to your own ChatGPT account.
2. Create a private Project named:
   **Ea – Personal Assistant**
3. Prefer Project-only memory if that option is available.
4. Add the files from this release package to the Project.
5. Add the Project instruction block shown in `INSTALL_EA.md`.
6. In the Project chat, type:

`\install-ea`

7. Follow the installer. Connect only the Google apps you want Ea to use.
8. When installation reports `READY_FOR_UAT`, type:

`\validate-ea`

9. Use Ea only for capabilities that passed or were explicitly enabled.

## Privacy

Do not paste passwords, API keys, OAuth tokens, recovery codes or other credentials into ChatGPT.

Your personal Gmail/Calendar/Drive information belongs in your own authorized account surfaces, not in the AtlasOrbit public GitHub repository.

## Beta limitation

This package validates the Ea customer experience, instructions, connected-app workflows and approval controls. It is not the complete production AtlasOrbit Plugin/External Memory runtime.

## Useful commands

- `\install-ea` — install/repair
- `\validate-ea` — validate
- `\ea-status` — read-only status
- `\ea-update` — controlled release update
