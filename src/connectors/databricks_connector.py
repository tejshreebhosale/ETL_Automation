from databricks import sql
import pandas as pd


def read_databricks(query, config):
    conn = sql.connect(
        server_hostname=config["server_hostname"],
        http_path=config["http_path"],
        access_token=config["access_token"]
    )

    cursor = conn.cursor()
    cursor.execute(query)

    df = pd.DataFrame(
        cursor.fetchall(),
        columns=[col[0] for col in cursor.description]
    )

    conn.close()

    return df