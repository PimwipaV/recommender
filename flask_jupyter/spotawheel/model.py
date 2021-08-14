import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# data ingestion
df = pd.read_csv('Spotawheel_case_study (1).csv')

# data preparation
df['Brand'] = df['Name'].str.split(' ').str[0]
df["Fueltype"]= df["Fuel_Type"].astype('category')
df["Fueltypecat"] = df["Fueltype"].cat.codes
df["Transmissiontype"]= df["Transmission"].astype('category')
df["Transmissiontypecat"] = df["Transmissiontype"].cat.codes
df["Brandtype"]= df["Brand"].astype('category')
df["Brandtypecat"] = df["Brandtype"].cat.codes

# data segregation train_test_split
x = df[["Mileage", "Kilometers_Driven", "Owner_Type","Fueltypecat", "Transmissiontypecat", "Brandtypecat", "Age", "Engine", "Seats", "Power"]].values
y = df["Price"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# train model and save as artifact
reg = LinearRegression().fit(x_train, y_train)

# take the saved model and predict
def predict(reg, user_input=None):
    proposed_buying_price = reg.predict(user_input)
    return proposed_buying_price