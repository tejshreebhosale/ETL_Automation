import os
import pandas as pd
import matplotlib.pyplot as plt


def generate_dashboard(summary):
    os.makedirs("reports", exist_ok=True)

    df = pd.DataFrame(summary)

    # 🔹 Create chart (no color specified as per best practice)
    plt.figure()
    df["status"].value_counts().plot(kind="bar")
    plt.title("Test Status Summary")
    plt.xlabel("Status")
    plt.ylabel("Count")

    chart_path = "reports/status_chart.png"
    plt.savefig(chart_path)
    plt.close()

    # 🔹 Generate HTML
    html_content = f"""
    <html>
    <head>
        <title>ELT Validation Dashboard</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            h1 {{ color: #333; }}
            table {{
                border-collapse: collapse;
                width: 80%;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>

    <h1>ELT Validation Summary</h1>

    <table>
        <tr>
            <th>Table</th>
            <th>Passed</th>
            <th>Failed</th>
            <th>Status</th>
        </tr>
    """

    for row in summary:
        html_content += f"""
        <tr>
            <td>{row['table']}</td>
            <td>{row['passed']}</td>
            <td>{row['failed']}</td>
            <td>{row['status']}</td>
        </tr>
        """

    html_content += f"""
    </table>

    <h2>Status Chart</h2>
    <img src="status_chart.png" width="500">

    </body>
    </html>
    """

    html_path = "reports/dashboard.html"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_path