import os
import yaml
import pandas as pd

# =====================================================
# Project Directories
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(BASE_DIR, "config", "test_config.yaml")
LOG_DIR = os.path.join(BASE_DIR, "logs")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# Create reports directory if it doesn't exist
os.makedirs(REPORT_DIR, exist_ok=True)

# =====================================================
# Read YAML Configuration
# =====================================================
with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)

tests = config["tests"]

summary = []

# =====================================================
# Analyze Log Files
# =====================================================
for test in tests:

    test_name = test["name"]
    log_file = os.path.join(LOG_DIR, test_name + ".log")

    if not os.path.exists(log_file):
        print(f"Log file not found: {log_file}")
        continue

    with open(log_file, "r") as file:
        log_data = file.read()

    # Count Messages
    info_count = log_data.count("UVM_INFO")
    warning_count = log_data.count("UVM_WARNING")
    error_count = log_data.count("UVM_ERROR")
    fatal_count = log_data.count("UVM_FATAL")

    # Determine Result
    result = "UNKNOWN"

    for line in log_data.splitlines():

        if "TEST_CASE RESULT: PASSED" in line:
            result = "PASSED"

        elif "TEST_CASE RESULT: FAILED" in line:
            result = "FAILED"

    # Store Summary
    summary.append(
        {
            "test": test_name,
            "errors": error_count,
            "warnings": warning_count,
            "fatals": fatal_count,
            "result": result,
        }
    )

# =====================================================
# Generate CSV Report
# =====================================================
df = pd.DataFrame(summary)

csv_file = os.path.join(REPORT_DIR, "summary.csv")
df.to_csv(csv_file, index=False)

# =====================================================
# Generate Excel Report
# =====================================================
excel_file = os.path.join(REPORT_DIR, "summary.xlsx")
df.to_excel(excel_file, index=False)

# =====================================================
# Generate YAML Report
# =====================================================
yaml_file = os.path.join(REPORT_DIR, "summary.yaml")

with open(yaml_file, "w") as file:
    yaml.dump(
        summary,
        file,
        default_flow_style=False,
        sort_keys=False,
    )

# =====================================================
# Overall PASS / FAIL Summary
# =====================================================
total_tests = len(summary)
passed_tests = 0
failed_tests = 0

for test in summary:

    if test["result"] == "PASSED":
        passed_tests += 1

    elif test["result"] == "FAILED":
        failed_tests += 1

# =====================================================
# Console Output
# =====================================================
print("\n========================================")
print("      LOG ANALYZER SUMMARY REPORT")
print("========================================")
print(f"Total Tests   : {total_tests}")
print(f"Passed Tests  : {passed_tests}")
print(f"Failed Tests  : {failed_tests}")
print("========================================")

print("\nGenerated Report Files")
print("----------------------------------------")
print(f"CSV   : {csv_file}")
print(f"Excel : {excel_file}")
print(f"YAML  : {yaml_file}")
print("----------------------------------------")
print("Report Generation Completed Successfully")
