import pandas as pd
from db import get_connection


def get_startup_ranking(limit=10):
    conn = get_connection()

    query = """
        SELECT
            startup_name,
            setor,
            tech_score
        FROM tech_score
        ORDER BY tech_score DESC
        LIMIT ?
    """

    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()

    return df


if __name__ == "__main__":
    df = get_startup_ranking(5)
    print(df)

def get_startups_by_sector(sector=None):
    conn = get_connection()

    if sector and sector != "Todos":
        query = """
            SELECT startup_name, setor, tech_score
            FROM tech_score
            WHERE setor = ?
            ORDER BY tech_score DESC
        """
        df = pd.read_sql_query(query, conn, params=(sector,))
    else:
        query = """
            SELECT startup_name, setor, tech_score
            FROM tech_score
            ORDER BY tech_score DESC
        """
        df = pd.read_sql_query(query, conn)

    conn.close()
    return df

def get_scores_by_sector():
    conn = get_connection()

    query = """
        SELECT setor, tech_score
        FROM tech_score
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df

def get_startup_radar(startup_name):
    conn = get_connection()

    query = """
        SELECT
            performance, viabilidade, confiabilidade,
            usabilidade, energia, fisico,
            conectividade, ciclo_vida
        FROM tech_score
        WHERE startup_name = ?
    """

    df = pd.read_sql_query(query, conn, params=(startup_name,))
    conn.close()

    return df
