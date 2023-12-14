import os
import json
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


#aggre transactions
path1="pulse/data/aggregated/transaction/country/india/state/"
agg_tran_list=os.listdir(path1)

columns1={"States":[],"Years":[], "Quarter":[],"Transaction_type":[], "Transaction_count":[], "Transaction_amount":[]}
for state in agg_tran_list:
    cur_states=path1+state+"/"
    if os.path.exists(cur_states) and os.path.isdir(cur_states):
        agg_year_list = os.listdir(cur_states)
        
        for year in agg_year_list:
            cur_year=cur_states+year+"/"
            if os.path.exists(cur_year) and os.path.isdir(cur_year):
                agg_file_list=os.listdir(cur_year)
                
                for file in agg_file_list:
                            cur_file=cur_year+file
                            data=open(cur_file,"r")
                            

                            A=json.load(data)
                            for i in A["data"]["transactionData"]:
                                name=i["name"]
                                count=i["paymentInstruments"][0]["count"]
                                amount=i["paymentInstruments"][0]["amount"]
                                columns1["Transaction_type"].append(name)
                                columns1["Transaction_count"].append(count)
                                columns1["Transaction_amount"].append(amount)
                                columns1["States"].append(state)
                                columns1["Years"].append(year)
                                columns1["Quarter"].append(int(file.strip(".json")))
                                

aggre_transaction=pd.DataFrame(columns1)
aggre_transaction["States"]=aggre_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
aggre_transaction["States"]=aggre_transaction["States"].str.replace("-"," ")
aggre_transaction["States"]=aggre_transaction["States"].str.title()
aggre_transaction["States"]=aggre_transaction["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
aggre_transaction



#aggregated user
path2="pulse/data/aggregated/user/country/india/state/"
agg_user_list=os.listdir(path2)

columns2={"States":[],"Years":[], "Brands":[],"Quarter":[], "Transaction_count":[], "Percentage":[]}

for state in agg_user_list:
    cur_states=path2+state+"/"
    agg_year_list = os.listdir(cur_states)
    
    for year in agg_year_list:
        cur_year=cur_states+year+"/"
        agg_file_list=os.listdir(cur_year)
        
        for file in agg_file_list:
                    cur_file=cur_year+file
                    data=open(cur_file,"r")
                    
                    B=json.load(data)
                    
                    try:
                        for i in B["data"]["usersByDevice"]:
                            brand=i["brand"]
                            count=i["count"]
                            percentage=i["percentage"]
                            columns2["Brands"].append(brand)
                            columns2["Transaction_count"].append(count)
                            columns2["Percentage"].append(percentage)
                            columns2["States"].append(state)
                            columns2["Years"].append(year)
                            columns2["Quarter"].append(int(file.strip(".json")))
                    except:
                        pass
                    
aggre_user=pd.DataFrame(columns2)
aggre_user["States"]=aggre_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
aggre_user["States"]=aggre_user["States"].str.replace("-"," ")
aggre_user["States"]=aggre_user["States"].str.title()
aggre_user["States"]=aggre_user["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
aggre_user



#map_transaction
path3="pulse/data/map/transaction/hover/country/india/state/"
map_tran_list=os.listdir(path3)

columns3={"States":[],"Years":[], "Quarter":[],"Districts":[], "Transaction_count":[], "Transaction_amount":[]}
for state in  map_tran_list:
    cur_states=path3+state+"/"
    if os.path.exists(cur_states) and os.path.isdir(cur_states):
        agg_year_list = os.listdir(cur_states)
    
        for year in agg_year_list:
            cur_year=cur_states+year+"/"
            if os.path.exists(cur_year) and os.path.isdir(cur_year):
                agg_file_list=os.listdir(cur_year)
                

                for file in agg_file_list:
                    cur_file=cur_year+file
                    data=open(cur_file,"r")
                    

                    C=json.load(data)
                    for i in C["data"]["hoverDataList"]:
                        name=i["name"]
                        count=i["metric"][0]["count"]
                        amount=i["metric"][0]["amount"]
                        columns3["Districts"].append(name)
                        columns3["Transaction_count"].append(count)
                        columns3["Transaction_amount"].append(amount)
                        columns3["States"].append(state)
                        columns3["Years"].append(year)
                        columns3["Quarter"].append(int(file.strip(".json")))

map_tran=pd.DataFrame(columns3)
map_tran["States"]=map_tran["States"].str.replace("andaman-&_nicobar-islands","Andaman & Nicobar")
map_tran["States"]=map_tran["States"].str.replace("-"," ")
map_tran["States"]=map_tran["States"].str.title()
map_tran["States"]=map_tran["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")


#map_user
path4="pulse/data/map/user/hover/country/india/state/"
map_user_list=os.listdir(path4)

columns4={"States":[],"Years":[], "Quarter":[],"Districts":[], "RegisteredUsers":[], "AppOpens":[]}
for state in  map_user_list:
    cur_states=path4+state+"/"
    if os.path.exists(cur_states) and os.path.isdir(cur_states):
        agg_year_list = os.listdir(cur_states)
    
        for year in agg_year_list:
            cur_year=cur_states+year+"/"
            if os.path.exists(cur_year) and os.path.isdir(cur_year):
                agg_file_list=os.listdir(cur_year)
                

                for file in agg_file_list:
                    cur_file=cur_year+file
                    data=open(cur_file,"r")
                    

                    D=json.load(data)
                    for i in D["data"]["hoverData"].items():
                        district=i[0]
                        registeredUsers=i[1]["registeredUsers"]
                        appOpens=i[1]["appOpens"]
                        columns4["Districts"].append(district)
                        columns4["RegisteredUsers"].append(registeredUsers)
                        columns4["AppOpens"].append(appOpens)
                        columns4["States"].append(state)
                        columns4["Years"].append(year)
                        columns4["Quarter"].append(int(file.strip(".json")))


map_user=pd.DataFrame(columns4)
map_user["States"] = map_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
map_user["States"] = map_user["States"].str.replace("-"," ")
map_user["States"] = map_user["States"].str.title()
map_user['States'] = map_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")


#Top Transaction
path5="pulse/data/top/transaction/country/india/state/"
top_tran_list=os.listdir(path5)

columns5={"States":[],"Years":[], "Quarter":[],"Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}
for state in  top_tran_list:
    cur_states=path5+state+"/"
    if os.path.exists(cur_states) and os.path.isdir(cur_states):
        top_year_list = os.listdir(cur_states)
    
        for year in top_year_list:
            cur_years=cur_states+year+"/"
            if os.path.exists(cur_years) and os.path.isdir(cur_years):
                top_file_list=os.listdir(cur_years)
                

                for file in top_file_list:
                    cur_file=cur_years+file
                    data=open(cur_file,"r")
                    
                    E=json.load(data)
                    for i in E["data"]["pincodes"]:
                        entityName=i["entityName"]
                        count=i["metric"]["count"]
                        amount=i["metric"]["amount"]
                        columns5["Pincodes"].append(entityName)
                        columns5["Transaction_amount"].append(amount)
                        columns5["Transaction_count"].append(count)
                        columns5["States"].append(state)
                        columns5["Years"].append(year)
                        columns5["Quarter"].append(int(file.strip(".json")))


                    
top_transaction=pd.DataFrame(columns5)
top_transaction["States"] = top_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
top_transaction["States"] = top_transaction["States"].str.replace("-"," ")
top_transaction["States"] = top_transaction["States"].str.title()
top_transaction['States'] = top_transaction['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")




# top_user
path6="pulse/data/top/user/country/india/state/"
top_user_list=os.listdir(path6)

columns6={"States":[], "Years":[], "Quarter":[],"Pincodes":[],"RegisteredUser":[]}

for state in top_user_list:
    cur_states=path6+state+"/"
    top_year_list=os.listdir(cur_states)

    for year in top_year_list:
        cur_years=cur_states+year+"/"
        top_file_list=os.listdir(cur_years)


        for file in top_file_list:
            cur_files=cur_years+file
            data=open(cur_files,"r")

            F=json.load(data)

            for i in F["data"]["pincodes"]:
                name=i["name"]
                registeredusers=i["registeredUsers"]
                columns6["Pincodes"].append(name)
                columns6["RegisteredUser"].append(registeredusers)
                columns6["States"].append(state)
                columns6["Years"].append(year)
                columns6["Quarter"].append(int(file.strip(".json")))

top_user=pd.DataFrame(columns6)
top_user["States"] = top_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
top_user["States"] = top_user["States"].str.replace("-"," ")
top_user["States"] = top_user["States"].str.title()
top_user['States'] = top_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")




# transfer to SQL aggre_transaction
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use phonepe")


create_query1='''create table if not exists aggregated_transaction (States varchar(150),Years int,Quarter int,Transaction_type varchar(150),Transaction_count bigint,Transaction_amount bigint)'''
mycursor.execute(create_query1)
mydb.commit()


for index,row in aggre_transaction.iterrows():
    insert_query1='''insert into aggregated_transaction (States,Years,Quarter,Transaction_type,Transaction_count,Transaction_amount)values(%s,%s,%s,%s,%s,%s)'''
    values=(row["States"],row["Years"],row["Quarter"],row["Transaction_type"],row["Transaction_count"],row["Transaction_amount"])
    mycursor.execute(insert_query1,values)
    mydb.commit()





    #aggre_user
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use phonepe")

create_query2='''create table if not exists aggregated_user (States varchar(100),Years int,Brands varchar(100),Quarter int,Transaction_count bigint,Percentage varchar(50))'''
mycursor.execute(create_query2)
mydb.commit()

for index,row in aggre_user.iterrows():
    insert_query2='''insert into aggregated_user(States,Years,Brands,Quarter,Transaction_count,Percentage)values(%s,%s,%s,%s,%s,%s)'''
    values=(row["States"],row["Years"],row["Brands"],row["Quarter"],row["Transaction_count"],row["Percentage"])


    mycursor.execute(insert_query2,values)
    mydb.commit()


    #map_tran
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use phonepe")
drop_query='''drop table if exists map_transaction'''
mycursor.execute(drop_query)
mydb.commit()

create_query3='''create table if not exists map_transaction(States varchar(100),Years int,Quarter int,Districts varchar(100),Transaction_count bigint,Transaction_amount bigint)'''
mycursor.execute(create_query3)
mydb.commit()


for index,row in map_tran.iterrows():
    insert_query3='''insert into map_transaction(States,Years,Quarter,Districts,Transaction_count,Transaction_amount)values(%s,%s,%s,%s,%s,%s)'''
    values=(row["States"],row["Years"],row["Quarter"],row["Districts"],row["Transaction_count"],row["Transaction_amount"])

    mycursor.execute(insert_query3,values)
    mydb.commit()



    #map_user
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use phonepe")


create_query4='''create table if not exists map_user(States varchar(100),Years int,Quarter int,Districts varchar(100),RegisteredUsers int,AppOpens bigint)'''
mycursor.execute(create_query4)
mydb.commit()

for index,row in map_user.iterrows():
    insert_query4='''insert into map_user(States,Years,Quarter,Districts,RegisteredUsers,AppOpens)values(%s,%s,%s,%s,%s,%s)'''
    values=(row["States"],row["Years"],row["Quarter"],row["Districts"],row["RegisteredUsers"],row["AppOpens"])

    mycursor.execute(insert_query4,values)
    mydb.commit()





    #top_transaction


import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use phonepe")

create_query5='''create table if not exists top_transaction(States varchar(100),Years int,Quarter int,Pincodes int,Transaction_count bigint,Transaction_amount bigint)'''
mycursor.execute(create_query5)
mydb.commit()


for index,row in top_transaction.iterrows():
    insert_query5='''insert into top_transaction(States,Years,Quarter,Pincodes,Transaction_count,Transaction_amount)values(%s,%s,%s,%s,%s,%s)'''
    values=(row["States"],row["Years"],row["Quarter"],row["Pincodes"],row["Transaction_count"],row["Transaction_amount"])

    mycursor.execute(insert_query5,values)
    mydb.commit()





    #top_user
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use phonepe")


create_query6='''create table if not exists top_user (States varchar(100),Years int,Quarter int,Pincodes int,RegisteredUser int)'''
mycursor.execute(create_query6)
mydb.commit()

for index,row in top_user.iterrows():
    insert_query6='''insert into top_user (States,Years,Quarter,Pincodes,RegisteredUser)values(%s,%s,%s,%s,%s)'''
    values=(row["States"],row["Years"],row["Quarter"],row["Pincodes"],row["RegisteredUser"])
    mycursor.execute(insert_query6,values)
    mydb.commit()






    
