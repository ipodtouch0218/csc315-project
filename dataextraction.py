""" This script reads the data from the 
various csv files in Data folder and writes
SQL queries into datainsertion.sqlto import 
data into database.
"""


#imported libraries
import numpy as np
import pandas as pd

with open("datainsertion.sql","w") as file:

    #putting Animal data into pandas DataFrame
    df = pd.read_csv("Data/Animal.csv")

    #selecting attributes of interest
    df = df.loc[:,["animal_id","sex","dam","status"]]
    
    #clean up data
    df = df.dropna(how='all')

    #write Animal data into datainserition.sql
    for i in df.index:
        file.write("INSERT INTO animal (animal_id, sex, dam, status) VALUES (")
        for j in df:
            file.write(str(df.loc[i,j]))
            if df.loc[i,j] not in ['Current','Dead','Sold']:
                file.write(',')
        file.write(");\n")

    #TO DO: write SessionAnimal data into datainsertion.sql
