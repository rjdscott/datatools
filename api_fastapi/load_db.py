import pandas as pd
import sqlite3 as sq


def get_data(input_path: str) -> pd.DataFrame:
    df = pd.read_parquet(input_path, engine='pyarrow')
    df.reset_index()
    return df


def write_data(df: pd.DataFrame, db_path: str, table_name: str) -> None:
    with sq.connect(db_path) as conn:
        df.to_sql(table_name, con=conn, if_exists='replace')
        df2 = pd.read_sql(f"select * from {table_name}", con=conn)
        df2.rename(columns={'index': 'id'}, inplace=True)
        df2.id += 1
        df2.to_sql(table_name, con=conn, if_exists='replace', index=False)


if __name__ == '__main__':
    input_data_path = '../data/all-tickers'
    db_path = 'sync/app.db'
    db_table_name = 'prices'
    write_data(get_data(input_path=input_data_path), db_path=db_path, table_name=db_table_name)
