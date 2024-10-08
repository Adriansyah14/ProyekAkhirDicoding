import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set(style='dark')

# helper function

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_approved_at').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return daily_orders_df

# 1
def create_mostorder_df(df):
    mostorder_df = all_df.groupby(by="product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
    mostorder_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return mostorder_df

# 2
def create_lessorder_df(df):
    lessorder_df = all_df.groupby(by="product_category_name_english").order_id.nunique().sort_values(ascending=True).reset_index()
    lessorder_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    return lessorder_df

# pertanyaan 3
def create_byreviewscore_df(df):
    byreviewscore_df = df.groupby(by="review_score").customer_id.nunique().reset_index()
    byreviewscore_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return byreviewscore_df

# 4
def create_bypaymenttype_df(df):
    bypaymenttype_df = all_df.groupby(by="payment_type").customer_id.nunique().reset_index()
    bypaymenttype_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return bypaymenttype_df

# 5
def create_bystate_df(df):
    bystate_df = all_df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return bystate_df

# load cleaned data
all_df = pd.read_csv("E:\LATIHAN DICODING (Data Science)\E-commerce-public-dataset\submission\dashboard\hasil_merge.csv")

datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Assuming your data has a column named 'timestamp' with extra characters
all_df['order_approved_at'] = all_df['order_approved_at'].str.replace('.098800128', '', regex=False)
all_df['order_delivered_customer_date'] = all_df['order_delivered_customer_date'].str.replace('.098800128', '', regex=False)

# Convert to datetime
all_df['order_approved_at'] = pd.to_datetime(all_df['order_approved_at'], format='mixed')
all_df['order_delivered_customer_date'] = pd.to_datetime(all_df['order_delivered_customer_date'], format='mixed')

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/Adriansyah14/ProyekAkhirDicoding/90add95535337ae6beba8467a7014d3a563bb7df/logo1.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                (all_df["order_approved_at"] <= str(end_date))]


st.header('E-Commerce Public Dashboard :100:')


st.subheader('The Most & Less Sold Products :medal:')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors1 = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
colors2 = ["#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000"]


mostorder_df = create_mostorder_df(all_df)
lessorder_df = create_lessorder_df(all_df)

sns.barplot(x="order_count", y="product_category_name_english", data=mostorder_df.head(10), palette=colors1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_count", y="product_category_name_english", data=lessorder_df.sort_values(by="order_count", ascending=True).head(10), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)


st.subheader("Customer Demographics")

byreviewscore_df = create_byreviewscore_df(all_df)
bypaymenttype_df = create_bypaymenttype_df(all_df)
bystate_df = create_bystate_df(all_df)

colors3 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#FF4500"]
colors4 = ["#FF4500", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors5 = ["#FF4500"]

col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="customer_count", 
        x="review_score",
        data=byreviewscore_df.sort_values(by="customer_count", ascending=False),
        palette=colors3,
        ax=ax
    )
    ax.set_title("Review Score by Customer", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="customer_count", 
        x="payment_type",
        data=bypaymenttype_df.sort_values(by="customer_count", ascending=False),
        palette=colors4,
        ax=ax
    )
    ax.set_title("Customer Payment Type", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="customer_count", 
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors5,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)