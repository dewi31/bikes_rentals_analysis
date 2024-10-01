import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Pembuatan helper function

def create_sum_daily_rent(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum" 
    })
    
    daily_rent_df = daily_rent_df.reset_index() 

    daily_rent_df.rename(columns={
        "casual": "casual_count",
        "registered": "register_count",
        "cnt": "rent_count" 
    }, inplace=True)
    
    return daily_rent_df

def create_sum_bike_days(df):
    sum_bike_days = df.groupby("week_map").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_bike_days

def create_sum_bike_season(df):
    sum_bike_season = df.groupby("season_map").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_bike_season

def create_sum_bike_workday(df):
    sum_bike_workday = df.groupby("workday_map").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_bike_workday


rental_df = pd.read_csv('dashboard/rental_data.csv')

datetime_columns = ["dteday"]
rental_df.sort_values(by="dteday", inplace=True)
rental_df.reset_index(drop=True, inplace=True)

# Mengubah kolom dteday menjadi datetime
for column in datetime_columns:
    rental_df[column] = pd.to_datetime(rental_df[column])

min_date = rental_df["dteday"].min()
max_date = rental_df["dteday"].max()

# Membuat filter di sidebar
with st.sidebar:
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = rental_df[(rental_df["dteday"] >= pd.to_datetime(start_date)) & 
                    (rental_df["dteday"] <= pd.to_datetime(end_date))]

# Membuat beberapa dataframe dengan helper function
daily_rent_df = create_sum_daily_rent(main_df)
sum_bike_days = create_sum_bike_days(main_df)
sum_bike_season = create_sum_bike_season(main_df)
sum_bike_workday = create_sum_bike_workday(main_df)

# visualisasi data
st.header('Bike Sharing Dashboard \U0001F6B2')
st.subheader('Daily Rent')
    
col1, col2, col3 = st.columns(3)
    
with col1:
        total_rent = main_df.cnt.sum()
        st.metric("Total daily rent", value=f"{total_rent:,}")
    
with col2:
        total_rent_casual = main_df.casual.sum()
        st.metric("Number of casual users", value=f"{total_rent_casual:,}")

with col3:
        total_rent_rgstr = main_df.registered.sum()
        st.metric("Number of registered user", value=f"{total_rent_rgstr:,}")

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(
        daily_rent_df["dteday"],
        daily_rent_df["rent_count"],
        marker='o', 
        linewidth=2,
        color="#A594F9"
    )
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
    
st.pyplot(fig)

st.subheader("Bike Sharing Demographics")
 
col1, col2 = st.columns(2)

with col1:

    fig, ax = plt.subplots(figsize=(10, 8))
    colors_ = ["#A594F9", "#CDC1FF", "#CDC1FF", "#CDC1FF"]
    sns.barplot(
                x="season_map", 
                y="cnt",
                data=sum_bike_season.sort_values(by="cnt", ascending=False),
                palette=colors_,
                ax=ax
            )
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.set_title("Bikes Rentals by Season", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:

    fig, ax = plt.subplots(figsize=(10, 8))
    colors_ = ["#A594F9", "#CDC1FF"]
    sns.barplot(
                x="workday_map", 
                y="cnt",
                data=sum_bike_workday.sort_values(by="cnt", ascending=False),
                palette=colors_,
                ax=ax
            )
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.set_title("Bikes Rentals by Workday", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)


fig, ax = plt.subplots(figsize=(18, 15))
colors_ = ["#A594F9", "#CDC1FF", "#CDC1FF", "#CDC1FF", "#CDC1FF", "#CDC1FF", "#CDC1FF"]
sns.barplot(
                x="cnt", 
                y="week_map",
                data=sum_bike_days.sort_values(by="cnt", ascending=False),
                palette=colors_,
                ax=ax
            )
ax.set_title("Bikes Rentals by Days", loc="center", fontsize=40)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
