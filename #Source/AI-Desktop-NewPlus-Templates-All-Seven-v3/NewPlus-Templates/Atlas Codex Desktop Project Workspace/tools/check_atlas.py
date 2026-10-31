from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parent.parent
baseline = "AGENTS.md"
required = [baseline, "context/documentation.md", "tasks/onboarding.md", "HANDOFF.md"]
errors = ["Missing: " + name for name in required if not (root / name).is_file()]
output = root / "outputs/onboarding-guide.md"
if not output.is_file():
    errors.append("Missing: outputs/onboarding-guide.md")
else:
    text = output.read_text(encoding="utf-8")
    if len(re.findall(r"^# [^#].+", text, re.M)) != 1:
        errors.append("Expected exactly one H1 title")
    if re.findall(r"^(\d+)\. ", text, re.M) != ["1", "2", "3"]:
        errors.append("Expected exactly three ordered steps")
    if text.count("Expected result:") < 3:
        errors.append("Each step needs an expected result")
    if "../" + baseline not in text:
        errors.append("Missing relative link to the project baseline")
    if "## Verification checklist" not in text:
        errors.append("Missing final verification checklist")
if errors:
    print("FAIL\n" + "\n".join(errors))
    sys.exit(1)
print("PASS: required files and structural onboarding criteria are present.")
