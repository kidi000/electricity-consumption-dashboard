import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
#from datetime import datetime

path_d= "C:/Users/kidist/Documents/python/daily_avg_data.csv"
path_w= "C:/Users/kidist/Documents/python/weekly_avg_data.csv"
path_m= "C:/Users/kidist/Documents/python/monthly_avg_data.csv"

df_daily= pd.read_csv(path_d)
df_weekly= pd.read_csv(path_w)
df_monthly= pd.read_csv(path_m)


df_daily['datetime'] = pd.to_datetime(df_daily['datetime'])
df_weekly['datetime'] = pd.to_datetime(df_weekly['datetime'])
df_monthly['datetime'] = pd.to_datetime(df_monthly['datetime'])

min_date = min(df_daily['datetime'].min(), df_weekly['datetime'].min(), df_monthly['datetime'].min())
max_date = max(df_daily['datetime'].max(), df_weekly['datetime'].max(), df_monthly['datetime'].max())



st.title('electricity consumption dashboard')



st.subheader(" Time Selecter ")
start_date= st.date_input("start time", value= min_date.date(), min_value= min_date.date(), max_value= max_date.date())
end_date= st.date_input("End time", value= max_date.date(), min_value= start_date, max_value= max_date.date())



st.subheader("summary")
starting_time = start_date.strftime("%Y-%m-%d")
ending_time = end_date.strftime("%Y-%m-%d")
st.write(f"Showing range:   **{starting_time}**  -  **{ending_time}**")


selected_days= df_daily[(df_daily['datetime'] >= pd.to_datetime(start_date)) &
                        (df_daily['datetime'] <= pd.to_datetime(end_date))]
total_kWh = (selected_days['kWh']).sum()
total_bill = round(((selected_days['hourlybill']).sum()) , 2)
avg_price = round(selected_days['Price'].mean(), 2)
avg_paidprice= round((total_bill / total_kWh)*100 , 2)



st.write(f" Total consumption over the period: **{total_kWh:.1f} kWh** ")
st.write(f" Total bill over the period : **{total_bill}€** ")
st.write(f" Average hourly price : **{avg_price} cents** ")
st.write(f" Average paid price : **{avg_paidprice} cents** ")


st.subheader("interval period ")
interval= st.selectbox( "averaging period", ("Daily", "Weekly", "Monthly"))

if interval == "Daily":
    df_select= df_daily [
        (df_daily['datetime'] >= pd.to_datetime(start_date)) & 
        (df_daily['datetime'] <= pd.to_datetime(end_date))
    ]
elif interval== "Weekly":
    df_select= df_weekly[
        (df_weekly['datetime'] >= pd.to_datetime(start_date)) & 
        (df_weekly['datetime'] <= pd.to_datetime(end_date))
    ]
else: 
    df_select= df_monthly[
        (df_monthly['datetime'] >= pd.to_datetime(start_date)) & 
        (df_monthly['datetime'] <= pd.to_datetime(end_date))
    ]
    

#plotting 

#plotting electricity consumption
fig1, kwh = plt.subplots(figsize=(12, 7))
kwh.plot(df_select['datetime'], df_select['kWh'] , color='red', linewidth=2)
kwh.set_ylabel('Electricity Consumption (kWh)')
kwh.set_xlabel('Time')
kwh.grid()
#kwh.set_title(f'{interval} Electricity Consumption')
st.pyplot(fig1)

#plotting electricity price
fig2, price = plt.subplots(figsize=(12, 7))
price.plot(df_select['datetime'], df_select['Price']*100, color='red', linewidth=2)
price.set_ylabel('Electricity Price (cents)')
price.set_xlabel('Time')
price.grid()
#price.set_title(f'{interval} Electricity price(cents)')
st.pyplot(fig2)


#plotting electricity bill(Euro)
fig3, bill = plt.subplots(figsize=(12, 7))
bill.plot(df_select['datetime'], df_select['hourlybill'], color='red', linewidth=2)
bill.set_ylabel('electricity bill (Euro)')
bill.set_xlabel('Time')
bill.grid()
#bill.set_title(f'{interval} electricity bill(Euro)')
st.pyplot(fig3)


#plotting Temperature
fig4, temp = plt.subplots(figsize=(12, 7))
temp.plot(df_select['datetime'], df_select['Temperature'], color='red', linewidth=2)
temp.set_ylabel('Temperature')
temp.set_xlabel('Time')
temp.grid()
#temp.set_title(f'{interval} Temperature')
st.pyplot(fig4)