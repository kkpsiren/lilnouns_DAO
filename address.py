import streamlit as st
from utils import get_pic

def print_meta(query_df,selected_noun):
    get_pic(selected_noun)
    st.markdown(f'Lil Noun #{selected_noun}')
    data = query_df.query('TOKENID==@selected_noun').iloc[0]
    st.markdown(f'''
    Minted at {data["MINT_TIME"]}  
    Mint hash [{data["MINT_HASH"]}](https://etherscan.io/tx/{data["MINT_HASH"]})  
    Background: {data['BACKGROUND']}  
    Body: {data['BODY']}  
    Accessory: {data['ACCESSORY']}  
    Head: {data['HEAD']}  
    Glasses: {data['GLASSES']}  
    ''')
    
    
def address_page(key, df, sales, transfers, settler, radio_choice):
    traits = [i for i in df.columns[-5:]]
    nouns = sorted(df['TOKENID'].unique())

    st.write(f'browser page for {radio_choice}')
    
    if radio_choice == "Browse Nouns":
        selected_noun = st.number_input('Select noun', min_value=0, max_value=df['TOKENID'].max())
        
        query_df = df.query('TOKENID==@selected_noun')
        print_meta(query_df,selected_noun)
        
    else:
        selected_trait = st.selectbox('Select Trait', traits)
        attributes = df[selected_trait].unique()
        selected_attribute = st.multiselect('Select Attributes', attributes)
        query_df = df[df[selected_trait].isin(selected_attribute)]
        nouns = query_df['TOKENID'].unique()
        if len(nouns) <=5:
            noun_list = nouns
        else:
            noun_list = nouns[:5]
        for selected_noun in noun_list:
            print_meta(query_df,selected_noun)
