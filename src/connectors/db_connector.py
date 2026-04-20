import oracledb
import pandas as pd


def read_oracle(query, config):
    conn = oracledb.connect(
        user=config["user"],
        password=config["password"],
        dsn=config["dsn"]
    )

    df = pd.read_sql(query, conn)

    conn.close()

    return df