import streamlit as st
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px
from plots import plot_timestampts, plot_dist_lil, plot_prices
from utils import get_pic


cm = sns.light_palette("green", as_cmap=True)
mint_address = '0x0bc3807ec262cb779b38d65b38158acc3bfede10'
auction_house = '0x830bd73e4184cef73443c15111a1df14e495c706' 
def landing_page(key, df,sales,transfers,settler):
    st.markdown("""
# Flipside Crypto <3 Nouns DAO
""")
    st.image('lilnouns.png')
    st.markdown(f"""
## Secondary Sales Activity          
### Intro

The Nouns are an Ethereum NFT project that brings a unique minting mechanism to the NFT space. One Noun is auctioned trustlessly every 24 hours, forever. 100% of the proceeds from these auctions are sent to the DAO treasury, which as of the time of this writing sits at 24,780 ETH. Getting a Noun won’t be cheap, as recent auctions have closed at over 100 ETH. As a Noun token holder you are entitled to one vote in the DAO, which uses a fork of Compound Governance and controls the treasury. There are no rules about trait rarity, and the artwork is generative and stored on-chain. Once an auction ends, someone must settle the current auction to initiate a new auction, which will restart the minting / auction cycle.

A sub-DAO was recently formed out of Nouns DAO called Lil Nouns DAO. This project has many of the same characteristics of Nouns DAO, except Lil Nouns mint every 15 minutes as opposed to once a day. 

For more details, see https://nouns.wtf/ & https://lilnouns.wtf/.

### How many Lil Nouns have been sold on a secondary exchange within 24 hours of being minted? 

- {settler['TOKENID'].nunique()} Lil Nouns out of {df['TOKENID'].nunique()} Lil Nouns have been sold on a secondary exchange within 24 hour of being minted.
""")
    st.plotly_chart(plot_timestampts(settler))
    with st.expander('show data'):
        st.dataframe(settler.sort_values('BLOCK_TIMESTAMP',ascending=False))
    
    st.markdown("""
Above, we see that more recent mints have been less sold in the secondary markets than the ones minted between May 15th and May 22th.    
Additionally these mid-May mints have had also higher prices.          
                
### Are there any common traits among these Lil Nouns?  
""")
    merged = settler.merge(df,on='TOKENID',how='left')
    #c1,c2,c3 = st.columns(3)
    #c4,c5 = st.columns(2)
    traits = [i for i in df.columns[-5:]]
    for k,trait in enumerate(traits):
        k = k+1
        data = merged.groupby(trait)['PRICE'].agg(['mean','count']).rename({'mean':'Mean_Price_ETH','count':'Events'},axis=1)
        data.index.name = trait
        # st.dataframe(data)
        # with eval(f'c{k}'):
        st.plotly_chart(plot_dist_lil(data.sort_values(['Events','Mean_Price_ETH'],ascending=[False,False])),use_container_width=True)
    #st.dataframe(df)
    
    st.markdown("""
We see that the attributes of traits are still relatively rare. Cool and Warm backgrounds have to sold relatively same amount (67 vs 64 times),
while Cool background is slightly more expensive than Warm background with average price of 0.96 ETH vs 0.9 ETH, however these price differences are insignificant.  

The Lil Nouns with Teal-Light background tend to sell more often in the secondary markets than other body attributes, however the average sell price is also lower. This suggests that these tend to appear also more frequently.                

There is no Lil Nouns accessory attributes that are sticking out since there are so many traits inside this attribute.  Body-Gradient-Redpink and Checkers-Big-Red-Cold are leading as they have been sold four times in 24 hours after mint.

Similar story is also with head attributes with a wide disperse array of unique attributes here. The most common traits that have been sold for this attribute are Werewolf and Beet.

For the Glasses trait, Square-Black and Square-Yellow-Orange-Multi are the most common attributes as they have been sold both 10 times in the 24 hours. 

For all, it appears that the mean price doesn't follow this "sought after" attributes and traits.

### Which Lil Noun’s have the biggest difference (positive or negative) between their mint price and secondary sale price? 
""")
    
    st.plotly_chart(plot_prices(settler))
    st.markdown(
        """
#### The Top 5 Lil Nouns that have had highest positive differences in sell prices      
""")
    small_set = settler.sort_values('PRICE_DIFF',ascending=False).head(5)
    s1,s2,s3,s4,s5 = st.columns(5)
    l = 0
    for i,ser in small_set.iterrows():
        l = l+1
        with eval(f's{l}'):
            get_pic(ser['TOKENID'])
            st.markdown(f"""
Lil Noun # {ser['TOKENID']}    
Minted {ser['MINT_PRICE']}  
Sold {ser['PRICE']}  
Difference {ser['PRICE_DIFF']} ETH  
                    """)

    st.markdown(
        """
#### The Top 5 Lil Nouns that have had highest negative differences in sell prices      
""")
    small_set = settler.sort_values('PRICE_DIFF',ascending=True).head(5)
    s1,s2,s3,s4,s5 = st.columns(5)
    l = 0
    for i,ser in small_set.iterrows():
        l = l+1
        with eval(f's{l}'):
            get_pic(ser['TOKENID'])
            st.markdown(f"""
Lil Noun # {ser['TOKENID']}    
Minted {ser['MINT_PRICE']}  
Sold {ser['PRICE']}  
Difference {ser['PRICE_DIFF']} ETH  
                    """)
    
    
    st.markdown("""
### Queries used

[Traits](https://app.flipsidecrypto.com/velocity/queries/75655225-bbdc-4c76-98f5-48e0e94bac82)   
[Secondary Sales Activity](https://app.flipsidecrypto.com/velocity/queries/177dc7b4-7560-4219-92d7-6b307700a307)    

### Github

[https://github.com/kkpsiren/Nouns_DAO](https://github.com/kkpsiren/lilnouns_DAO)

### Cool Links

[Explore Lil Nouns](https://lilnouns.notion.site/lilnouns/Explore-Lil-Nouns-db990658e6ab4cf19121b22642645032)
    
""")