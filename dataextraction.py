""" This script reads the data from the 
various csv files in Data folder and writes
SQL queries into datainsertion.sqlto import 
data into database.
"""


#imported libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

with open("datainsertion.sql","w") as file:
    
    #putting Animal data into pandas DataFrame
    df = pd.read_csv("Data/Animal.csv")

    #selecting attributes of interest
    df = df.loc[:,["animal_id","sex","dam","status"]]
    
    #clean up data
    df = df.dropna(how='all')
    df = df.drop_duplicates()
    
    #write Animal data into datainserition.sql
    for i in df.index:
        file.write("INSERT INTO animal (animal_id, sex, dam, status) VALUES (")
        for j in df:
            file.write(str(df.loc[i,j]))
            if df.loc[i,j] not in ['Current','Dead','Sold']:
                file.write(',')
        file.write(");\n")
    
    #putting SessionAnimalTrait data into pandas DataFrame
    df2 = pd.read_csv("Data/SessionAnimalTrait.csv")

    #selecting attributes of interest
    df2 = df2.loc[:,["session_id","animal_id","trait_code","alpha_value"]]

    #selecting tuples of interest
    """
    357 = BWT,
    469 = Dam Observations,
    475 = Dam Milk, 
    479 = Kid Ease,
    486 = Num of Kids
    501 = AUS Mother Score
    935 = Mother
    """
    df2 = df2.loc[df2["trait_code"].isin([357,469,475,479,486,501,935]),:]

    #dropping any tuples that have no value/score for their trait code
    df2 = df2.dropna(subset = ["alpha_value"])
    df2 = df2.drop_duplicates(subset = ["session_id","animal_id","trait_code"])
    df2 = df2.sort_values(["session_id","animal_id"])
    
    #dropping duplicates, giving an "index" for pivot
    sessions = df2[["session_id","animal_id"]].drop_duplicates()

    #created pivot
    data = df2.pivot(index = ['session_id','animal_id'], columns = 'trait_code', values = 'alpha_value')

    print(data, data.iloc[0,0], list(data.index[0]), sep = '\n')

    for i in range(0,len(data.index)):
        file.write("""INSERT INTO session_animal (session_id, animal_id, birth_weight, observations, milk_rating, 
        kid_ease, num_of_kids, mother_score, mothering) VALUES (""")
        #print()
        for k in list(data.index[i]):
            file.write(str(k))
            file.write(',')
        for j in range(len(data.iloc[i,:])):
            file.write(str(data.iloc[i,j]))
            if(j != (len(data.iloc[i,:]))-1):
                file.write(",")
        file.write(");\n")



    #FAILED ATTEMPT #1
    """
    #print(list(df2.loc[0,["session_id","animal_id"]]))
    #print(df2.loc[0].trait_code)

    rows = (df2.loc[0,["session_id","animal_id"]]) == (sessions.loc[0])
    print(rows)
    
    for row in sessions.index:
        a,b,c,d,e,f,g = None,None,None,None,None,None,None
        
        rows = df2[df2.loc[row,["session_id","animal_id"]] == sessions.loc[row]]
        #rows = (df2.loc[row2] for row2 in df2.index if list(df2.loc[row2,["session_id","animal_id"]]) == list(sessions.loc[row,:]))
        print(rows)
        
        for row2 in rows:
            if row2.trait_code == 357:
                print(row2.trait_code)
                a = row2.alpha_value
            elif row2.trait_code == 469:
                print(row2.trait_code)
                b = row2.alpha_value
            elif row2.trait_code == 475:
                print(row2.trait_code)
                c = row2.alpha_value
            elif row2.trait_code == 479:
                print(row2.trait_code)
                d = row2.alpha_value
            elif row2.trait_code == 486:
                print(row2.trait_code)
                e = row2.alpha_value
            elif row2.trait_code == 501:
                print(row2.trait_code)
                f = row2.alpha_value
            elif row2.trait_code == 935:
                print(row2.trait_code)
                g = row2.alpha_value
    
    print("INSERT INTO session_dam (session_id, animal_id, birth_weight, observations, milk_rating, kid_ease, num_of_kids, mother_score, mothering) VALUES ")
    print(a,b,c,d,e,f,g)
    """
    #FAILED ATTEMPT #2
    """
    data = {"session_id": sessions.loc[:,"session_id"],
                    "animal_id": sessions.loc[:,"animal_id"],
                    "birth_weight": None,
                    "observations": None,
                    "milk_rating": None,
                    "kid_ease": None,
                    "num_of_kids": None,
                    "mother_score": None,
                    "mothering": None}

    datatoinsert = pd.DataFrame(data)
    print(datatoinsert)
    
    for row in df2.index:
        if df2.loc[row].trait_code == 357:
            datatoinsert.loc[df2.loc[row,""], "birth_weight"] = df2.loc[row].alpha_value
        elif df2.loc[row].trait_code == 469:
            datatoinsert.loc[row, "observations"] = df2.loc[row].alpha_value
        elif df2.loc[row].trait_code == 475:
            datatoinsert.loc[row, "milk_rating"] = df2.loc[row].alpha_value
        elif df2.loc[row].trait_code == 479:
            datatoinsert.loc[row, "kid_ease"] = df2.loc[row].alpha_value
        elif df2.loc[row].trait_code == 486:
            datatoinsert.loc[row, "num_of_kids"] = df2.loc[row].alpha_value
        elif df2.loc[row].trait_code == 501:
            datatoinsert.loc[row, "mother_score"] = df2.loc[row].alpha_value
        elif df2.loc[row].trait_code == 935:
            datatoinsert.loc[row, "mothering"] = df2.loc[row].alpha_value
    """