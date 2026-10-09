from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
"active-source/04A_EA_PERSONAL_FINANCE_SENIOR_ADVISOR.md",
"knowledge/finance/PERSONAL_FINANCE_ADVISOR_PROTOCOL_CURRENT.md",
"knowledge/finance/PERSONAL_FINANCE_ADVISOR_CORE_INSTRUCTIONS.md",
"knowledge/finance/PERSONAL_FINANCE_ADVISOR_SPECIFICATION_CURRENT.md",
"knowledge/finance/EA_HOUSEHOLD_BUDGETING_PRIVATE_STATE_RULES_CURRENT.md",
"config/personal-finance/financial_state.schema.json",
"config/project/EA_PROJECT_INSTRUCTION_BLOCK.md",
"config/custom-gpt/EA_CUSTOM_GPT_INSTRUCTION_BLOCK.md",
"config/custom-gpt/EA_CUSTOM_GPT_KNOWLEDGE_FILE_LIST.md",
"registers/EA_PERSONAL_FINANCE_CAPABILITY_REGISTER_20261006.md",
"docs/decisions/EA_DECISION_PERSONAL_FINANCE_CAPABILITY_20261006.md"]
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append("missing "+rel)
manifest=json.loads((ROOT/"active-source/ea_optimized_source_manifest.json").read_text(encoding="utf-8"))
if "04A_EA_PERSONAL_FINANCE_SENIOR_ADVISOR.md" not in manifest.get("active_source_files",[]): errors.append("manifest missing 04A")
for rel in ["knowledge/finance/PERSONAL_FINANCE_ADVISOR_PROTOCOL_CURRENT.md","knowledge/finance/PERSONAL_FINANCE_ADVISOR_CORE_INSTRUCTIONS.md","knowledge/finance/PERSONAL_FINANCE_ADVISOR_SPECIFICATION_CURRENT.md","knowledge/finance/EA_HOUSEHOLD_BUDGETING_PRIVATE_STATE_RULES_CURRENT.md"]:
    if rel not in manifest.get("knowledge_files",[]): errors.append("manifest missing "+rel)
for rel in required:
    p=ROOT/rel
    if p.suffix in {".md",".json"} and p.exists() and "Privatøkonomi Seniorrådgiver" in p.read_text(encoding="utf-8"):
        errors.append("Norwegian system-role title in "+rel)
mod=(ROOT/"active-source/04A_EA_PERSONAL_FINANCE_SENIOR_ADVISOR.md").read_text(encoding="utf-8")
mod_lower=mod.lower()
for needle in ["r4","human-only","norwegian","english","financial_state.schema.json","EA_HOUSEHOLD_BUDGETING_PRIVATE_STATE_RULES_CURRENT.md"]:
    if needle.lower() not in mod_lower: errors.append("04A missing "+needle)
if errors:
    print("\n".join("FAIL: "+e for e in errors)); sys.exit(1)
print("PASS: Ea Personal Finance integration static validation")
