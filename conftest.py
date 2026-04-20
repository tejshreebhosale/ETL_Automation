import sys
from pathlib import Path

# Add the project root to Python path so pytest can find the src module
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def pytest_html_report_title(report):
    report.title = "ELT Data Validation Report"