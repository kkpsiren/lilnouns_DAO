import streamlit as st
#from scripts.utils import read_flipside
from landing import landing_page
from address import address_page
from beautify import flipside_logo, discord_logo
import os

from traits import *
# from dotenv import load_dotenv
# load_dotenv()
st.set_page_config(page_title="Flipside Crypto: Lil Nouns", layout="wide")

key = 'lilnoun'
df = get_traits(key)
sales = None #get_sales(key)
transfers = None #get_transfers(key)
settler = get_sales_activity(key)     



# df = read_flipside(url)

radio_choice = st.sidebar.radio("Choose", ("Main",
                                           "Browse Nouns",
                                           "Browse Traits",
                                           ), index=0)

st.sidebar.markdown("#### Connect")
discord_logo(os.getenv('DISCORD_USERNAME'))
flipside_logo()
flipside_logo(url="https://godmode.flipsidecrypto.xyz/")


if radio_choice == "Main":
    landing_page(key, df, sales, transfers, settler)

elif radio_choice == "Browse Nouns":
    address_page(key, df, sales, transfers, settler, radio_choice)

elif radio_choice == "Browse Traits":
    address_page(key, df, sales, transfers, settler, radio_choice)
              
else:
    st.write("shouldn't be here")


