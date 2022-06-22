import requests
import pandas as pd
import streamlit as st

def get_traits(key='lilnoun'):
    if key == 'noun':
        url = 'https://node-api.flipsidecrypto.com/api/v2/queries/4cb81caa-4088-40e0-933d-d8a057603d0b/data/latest'
    else:
        url = 'https://node-api.flipsidecrypto.com/api/v2/queries/75655225-bbdc-4c76-98f5-48e0e94bac82/data/latest'
    r = requests.get(url)
    if r.status_code==200:
        df = pd.DataFrame(r.json())
    else:
        r = requests.get(url)
        assert r.status_code==200
        df = pd.DataFrame(r.json())
    df['MINT_TIME'] = pd.to_datetime(df['MINT_TIME'])
    df['TOKENID'] = df['TOKENID'].astype('int')
    traits_table = pd.read_csv('traits.csv',sep='\t',index_col=0)
    traits_table['description'] = traits_table['description'].str.split('-',n=1).str[1]
    traits = [i.upper() for i in traits_table['trait'].unique()]

    for col in traits:
        col_lower = col.lower()
        df[col] = df[col].map(traits_table.query('trait==@col_lower')['description'])

    return df.sort_values(by='MINT_TIME',ascending=False)

def get_transfers(key='lilnoun'):
    if key == 'noun':
        url = 'https://node-api.flipsidecrypto.com/api/v2/queries/94811dd6-4a66-4bb6-9e86-49feae817816/data/latest'
    else:
        url = ''
    r = requests.get(url)
    if r.status_code==200:
        df = pd.DataFrame(r.json())
    else:
        r = requests.get(url)
        assert r.status_code==200
        df = pd.DataFrame(r.json())
    df['BLOCK_TIMESTAMP'] = pd.to_datetime(df['BLOCK_TIMESTAMP'])
    df['TOKENID'] = df['TOKENID'].astype('int')
    return df.sort_values(by='BLOCK_TIMESTAMP',ascending=False)

def get_sales(key='lilnoun'):
    if key == 'noun':
        url='https://node-api.flipsidecrypto.com/api/v2/queries/38b06169-9f9b-4256-8396-b0ad8410528c/data/latest'
    else:
        url = ''
    r = requests.get(url)
    if r.status_code==200:
        df = pd.DataFrame(r.json())
    else:
        r = requests.get(url)
        assert r.status_code==200
        df = pd.DataFrame(r.json())
    df['BLOCK_TIMESTAMP'] = pd.to_datetime(df['BLOCK_TIMESTAMP'])
    df['TOKENID'] = df['TOKENID'].astype('int')
    return df.sort_values(by='BLOCK_TIMESTAMP',ascending=False)

def get_sales_activity(key='lilnoun'):
    if key == 'lilnoun':
        url = 'https://node-api.flipsidecrypto.com/api/v2/queries/177dc7b4-7560-4219-92d7-6b307700a307/data/latest'
    else:
        url = ''
    r = requests.get(url)
    if r.status_code==200:
        df = pd.DataFrame(r.json())
    else:
        r = requests.get(url)
        assert r.status_code==200
    df = pd.DataFrame(r.json())
    df['BLOCK_TIMESTAMP'] = pd.to_datetime(df['BLOCK_TIMESTAMP'])
    df['TOKENID'] = df['TOKENID'].astype('int')
    # df = df[['BLOCK_TIMESTAMP','WHO_SETTLES','TOKENID','ORIGIN_FROM_ADDRESS']]
    return df.sort_values(by='BLOCK_TIMESTAMP',ascending=False)

if __name__ == '__main__':
    key='noun'
    df = get_traits(key)
    sales = get_sales(key)
    transfers = get_transfers(key)
    
    ## https://lil.noun.pics/1900.jpg
    