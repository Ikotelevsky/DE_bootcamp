import pandas as pd
import argparse
import os
from sqlalchemy import create_engine, types
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv'
    os.system(f'wget {url} -O {csv_name}')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    # Define data types for date columns
    dtype = {'lpep_pickup_datetime': types.DateTime(), 'lpep_dropoff_datetime': types.DateTime()}

    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', dtype=dtype)

    df.to_sql(name=table_name, con=engine, if_exists='append', dtype=dtype)

    while True:
        t_start = time()

        df = next(df_iter)

        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append', dtype=dtype)

        t_end = time()
        print(df.lpep_pickup_datetime.dtype)
        print('Inserted another chunk. It took %.3f seconds' % (t_end - t_start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres ')
    parser.add_argument('--user', help='User name for postgres')
    parser.add_argument('--password', help='Password for postgres')
    parser.add_argument('--host', help='Host for postgres')
    parser.add_argument('--port', help='Port for postgres')
    parser.add_argument('--db', help='Database name for postgres')
    parser.add_argument('--table_name', help='Table name for postgres')
    parser.add_argument('--url', help='URL for csv file')

    args = parser.parse_args()

    main(args)
