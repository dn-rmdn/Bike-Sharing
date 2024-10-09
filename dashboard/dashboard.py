import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
sns.set(style='ticks')

# Creating Functions
def resample_data(data, timeframe):
    if timeframe == 'daily':
        r_data = data.resample(rule='D', on='date').agg({
            "temp": "mean",
            "atemp": "mean",
            "humidity": "mean",
            "wind_speed": "mean",
            "casual": "sum",
            "registered": "sum",
            "total": "sum"
        })
    elif timeframe == 'monthly':
        r_data = data.resample(rule='M', on='date').agg({
            "temp": "mean",
            "atemp": "mean",
            "humidity": "mean",
            "wind_speed": "mean",
            "casual": "sum",
            "registered": "sum",
            "total": "sum"
        })
    elif timeframe == 'weekly':
        r_data = data.resample(rule='W-MON', on='date').agg({
            "temp": "mean",
            "atemp": "mean",
            "humidity": "mean",
            "wind_speed": "mean",
            "casual": "sum",
            "registered": "sum",
            "total": "sum"
        })
    elif timeframe == 'quarterly':
        r_data = data.resample(rule='Q', on='date').agg({
            "temp": "mean",
            "atemp": "mean",
            "humidity": "mean",
            "wind_speed": "mean",
            "casual": "sum",
            "registered": "sum",
            "total": "sum"
        })
    elif timeframe == 'yearly':
        r_data = data.resample(rule='A', on='date').agg({
            "temp": "mean",
            "atemp": "mean",
            "humidity": "mean",
            "wind_speed": "mean",
            "casual": "sum",
            "registered": "sum",
            "total": "sum"
        })
    
    return r_data

def group_data(data, kind):
    if kind == 'season':
        g_data = data.groupby('season').agg({
        'registered':'mean',
        'casual':'mean',
        'total': 'mean'
        }).reset_index()
    elif kind == 'weather':
        g_data = data.groupby('weather_situation').agg({
        'casual':'mean',
        'registered':'mean',
        'total': 'mean'
        }).reset_index()
    elif kind == 'hoursea':
        g_data = data.groupby(by=['hour','season']).agg({
            "casual": "mean",
            "registered": "mean",
            "total": "mean"
            }).reset_index()
    elif kind == 'hour':
            g_data = data.groupby(by=['hour']).agg({
            "casual": "mean",
            "registered": "mean",
            "total": "mean"
            }).reset_index()

    return g_data

# Load the dataset
all_df = pd.read_csv('dashboard/hour_df.csv')
all_df['date'] = pd.to_datetime(all_df['date'])

# Sidebar settings
st.header('Bike Sharing Analysis :bike:')
st.sidebar.image("https://github.com/dn-rmdn/logo_assets/blob/main/Bike%20Share.jpg?raw=true", width=300)
min_date = all_df['date'].min().date()
max_date = all_df['date'].max().date()

# Date range filters
start_date, end_date = st.sidebar.date_input(
    label='Time interval',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Convert date objects to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filtering data based on selected date range
filtered_data = all_df[(all_df['date'] >= start_date) & (all_df['date'] <= end_date)]

# Calculate today's count and yesterday's count
todays= int(filtered_data['total'].iloc[-1])
yesterdays= int(filtered_data['total'].iloc[-2])

# Display the metric in the sidebar with thousand separators
st.sidebar.metric(
    label="Daily growth of users",
    value=todays,
    delta=yesterdays
)

# Data transform
daily_users = resample_data(filtered_data, timeframe='daily')
weekly_users = resample_data(filtered_data, timeframe='weekly')
monthly_users = resample_data(filtered_data, timeframe='monthly')
quarterly_users = resample_data(filtered_data, timeframe='quarterly')
yearly_users = resample_data(filtered_data, timeframe='yearly')

mean_season = group_data(filtered_data, kind='season')
mean_weather = group_data(filtered_data, kind='weather')
mean_hoursea = group_data(filtered_data, kind='hoursea')
mean_hour = group_data(filtered_data, kind='hour')
cluster = group_data(filtered_data, kind='hour')

mean_weather['weather_situation'] = mean_weather['weather_situation'].replace({1: 'Clear/Partly Cloudly', 2: 'Misty/Cloudy', 
                                                                          3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'})

# 1st row
st.subheader('Total Users')

with st.container():

    col1, col2, col3 = st.columns(3)


    with col1:
        total_casual = daily_users.casual.sum()
        st.metric("Total Casual Users", value=f"{total_casual:,}")

    with col2:
        total_registered = daily_users.registered.sum()
        st.metric("Total Registered Users", value=f"{total_registered:,}")

    with col3:
        total = daily_users.total.sum()
        st.metric("Total Users", value=f"{total:,}")

colors = ['#367BE0', '#E04A36', '#B9E036']
# 2nd row
with st.container():
        st.subheader('Daily Users')

        # set figure size
        fig1, ax1 = plt.subplots(figsize=(10,5))
        # Plotting
        sns.lineplot(x='date', y='total', data=daily_users, ax=ax1, linewidth=2, color=colors[0])
        ax1.set_ylabel("Total users", fontsize=14)
        ax1.set_xlabel(" ")
        ax1.set_title(" ", fontsize=20)
        ax1.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability

        # Display the plot in Streamlit
        plt.tight_layout()
        plt.show()

        st.pyplot(fig1)

#3rd row
with st.container():
    st.subheader('Popular Usage')
    tab1, tab2= st.tabs(["Hourly", "Season & Weather"])

    # ticks formatting 
    hour_labels = [f'{int(h):02d}.00' for h in mean_hour['hour'].unique()]

    with tab1:
        # set figure size
        fig2, ax2 = plt.subplots(figsize=(12,7))
        # Plotting
        sns.barplot(x='hour', y='total', data=mean_hour, ax=ax2, color=colors[0])
        ax2.set_ylabel("Avg. of Users per Hour", fontsize=14)
        ax2.set_xlabel(" ")
        ax2.set_title(" ")
        plt.xticks(ticks=mean_hour['hour'].unique(), labels=hour_labels, rotation=45)
        ax2.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
        
        plt.xticks(fontsize=11)  # X-axis tick font size
        plt.yticks(fontsize=11)  # Y-axis tick font size

        plt.tight_layout()
        plt.show()
        
        st.pyplot(fig2)

    with tab2:
        #create bar chart
        fig3, ax3 = plt.subplots(nrows=1, ncols=2, figsize=(12,7))

        sns.barplot(x='season', y='registered', 
                    data=mean_season, ax=ax3[0],
                    label='Registered', color=colors[0])
        sns.barplot(x='season', y='casual', 
                    data=mean_season, ax=ax3[0],
                    label='Casual', color=colors[1])

        ax3[0].set_ylabel("Avg. of Users", fontsize=14)
        ax3[0].set_xlabel(" ")
        ax3[0].set_title("Avg. of Casual and Registered Users by Season", fontsize=16)
        ax3[0].set_ylim((0,200))
        ax3[0].legend(loc='upper right')

        plt.xticks(fontsize=11)  # X-axis tick font size
        plt.yticks(fontsize=11)  # Y-axis tick font size

        sns.barplot(x='weather_situation', y='registered', 
                    data=mean_weather, ax=ax3[1], 
                    label='Registered', color=colors[0])
        sns.barplot(x='weather_situation', y='casual', 
                    data=mean_weather, ax=ax3[1], 
                    label='Casual', color=colors[1])
        ax3[1].set_ylabel("Avg. of Users", fontsize=14)
        ax3[1].set_xlabel(" ")
        ax3[1].set_title("Avg. of Casual and Registered Users by Weather Situation", fontsize=16)
        ax3[1].legend()

        plt.xticks(fontsize=11)  # X-axis tick font size
        plt.yticks(fontsize=11)  # Y-axis tick font size

        plt.tight_layout()
        plt.show()

        st.pyplot(fig3)

# 4th row    
with st.container():
    st.subheader('Clustering')

    tab1, tab2= st.tabs(["Distribution", "Clustering by Hour"])


    with tab1:
        # Plot for distribution of Hours
        #set figure size
        plt.figure(figsize=(12, 7))

        displot_fig = sns.displot(filtered_data, x='hour', hue='usage_cluster', kind='kde', fill=True)
        plt.title('Distribution of Hours', fontsize=16)
        plt.xlabel(' ')
        plt.ylabel('Frequency', fontsize=14)
        #plt.legend(loc='center')
        displot_fig._legend.set_bbox_to_anchor((0.95, 0.9))
        displot_fig._legend.set_loc('upper right')  
        plt.xticks(ticks=cluster['hour'].unique(), labels=hour_labels, rotation=90, fontsize=11)
        plt.yticks(fontsize=11)  # Y-axis tick font size

        # Add border (box) to the plot
        plt.gca().spines['top'].set_visible(True)
        plt.gca().spines['right'].set_visible(True)
        plt.gca().spines['left'].set_visible(True)
        plt.gca().spines['bottom'].set_visible(True)

        plt.tight_layout()
        plt.show()

        st.pyplot(displot_fig)
        with st.expander("Notes"):
            st.write("""
            *Clustering* yang digunakan pada tahap ini merupakan clustering sederhana dengan ketentuan. 
            Jika `hourly_users` kurang dari `0.5*avg_total_users` maka `usage_label = 'Low Usage'`. 
            Jika `hourly_users` di antara `0.5*avg_total_users` dan `1.5*avg_total_users` maka `usage_label = 'Medium'`. Jika tidak maka `usage_label = 'High Usage'`.
            
            """)

    with tab2:
        # Plot Avg. users hourly
        fig5, ax5 = plt.subplots(figsize=(12, 7))

        sns.lineplot(data=cluster, x='hour', y='total', marker='o', linewidth=3)
        ax5.set_title('Avg. Users Hourly', fontsize=16)
        ax5.set_xlabel(' ')
        ax5.set_ylabel('Number of Users', fontsize=14)
        ax5.set_xticks(ticks=cluster['hour'].unique(), labels=hour_labels, rotation=45)

        # Add border (box) to the plot
        plt.gca().spines['top'].set_visible(True)
        plt.gca().spines['right'].set_visible(True)
        plt.gca().spines['left'].set_visible(True)
        plt.gca().spines['bottom'].set_visible(True)

        # Menambahkan garis vertikal putus-putus di jam 5, 10, 15, dan 20
        plt.axvline(x=7, linestyle='--', color='red')
        plt.axvline(x=14, linestyle='--', color='red')
        plt.axvline(x=19, linestyle='--', color='red')

        # Adding annotation
        plt.text(x=1, y=450, s='Low Usage', fontsize=14, color='black')
        plt.text(x=8.5, y=450, s='Medium Usage', fontsize=14, color='black')
        plt.text(x=14.5, y=450, s='High Usage', fontsize=14, color='black')
        plt.text(x=19.5, y=450, s='Low Usage', fontsize=14, color='black')
        
        plt.xticks(fontsize=11)  # X-axis tick font size
        plt.yticks(fontsize=11)  # Y-axis tick font size
        
        plt.tight_layout()
        plt.show()

        st.pyplot(fig5)

st.caption('Copyright © den-rmdani 2024')

