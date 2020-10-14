import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    This function load the staging tables from the S3 buckets using the COPY function created in "sql_queries.py".

    INPUTS:
    * cur: the cursor variable
    * conn: the connection to the Redshift cluster.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    This function process and inserts the data from the staging tables to the fact and dimensional tables using the queries in "sql_queries.py".

    INPUTS:
    * cur: the cursor variable
    * conn: the connection to the Redshift cluster.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()