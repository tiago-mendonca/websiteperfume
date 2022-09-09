# import all necessary packages
import streamlit as st
import numpy as np
import random
import pandas as pd
import csv
import pickle

# put title etc.
st.title('Perfume')
st.header('Scent Selector')
st.subheader("Let's go!")



# read lists of olfactory notes
t = pd.read_csv('top_demo.csv', names = ["0"], header = None)
top = t["0"].tolist()

m = pd.read_csv('middle_demo.csv', names = ["0"], header = None)
middle = m["0"].tolist()

b = pd.read_csv('base_demo.csv', names = ["0"], header = None)
base = b["0"].tolist()



# create dataframes containing 0 for top, middle and base lists
input_top = pd.DataFrame(0, index=np.arange(1), columns=top)

input_middle = pd.DataFrame(0, index=np.arange(1), columns=middle)

input_base = pd.DataFrame(0, index=np.arange(1), columns=base)




## top notes

# create dictionary containing nice note names as key and official name as value
new_list_top_demo = []

for i in top:
    new_list_top_demo.append(i.split('_', )[0])

res_top = {}
for value in new_list_top_demo:
    for key in top:
        res_top[key] = value
        top.remove(key)
        break



# select top notes (on website) and store in variable
option_t = st.multiselect('Select the top notes or start typing to search specific note', [res_top[i] for i in res_top])



# get actual name from nice name using dictionary
notes_top = []

for x in option_t:
    notes_top.append([k for k, v in res_top.items() if v == x])

t_list = [item for sublist in notes_top for item in sublist]



# take actual name and loop through column names; replace 0 by corresponding value in dataframe
for y in input_top.columns:
    for z in t_list:
        if y in z:
            input_top[z] = 0.2


# just for visualisation, can get rid of it
st.text(input_top)




## middle notes

# create dictionary containing nice note names as key and official name as value

new_list_middle_demo = []

for i in middle:
    new_list_middle_demo.append(i.split('_', )[0])

res_middle = {}
for value in new_list_middle_demo:
    for key in middle:
        res_middle[key] = value
        middle.remove(key)
        break



# select top notes (on website) and store in variable
option_m = st.multiselect('Select the middle notes or start typing to search specific note', [res_middle[i] for i in res_middle])



# get actual name from nice name using dictionary
notes_middle = []

for a in option_m:
    notes_middle.append([k for k, v in res_middle.items() if v == a])

m_list = [item for sublist in notes_middle for item in sublist]



# take actual name and loop through column names; replace 0 by corresponding value in dataframe
for b in input_middle.columns:
    for c in m_list:
        if b in c:
            input_middle[c] = 0.7


# just for visualisation, can get rid of it
st.text(input_middle)




## base notes

# create dictionary containing nice note names as key and official name as value
new_list_base_demo = []

for i in base:
    new_list_base_demo.append(i.split('_', )[0])

res_base = {}
for value in new_list_base_demo:
    for key in base:
        res_base[key] = value
        base.remove(key)
        break




# select base notes (on website) and store in variable
option_b = st.multiselect('Select the base notes or start typing to search specific note', [res_base[i] for i in res_base])



# get actual name from nice name using dictionary
notes_base = []

for l in option_b:
    notes_base.append([k for k, v in res_base.items() if v == l])

b_list = [item for sublist in notes_base for item in sublist]



# take actual name and loop through column names; replace 0 by corresponding value in dataframe
for m in input_base.columns:
    for n in b_list:
        if m in n:
            input_base[n] = 0.1


# just for visualisation, can get rid of it
st.text(input_base)



# create X_new : concatenated dataframe of input top, middle and base
X_new = pd.concat([input_top, input_middle, input_base], axis = 1)



# just for visualisation, can get rid of it
st.text(X_new)


# use button to calculate success
test = st.button('Calculate Sucess')

if test:

    # load model
    model = pickle.load(open('test_model.pkl', 'rb'))


    # predict if perfume is a success or not
    if model.predict(X_new) == 1 and len(X_new.loc[~(X_new==0).all(axis=1)])!=0:
        st.markdown('Congrats! Your perfume is a SUCCESS.')

        st.balloons()
    elif len(X_new.loc[~(X_new==0).all(axis=1)])==0:

        st.error('Please imput some notes!', icon="🚨")


    else:
        st.markdown('Sorry, your perfume will not be successful. Try again!')


# try recall, precision etc. cannot find unsuccessful perfume
