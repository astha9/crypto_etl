import requests 
import pandas as pd
import sqlite3

try:
    response=requests.get("https://api.coingecko.com/api/v3/coins/list",timeout=10)
    data=response.json()
    data_coin_list=[]
    #Get coins list 
    for coin in data:
        if coin["id"] in ["bitcoin" ,"ethereum", "dogecoin"]:
            data_coin_list.append(coin["id"])

    all_data=[]
    #Get prices and timestamp for data_coin_list for 30 days
    for coin in data_coin_list:
        response=requests.get(f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=30"
                            ,timeout=10).json()
        if 'prices' not in response:
            continue
        df=pd.DataFrame(response['prices'],columns=['timestamp','prices'])
        df['coin']=coin
        all_data.append(df)

    final_df=pd.concat(all_data,ignore_index=False)[['coin','prices','timestamp']]
    final_df.to_csv(f"./output_files/crypto_coin.csv",index=False)
    print("File written to /output_files")

    #Connection to sqllite 
    conn=sqlite3.connect("crypto_prices.db")
    #Save to SQLite db
    final_df.to_sql("crypto_prices_table",conn,if_exists='replace',index=False)
    conn.close()
except Exception as e:
    print("Error :",str(e))   


        