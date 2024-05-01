
# Phonepe-Data-visualization-and-Exploration

The learning outcomes of this project:

Data extraction and processing: You will learn how to use Clone Github to extract data from a repository and pre-process the data using Python libraries such as Pandas.
Database management: You will learn how to use a relational database such as MySQL to store data and retrieve it efficiently for analysis and visualization.
Visualization and dashboard creation: You will learn how to use libraries such as Streamlit and Plotly to create interactive and visually appealing dashboards for data visualization.
Geo visualization: You will learn how to create and display data on a map using Plotly's built-in geo map functions.
Dynamic updating: You will learn how to create a dashboard that dynamically updates based on the latest data in a database.
Project development and deployment: You will learn how to develop a comprehensive and user-friendly solution, from data extraction to dashboard deployment. You will also learn how to test and deploy the solution to ensure it is secure, efficient, and user-friendly.




## Developer Guide

1.Tools

Visual Studio.
Python 3.12.0 or higher.
MySQL

2.Requirement Libraries to Install

pip install pandas numpy os json requests subprocess mysql.connector streamlit plotly.express
3.Import Libraries

clone libraries

import pandas as pd
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
import time
import numpy as np


4. E T L Process

a) Extract data

Initially, we Clone the data from the Phonepe GitHub repository by using Python libraries. https://github.com/PhonePe/pulse.git

b) Process and Transform the data

Process the clone data by using Python algorithms and transform the processed data into DataFrame format.

c) Load data

Finally, create a connection to the MySQL server and create a Database and stored the Transformed data in the MySQL server by using the given method. 

5. E D A Process and Frame work

a) Access MySQL DB

Create a connection to the MySQL server and access the specified MySQL DataBase

b) Filter the data

Filter and process the collected data depending on the given requirements by using SQL queries

c) Visualization

Finally, create a Dashboard by using Streamlit and applying selection and dropdown options on the Dashboard and show the output are Geo visualization, bar chart, and Dataframe Table
