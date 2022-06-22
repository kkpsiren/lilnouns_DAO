import plotly.express as px
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, MaxNLocator
import seaborn as sns
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_strip(data,x,y,scale=False):
    fig,ax = plt.subplots()
    sns.stripplot(data=data,x=x,y=y,ax=ax)
    if scale:
        plt.yscale('log')
    sns.despine()
    return fig


def plot_groups(data, groups):
    data['groups'] = groups
    data = data.query('groups!="C0"')
    s = data.groupby('groups').quantile(0.5)
    g1 = plot_strip(data,x='groups',y='minted',scale=True)
    g2 = plot_strip(data,x='groups',y='NFT_history',scale=False)
    g3 = plot_strip(data,x='groups',y='ETH_balance',scale=True)

    return g1,g2,g3,s

def cluster_plot(data):
    dist = pdist(data.values, metric='correlation')
    Z = hierarchy.linkage(dist, 'single')
    
    g = sns.clustermap(data.T.corr(),
        row_linkage=Z,
        col_linkage=Z,)
    den = hierarchy.dendrogram(g.dendrogram_col.linkage, labels=data.index,
                            color_threshold=0.10, distance_sort=True, ax=g.ax_col_dendrogram)
    g.ax_col_dendrogram.axis('on')
    # sns.despine(ax=g.ax_col_dendrogram, left=False, right=True, top=True, bottom=True)
    g.ax_col_dendrogram.yaxis.set_major_locator(MaxNLocator())
    g.ax_col_dendrogram.yaxis.set_major_formatter(ScalarFormatter())
    g.ax_col_dendrogram.grid(axis='y', ls='--', color='grey')
    # g.ax_col_dendrogram.yaxis.tick_right()
    
    groups = pd.Series(den['leaves_color_list'], index= [data.index[i] for i in den['leaves']])
    return g.fig, groups


def number_plot(df,mint):
    ser = df['TOKENID'].value_counts().sort_values(ascending=False)
    # fig,(ax,ax1) = plt.subplots(ncols=2,figsize=(12,4))
    a = ser.to_frame('counts').reset_index()
    a = a.rename({'index':'TOKENID'},axis=1)
    a = a.reset_index()
    a['last_sold'] = a['TOKENID'].map(df.groupby('TOKENID')['BLOCK_TIMESTAMP'].max())
    a['minted'] = a['TOKENID'].map(mint.groupby('TOKENID')['BLOCK_TIMESTAMP'].min())
    a['diff'] = (a['last_sold'] - a['minted']).dt.days
    a['price'] = a['TOKENID'].map(df.sort_values('BLOCK_TIMESTAMP',ascending=False).groupby('TOKENID')['PRICE'].first())
    # a['diff'] = a['last_sold'] - a['minted']
    # a['counts'].plot(ax=ax)


    fig = make_subplots(rows=2, cols=2)

    fig.add_trace(
        go.Scatter(x=a['index'].tolist(), 
                   y=a['counts'].tolist(),
                   hovertemplate =
                    '<i>Number of Sales</i>: %{y:.0f}<br>'+
                    '%{text}',
                   text = [f'<b>Token ID</b>: {k}<br><b>Last Sale</b>: {i}<br><b>Minted</b>: {j}' for k,i,j in zip(a['TOKENID'].tolist(), a['last_sold'].tolist(),a['minted'].tolist())],
                   
                   showlegend = False),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=a['TOKENID'].tolist(), 
                   y=a['counts'].tolist(),
                   mode="markers",
                   hovertemplate =
                    '<br><b>Token ID</b>: %{x}<br>'+
                    '<i>Number of Sales</i>: %{y:.0f}<br>'+
                    '%{text}',
                   text = [f'<b>Last Sale</b>: {i}<br><b>Minted</b>: {j}' for i,j in zip(a['last_sold'].tolist(),a['minted'].tolist())],
    
                   showlegend = False),
        row=1, col=2,
        
    )

    fig.add_trace(
        go.Scatter(x=a['diff'].tolist(), 
                   y=a['price'].tolist(),
                   mode="markers",
                   hovertemplate =
                   '<i>Minted %{x:.0f} days before Sold</i><br>'+
                    '<br><b>Last Price</b>: %{y:.2f} ETH<br>'+
                    '%{text}',
                   text = [f'<b>Token ID</b>: {k}<br><b>Last Sale</b>: {i}<br><b>Minted</b>: {j}' for k,i,j in zip(a['TOKENID'].tolist(),a['last_sold'].tolist(),a['minted'].tolist())],
    
                   showlegend = False),
        row=2, col=1,
        
    )


    fig.update_layout(height=800, width=800, title_text="Sales")
    fig['layout']['xaxis']['title']='Index'
    fig['layout']['yaxis']['title']='Number of Sales'
    fig['layout']['xaxis2']['title']='Token ID'
    fig['layout']['yaxis2']['title']='Number of Sales'
    fig['layout']['xaxis3']['title']='Days since Mint'
    fig['layout']['yaxis3']['title']='Price (ETH)'
    #plt.xticks([])
    # ax.set_xlabel('Number of NFTs')
    # ax.set_ylabel('Number Sales')
    # a.plot.scatter(x='TOKENID',y='counts',ax=ax1)
    # ax1.set_ylabel('Number Sales')
    # ax1.set_xlabel('TokenID')

    #sns.despine(fig=fig)
    return fig


def nft_plot(df):
    fig,ax = plt.subplots()
    df.reset_index()['NFT_ADDRESS'].plot(ax=ax)
    #plt.xticks([])
    plt.xlabel('Addresses')
    plt.ylabel('Number of NFTs Bought')
    sns.despine(fig=fig)
    return fig

def plot_dist(a):
    mean = a['mean'].mean()
    first_idx = a.columns[0]
    string = f'<br><b>{first_idx}</b>: '
    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Bar(x=a[first_idx].tolist(), 
                   y=a['mean'].tolist(),
                   hovertemplate =
                    string + '%{x}<br>'+
                    '<i>Median Price</i>: %{y:.2f} ETH<br>'+
                    '%{text}',
                   text = [f'<br><b>Number of Sales</b>: {i}' for i in a['count'].tolist()],
                   
                   showlegend = False),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
                   x=a[first_idx].tolist(), 
                   y=[mean for k in a['mean'].tolist()],
                   name='mean',
                   showlegend = False
                   ),
            row=1, col=1
    )

    fig.update_layout(height=400, width=400, title_text="Sales")
    fig['layout']['xaxis']['title']=f'{first_idx} Type'
    fig['layout']['yaxis']['title']='Mean Price'
    return fig, mean

def plot_settle1(df):
    fig, ax = plt.subplots()
    df.groupby('WHO_SETTLES')['TOKENID'].count().plot.bar(ax=ax)
    return fig

def plot_settle2(df):
    fig, ax = plt.subplots()
    df.plot.scatter(x='BLOCK_TIMESTAMP',y='WHO_SETTLES',ax=ax)
    plt.xticks(rotation=45)
    return fig


def plot_dist_count(a):
    mean = a['count'].mean()
    first_idx = a.columns[0]
    string = f'<br><b>{first_idx}</b>: '
    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Bar(x=a[first_idx].tolist(), 
                   y=a['count'].tolist(),
                   hovertemplate =
                    string + '%{x}<br>'+
                    '<i>Count</i>: %{y:.0f} times<br>',
                    #'%{text}',
                   #text = [f'<br><b>Number of Sales</b>: {i}' for i in a['count'].tolist()],
                   
                   showlegend = False),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
                   x=a[first_idx].tolist(), 
                   y=[mean for k in a['count'].tolist()],
                   name='mean count',
                   showlegend = False
                   ),
            row=1, col=1
    )

    fig.update_layout(height=400, width=400, title_text="Mints")
    fig['layout']['xaxis']['title']=f'{first_idx} Type'
    fig['layout']['yaxis']['title']='Count'
    return fig, mean


def plot_timestampts(df):
    df['BLOCK_TIMESTAMP'] = pd.to_datetime(df['BLOCK_TIMESTAMP'])
    df['MINT_TIMESTAMP'] = pd.to_datetime(df['MINT_TIMESTAMP'])

    fig = px.scatter(df, x="MINT_TIMESTAMP", y="BLOCK_TIMESTAMP", color="PRICE",
                     color_discrete_sequence=px.colors.qualitative.G10,
                     template='simple_white',title='MINT vs SECONDARY SELL',
                hover_data=['TOKENID','BLOCK_TIMESTAMP','MINT_TIMESTAMP','PRICE','BUYER_ADDRESS','SELLER_ADDRESS'],
                width=700, height=600)
    fig.update_layout(legend=dict(
    yanchor="top",
    y=-0.5,
    xanchor="left",
    x=0.01
))
    return fig

def plot_scatter(df):
    i = df['USER_ADDRESS'].unique()[0]
    df['BALANCE_DATE'] = pd.to_datetime(df['BALANCE_DATE'])
    df['SYMBOL'] = df['SYMBOL'].fillna(df['CONTRACT_ADDRESS'])
    fig = px.scatter(df, x="BALANCE_DATE", y="BALANCE", color="SYMBOL",
                     color_discrete_sequence=px.colors.qualitative.G10,
                     template='simple_white',title=i,
                hover_data=['SYMBOL'],width=800, height=800)
    fig.update_layout(legend=dict(
    yanchor="top",
    y=-0.5,
    xanchor="left",
    x=0.01
))
    return fig

def plot_dist_lil(a):
    #mean = a['mean'].mean()
    #first_idx = a.columns[0]
    #string = f'<br><b>{first_idx}</b>: '
    fig = make_subplots(rows=1, cols=1,specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(y=a['Events'].tolist(), 
                   x=a.index.tolist(),
                   hovertemplate =
                    '%{x}<br>'+
                    '<i>Number of Sales</i>: %{y}<br>'+
                    '%{text}',
                   text = [f'<br><b>Average Price</b>: {i:.2f} ETH' for i in a['Mean_Price_ETH'].tolist()],
                   
                   showlegend = False),
        secondary_y=False,
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
                   x=a.index.tolist(), 
                   y=a['Mean_Price_ETH'].tolist(),
                   name='Mean Price',
                   
                   showlegend = False
                   ),
        secondary_y=True,
        row=1, col=1
    )
    fig.update_layout(height=400, width=400, title_text=a.index.name)
    fig['layout']['xaxis']['title']=f'{a.index.name}'
    fig.update_yaxes(title_text="Number of Sales", secondary_y=False)
    fig.update_yaxes(title_text="Average Price", secondary_y=True)
    return fig


def plot_prices(df):
    df['BLOCK_TIMESTAMP'] = pd.to_datetime(df['BLOCK_TIMESTAMP'])
    df['MINT_TIMESTAMP'] = pd.to_datetime(df['MINT_TIMESTAMP'])

    fig = px.scatter(df, x="MINT_PRICE", y="PRICE", color="PRICE_DIFF",
                     color_discrete_sequence=px.colors.qualitative.G10,
                     template='simple_white',title='MINT vs SECONDARY SELL',
                hover_data=['TOKENID','BLOCK_TIMESTAMP','MINT_TIMESTAMP','PRICE_DIFF','PRICE','MINT_PRICE','BUYER_ADDRESS','SELLER_ADDRESS'],
                width=700, height=600)
    fig.update_layout(legend=dict(
    yanchor="top",
    y=-0.5,
    xanchor="left",
    x=0.01
))
    return fig


def eth_plot(df):
    fig,ax = plt.subplots()
    df.plot(x='USER_ADDRESS',y='BALANCE',ax=ax)
    plt.xticks([])
    plt.xlabel('Addresses')
    plt.ylabel('ETH balance')
    sns.despine()
    return fig