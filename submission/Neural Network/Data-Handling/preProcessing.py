# This script was applied to every data set for each participating
# Eliminate NAN Values which are hard to handle by the neural network
# Creates a NAN row at the end of the DF 
# NAN row is used to interpolate BETWEEN DFs 


import pandas as pd
import numpy as np
from numpy import nan as Nan


#Define data set here

df = pd.read_csv(r"DATA_SET_TO_READ", header=None)


# Removig ID, TaskID, FRAME_Number, TIMESTAMP
# Removing Fingers
df = df.drop(df.columns[0:4], axis=1)
df = df.drop(df.columns[88:], axis=1)
# Removing head
df = df.iloc[1:]



# Iter over df to find NAN values
for index, row in df.iterrows():
    try:
        if(index<len(df.index)):
            this_row = int(df.iloc[index].iloc[0])
            next_row = int(df.iloc[index+1].iloc[0])
            #print("This row: ", this_row)
            #print("Next row: ", next_row)

            if(this_row+1 != next_row): 
                print("Missing frame: ", this_row+1)
    except:
        print("End of df")


# Convert df to numeric
# Interpolate missing values
df = df.convert_objects(convert_numeric=True)
df = df.interpolate(method='linear', limit_direction='forward', axis=0)


# Append NAN row to end of df 
# Used for concatinating dfs
s = pd.Series(Nan, df.columns)
f = lambda d: d.append(s, ignore_index=True)

df = df.append(s, ignore_index=True)