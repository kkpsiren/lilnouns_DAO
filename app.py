import streamlit as st
#from scripts.utils import read_flipside
from landing import landing_page
from beautify import flipside_logo, discord_logo
import os

from traits import *
# from dotenv import load_dotenv
# load_dotenv()

key = 'noun'
df = get_traits(key)
sales = get_sales(key)
transfers = get_transfers(key)
settler = get_settler(key)     

st.set_page_config(page_title="Flipside Crypto: Nouns DAO", layout="wide")

# df = read_flipside(url)

#radio_choice = st.sidebar.radio("Choose", ("Main",
#                                           #"Individual Addresses"
#                                           ), index=0)
#if radio_choice == "Main":
#elif radio_choice == "Individual Addresses":
#    address_page(df,df_minted,df_images)
        
#else:
#    st.write("shouldn't be here")


st.sidebar.markdown("#### Connect")
discord_logo(os.getenv('DISCORD_USERNAME'))
flipside_logo()
flipside_logo(url="https://godmode.flipsidecrypto.xyz/")
landing_page(key, df, sales, transfers, settler)
