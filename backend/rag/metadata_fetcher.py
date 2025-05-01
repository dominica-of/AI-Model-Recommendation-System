import psycopg2
import pandas as pd

class MetadataFetcher:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def fetch_models(self, model_ids):
        if not model_ids:
            return []

        query = "SELECT * FROM models WHERE model = ANY(%s)"
        cur = self.conn.cursor()
        cur.execute(query, (model_ids,))  # pass as tuple containing list
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        cur.close()

        return [dict(zip(colnames, row)) for row in rows]

    def get_unique_actions(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT DISTINCT action FROM models WHERE action IS NOT NULL")
            return [row[0] for row in cur.fetchall()]

    def get_unique_tasks(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT DISTINCT model_task FROM models WHERE model_task IS NOT NULL")
            return [row[0] for row in cur.fetchall()]

    def get_unique_input_data(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT DISTINCT input_data FROM models WHERE input_data IS NOT NULL")
            return [row[0] for row in cur.fetchall()]

    def close(self):
        self.conn.close()
    