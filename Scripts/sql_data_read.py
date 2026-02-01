import sqlite3
import pandas as pd

conn=sqlite3.connect("crypto_prices.db")
df=pd.read_sql("select * from crypto_prices_table",conn)
print(df)
