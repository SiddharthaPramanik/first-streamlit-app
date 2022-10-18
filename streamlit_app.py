import pandas as pd
import requests
import streamlit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.text('Avocado Toast')

streamlit.header('Build Your Own Fruit Smoothie')
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

# Fruityvice API
streamlit.header('Fruityvice Fruit Advice!')
fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + 'kiwi')

# Write json to screen
# streamlit.text(fruityvice_response.json())

# Take the json version of the reponse and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

# Write the normalized response to table on screen
streamlit.dataframe(fruityvice_normalized)


