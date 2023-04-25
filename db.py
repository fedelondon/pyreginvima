import os
import sshtunnel
from dotenv import load_dotenv
import psycopg2 as pg

load_dotenv()


def connection_db(query):
    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0
    with sshtunnel.SSHTunnelForwarder(
            (os.getenv('SSH_HOST'),22),
            ssh_username=os.getenv('SSH_USER'),
            ssh_password=os.getenv('SSH_PKEY'),
            remote_bind_address=('0.0.0.0',5432)
    ) as tunnel:
        tunnel.start()

        conn = pg.connect(
            host=os.getenv('LOCALHOST'),
            port=tunnel.local_bind_port,
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
            database=os.getenv('PG_DATABASE_NAME')
        )

        db_cursor = conn.cursor()
        db_cursor.execute(query)
        return db_cursor.fetchall()

        #tunnel.stop()
