import streamlit as st
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px
from plots import number_plot, plot_dist,plot_dist_count,plot_settle1,plot_settle2

# @st.cache()
def get_pic(selected):
    st.image(f'https://noun.pics/{selected}.jpg')

@st.cache()
def get_merged(sales,df):
    return sales.merge(df,how='left',on='TOKENID')
    
cm = sns.light_palette("green", as_cmap=True)
mint_address = '0x0bc3807ec262cb779b38d65b38158acc3bfede10'
auction_house = '0x830bd73e4184cef73443c15111a1df14e495c706' 
def landing_page(key, df,sales,transfers,settler):
    st.image('nouns.png')
    st.markdown("""## Flipside Crypto <3 Nouns DAO
                
### Intro

The Nouns are an Ethereum NFT project that brings a unique minting mechanism to the NFT space. One Noun is auctioned trustlessly every 24 hours, forever. 100% of the proceeds from these auctions are sent to the DAO treasury, which as of the time of this writing sits at 24,780 ETH. Getting a Noun won’t be cheap, as recent auctions have closed at over 100 ETH. As a Noun token holder you are entitled to one vote in the DAO, which uses a fork of Compound Governance and controls the treasury. There are no rules about trait rarity, and the artwork is generative and stored on-chain. Once an auction ends, someone must settle the current auction to initiate a new auction, which will restart the minting / auction cycle.

A sub-DAO was recently formed out of Nouns DAO called Lil Nouns DAO. This project has many of the same characteristics of Nouns DAO, except Lil Nouns mint every 15 minutes as opposed to once a day. 

For more details, see https://nouns.wtf/ & https://lilnouns.wtf/
""")
    st.markdown(
        """
Part 1: 
""")
    st.markdown(
        """
### Analyze the mint and secondary NFT marketplace activity for Nouns DAO. 
""")
    
    
    selected = st.number_input('Select Noun', min_value=df['TOKENID'].min(), 
                               max_value=df['TOKENID'].max(),
                               value=df['TOKENID'].max())
    
    transfers_selected = transfers.query('(TOKENID==@selected) & (EVENT_TYPE=="other")').drop(['EVENT_TYPE','TOKENID'],axis=1)
    sales_selected = sales.query('TOKENID==@selected')
    current_address = transfers_selected.sort_values('BLOCK_TIMESTAMP',ascending=False)['NFT_TO_ADDRESS'].iloc[0]
    if current_address == mint_address:
        current_owner = ' Nouns DAO: Treasury'
    elif current_address == auction_house:
        current_owner = 'Nouns DAO: Nouns Auction House Proxy'
    else:
        current_owner = current_address
    get_pic(selected)
    st.write(f'https://nouns.wtf/noun/{selected}')
    
    st.markdown(f"""{key} {selected} current_owner: [{current_owner}](https://etherscan.io/address/{current_address})  
{sales_selected.shape[0]} sales
                """)
    with st.expander('show data'):
        l,r = st.columns(2)
        with l:
            st.write(f'transfers')
            
            st.dataframe(transfers_selected)
        with r:
            st.write(f'sales')
            st.dataframe(sales_selected)
    
    
    st.markdown("""
### Sales:
                """)
    
    fig = number_plot(sales,transfers)
    st.plotly_chart(fig)
    with st.expander('show data'):
        st.dataframe(sales)
        
    st.markdown(
        """
### Can we conclude if there are certain types of traits (body, accessory, etc.) that are causing some Nouns to sell or mint for more than others?
#### Sales
""")
    selected_trait = st.selectbox('Select Trait', ['BACKGROUND', 'BODY',
        'ACCESSORY', 'HEAD', 'GLASSES'],0)
    with st.expander('Show'):
        # traits sales
        merged = get_merged(sales,df)
        
        cols = ['BACKGROUND', 'BODY',
        'ACCESSORY', 'HEAD', 'GLASSES']
        extra = ['TOKENID','PRICE']
        merged= sales.merge(df,how='left',on='TOKENID')
        m = merged[cols+extra].groupby(selected_trait)['PRICE'].agg(['mean','count']).reset_index()
        mean_price_single = m.sort_values('mean',ascending=False).iloc[0]
        single = merged[merged[selected_trait]==mean_price_single[selected_trait]][['BLOCK_TIMESTAMP','TOKENID','PRICE',selected_trait]].sort_values('BLOCK_TIMESTAMP',ascending=False).iloc[0]
        #st.write(single)
        l,r = st.columns([6,12])
        with l:
            st.dataframe(m.sort_values('mean',ascending=False).style.background_gradient(cmap=cm))
        with r:
            fig,mean = plot_dist(m)
            st.plotly_chart(fig,use_container_width=True)
        l,r = st.columns([10,8])
        with r:
            st.markdown(f"""  
    #  
    #  
    #  
    #      
    attribute number {int(single[selected_trait])} has been 
    sold {int(mean_price_single['count'])} times     
    mean_price: {mean_price_single['mean']:.2f} ETH   
    max price {single['PRICE']:.2f} ETH  

    mean price across all attributes: {mean:.2f} ETH
    """)
        with l:
            st.write(f'Noun {int(single["TOKENID"])} with the most expensive attribute {int(single[selected_trait])}')
            get_pic(int(single['TOKENID']))
            st.write(f"https://nouns.wtf/noun/{int(single['TOKENID'])}")
            
    ###############
    st.markdown(
        """
#### Mints
""")
    with st.expander('Show'):
        # traits mints
        merged = get_merged(transfers.query('EVENT_TYPE=="mint"'),df)
        cols = ['BACKGROUND', 'BODY',
        'ACCESSORY', 'HEAD', 'GLASSES']
        extra = ['TOKENID']
        merged= sales.merge(df,how='left',on='TOKENID')
        m = merged[cols+extra].groupby(selected_trait)['TOKENID'].agg(['count']).reset_index()
        mean_price_single = m.sort_values('count',ascending=False).iloc[0]
        single = merged[merged[selected_trait]==mean_price_single[selected_trait]][['BLOCK_TIMESTAMP','TOKENID',selected_trait]].sort_values('BLOCK_TIMESTAMP',ascending=False).iloc[0]
        #st.write(single)
        l,r = st.columns([6,12])
        with l:
            st.dataframe(m.sort_values('count',ascending=False).style.background_gradient(cmap=cm))
        with r:
            fig,mean = plot_dist_count(m)
            st.plotly_chart(fig,use_container_width=True)
        l,r = st.columns([10,8])
        with r:
            st.markdown(f"""  
    #  
    #  
    #  
    #    
    trait number {int(single[selected_trait])}  has been minted {int(mean_price_single['count'])} times       
    """)
        with l:
            st.write(f'Noun {int(single["TOKENID"])} with the most common attribute {int(single[selected_trait])}')
            get_pic(int(single['TOKENID']))
            st.write(f"https://nouns.wtf/noun/{int(single['TOKENID'])}")
            
  ############### 
    
    st.markdown(
        """
### PArt2: Who is typically settling Nouns auctions? 
""")
    st.markdown(
        """
### Does the winner settle the auction, or does an eager new bidder settle the current auction to begin the next auction?

    """)
    
    l,r = st.columns(2)
    with l:
        st.dataframe(settler)
    with r:
        st.pyplot(plot_settle1(settler), use_container_width=True)
        st.pyplot(plot_settle2(settler), use_container_width=True)
    st.markdown(f""" ## Conclusion

- The winner nowadays settles the auctions less frequently than in the past
- 2/3 times to eager new bidder does the settlement
- There are many attributes in the traits class that have yet to be seen significant trading activity. 
Thus it is hard to say whether there are attributes of traits that are more preferred than other ones.
Noun 40 has been sold for 200ETH. This is exploding for many traits the average price as there is not 
yet an established secondary market since only ~340 Nouns have been minted.
- However we find a linear correlation showing that older Nouns tend to sell with higher amounts than newer ones.
- Not one Noun has been sold more than 2 times.
- Green Glasses tend to send in higher amounts than others. (these have been sold 17 times) but also minted 3 most frequent (7 times).
- Other frequently minted glasses 12 and 5 (blue glasses), sell with lower price than the green ones (17) (103 ETH vs 77 ETH and and 89 ETH )

### Queries used
[settling_the_nouns_transactions](https://app.flipsidecrypto.com/velocity/queries/1abcd9e9-23ec-47ae-8d3c-c8e43e127e7e)   
[nft transfers](https://app.flipsidecrypto.com/velocity/queries/94811dd6-4a66-4bb6-9e86-49feae817816)    
[nft sales](https://app.flipsidecrypto.com/velocity/queries/38b06169-9f9b-4256-8396-b0ad8410528c)   
[nft mints](https://app.flipsidecrypto.com/velocity/queries/4cb81caa-4088-40e0-933d-d8a057603d0b)   

### Github
[https://github.com/kkpsiren/Nouns_DAO](https://github.com/kkpsiren/Nouns_DAO)
    """)