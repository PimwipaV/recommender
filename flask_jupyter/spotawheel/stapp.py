import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

st.title("You're selling your car")
st.subheader("Let's calculate how much you will make from it")

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
#st.write(df)

# this section takes user input as x_test
brandchoose = st.selectbox(
    'What brand is your car?',
     df['Brand'].unique())
#have to map it back to brandtypecat
b = dict(enumerate(df["Brandtype"].cat.categories))
reversed_b = dict(map(reversed, b.items()))
brand = reversed_b[brandchoose]

transmissionchoose = st.selectbox(
    'Is it manual or automatic?',
     df['Transmissiontype'].unique())
t = dict(enumerate(df["Transmissiontype"].cat.categories))
reversed_t = dict(map(reversed, t.items()))
transmission = reversed_t[transmissionchoose]

age = st.text_input("How many years old is it?", 5)
mileage = st.text_input("How much is the mileage?", 10)
kilometers = st.text_input("How many kilometers has it been driven?", 50000)
owner = st.selectbox(
    'How many owners it has had?',
    df['Owner_Type'].unique())

fuelchoose = st.selectbox(
    'What type of fuel it uses?',
    df['Fuel_Type'].unique())
f = dict(enumerate(df["Fueltype"].cat.categories))
reversed_f = dict(map(reversed, f.items()))
fuel = reversed_f[fuelchoose]
engine = st.text_input("How big is the engine?", 1500)
power = st.text_input("How much power it has?", 100)
seats = st.text_input("How many seats has it?", 5)

# data segregation train_test_split
x = df[["Mileage", "Kilometers_Driven", "Owner_Type","Fueltypecat", "Transmissiontypecat", "Brandtypecat", "Age", "Engine", "Seats", "Power"]].values
y = df["Price"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# train model and save as artifact
reg = LinearRegression().fit(x_train, y_train)

# take the saved model and predict
user_input = [mileage, kilometers, owner, fuel, transmission, brand, age, engine, seats, power]
st.write(user_input)
user_input1 = np.array(user_input).reshape(1,10)
dummy = np.array([10, 40000,1, 0, 1, 10, 8, 2000, 5, 100]).reshape(1,10)
proposed_buying_price = reg.predict(user_input1)
st.write('You should get approximately this much')
st.write(proposed_buying_price)
