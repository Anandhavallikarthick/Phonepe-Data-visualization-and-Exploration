
import pandas as pd
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
import time
import numpy as np




# Setting up page configuration
icon = Image.open(r"pheadd.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Anandhavalli Karthick",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Anandhavalli Karthick*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

# #To clone the Github Pulse repository use the following code
# Reference Syntax - Repo.clone_from("Clone Url", "Your working directory")

# Creating connection with mysql 
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use phonepe")


# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}}
                
    )
# MENU 1 - HOME
if selected == "Home":
    st.image("pheadd.png")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts,sunburst charts, Pie charts and Geo map visualization are used to get some insights.")
        st.markdown("### :violet[About :] This dashboard app is created by *Anandhavalli Karthick*! and The Data has been cloned from Phonepe Pulse Github Repositary.")
# Content in the second column (col2)
    with col2:
        st.image("/Users/karthickkumar/Desktop/phone pay project/earth.gif", caption='Data Visualization and Exploration', use_column_width=True)
        

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:

    
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
       

        # Query to fetch data from MySQL database
        query = f"SELECT states, Years, Quarter, SUM(Transaction_count) AS Transactions_Count, SUM(Transaction_amount) AS Total_Amount FROM aggregated_transaction WHERE years = {Year} AND quarter = {Quarter} GROUP BY states"
        mycursor.execute(query)
       # Creating Pandas DataFrame from SQL query result
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Years', 'Quarter', 'Transactions_Count', 'Total_Amount'])

# Rendering Markdown content with Streamlit
        st.markdown("### States vs Transaction")
        df['Total_Amount'] = pd.to_numeric(df['Total_Amount'], errors='coerce')

        # Plotting scatter plot using Plotly Express
        fig = px.scatter(df, x="Transactions_Count", y="Total_Amount", animation_frame="Years", animation_group="State",
                        color="State", hover_name="State", size="Total_Amount",
                        size_max=40, labels={"Transactions_Count": "Transactions Count", "Total_Amount": "Total Amount"})

        fig.update_layout(width=900)  # Adjust width as needed (in pixels)

        # Displaying the Plotly Express scatter plot with animation slider in Streamlit
        st.plotly_chart(fig, use_container_width=True)

   
        selected_year_1 = st.slider("Select Year 1", min_value=2018, max_value=2022, key="year_1")
        selected_quarter = st.slider("Select Quarter", min_value=1, max_value=4, key="quarter")
        
        col1,col2,col3 = st.columns([1,1,1],gap="small")

        
        
        with col1:
            st.markdown("### :violet[States]")
            mycursor.execute(f"select states, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from aggregated_transaction where years = {selected_year_1} and quarter = {selected_quarter} group by states order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[Districts]")
            mycursor.execute(f"select districts , sum(Transaction_Count) as Total_Count, sum(Transaction_Amount) as Total from map_transaction where years = {selected_year_1} and quarter = {selected_quarter} group by districts order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


        
        with col3:
            st.markdown("### :violet[Pincodes]")
            mycursor.execute(f"select pincodes, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_transaction where years = {selected_year_1} and quarter = {selected_quarter} group by pincodes order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

  

                

        
# Top Charts - USERS          
    if Type == "Users":

     
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
                
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select brands, sum(Transaction_count) as Total_Count, avg(percentage)*100 as Avg_Percentage from aggregated_user where years = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[Districts]")
            mycursor.execute(f"select districts, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by districts order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincodes]")
            mycursor.execute(f"select Pincodes, sum(RegisteredUser) as Total_Users from top_user where years = {Year} and quarter = {Quarter} group by Pincodes order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[States]")
            mycursor.execute(f"select states, sum(Registeredusers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by states order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_AppOpens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Users'],
                             labels={'Total_AppOpens':'Total_AppOpens'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


         #sunburst chart
        st.markdown("## :violet[Top 10 State and districts to explore more about Total_users]")
        mycursor.execute(f"select States, Districts,years,quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction group by States, Districts order by Total_Transactions desc limit 10")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        
        fig2 = px.sunburst(df1, path=['State', 'District', 'Total_Transactions'], 
                           values='Total_Transactions',
                           color='Total_Transactions',
                           color_continuous_scale=px.colors.sequential.Agsunset)
        fig2.update_layout(width=1500)  
        st.plotly_chart(fig2,use_container_width=True)
            

# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select states, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} group by states order by states")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            
            
          

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)



        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select states, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} group by states order by states")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)


# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from aggregated_transaction where years= {Year} and quarter = {Quarter} group by Transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
   


# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('Andaman & Nicobar Islands','andhra pradesh','arunachal pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','delhi','goa','gujarat','haryana',
                              'himachal pradesh','jammu & kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil nadu','telangana','tripura','uttar pradesh','uttarakhand','west bengal'),index=30)

        mycursor.execute(f"select States, Districts,years,quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} and States = '{selected_state}' group by States, Districts,years,quarter order by states,districts")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)



        # Execute SQL query to retrieve data
     
        mycursor.execute(f"select States, Districts,years,quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} and States = '{selected_state}' group by States, Districts,years,quarter order by Total_Transactions DESC limit 10")


        # Create DataFrame from SQL query result
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                        'Total_Transactions', 'Total_amount'])

        # Create Pie chart with Plotly Express (donut chart)
        fig2 = px.pie(df1, values='Total_Transactions', names='District', hole=0.4
                    )

        # Update layout (if needed)
        fig2.update_traces(textposition='inside', textinfo='percent+label')

        # Display the Plotly donut chart in Streamlit
        st.markdown("## :violet[Top 10 Districts by Total Transactions]")
        chart_width = 1500 
        st.plotly_chart(fig2, use_container_width=True)

        


# EXPLORE DATA - USERS      
    
    if Type == "Users":
       
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select states, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by states order by states")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                            ('Andaman & Nicobar','andhra pradesh','arunachal pradesh','assam','bihar',
                            'chandigarh','chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','delhi','goa','gujarat','haryana',
                            'himachal pradesh','jammu & kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                            'madhya pradesh','maharashtra','manipur','meghalaya','mizoram',
                            'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                            'tamil nadu','telangana','tripura','uttar pradesh','uttarakhand','west bengal'),index=30)

        mycursor.execute(f"select States,years,quarter,Districts,sum(Registeredusers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} and states = '{selected_state}' group by States, Districts,years,quarter order by states,districts")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                    title=selected_state,
                    x="District",
                    y="Total_Users",
                    orientation='v',
                    color='Total_Users',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

#sunburst chart
        st.markdown("## :violet[Select State and districts to explore more]")
        mycursor.execute(f"select States, Districts,years,quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} and States = '{selected_state}' group by States, Districts,years,quarter order by states,districts")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        
        fig2 = px.sunburst(df1, path=['State', 'District', 'Total_amount'], 
                           values='Total_amount',
                           color='Total_amount',
                           color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig2,use_container_width=True)


        st.markdown("## :violet[TOP 10 districts of Total_Amount]")
        mycursor.execute(f"select States, Districts,years,quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} and States = '{selected_state}' group by States, Districts,years,quarter order by states,districts limit 10")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        
        fig2 = px.pie(df1, names='District', 
                           values='Total_amount',
                             hole=0.4)
        st.plotly_chart(fig2,use_container_width=True)
        


# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/Anandhavallikarthick/Phonepe-Data-visualization-and-Exploration")
        st.write("**:violet[Image and content source]** ⬇️")
        st.write("https://www.prnewswire.com/in/news-releases/phonepe-launches-the-pulse-of-digital-payments-india-s-first-interactive-geospatial-website-888262738.html")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

    

        


            

            
            