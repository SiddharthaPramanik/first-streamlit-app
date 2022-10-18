import pandas as pd
import requests
import snowflake.connector
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

# New section to display Fruityvice API Response
streamlit.header('Fruityvice Fruit Advice!')

# User input
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
streamlit.write('You entered', fruit_choice)
fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)

# Write json to screen
# streamlit.text(fruityvice_response.json())

# Take the json version of the reponse and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

# Write the normalized response to table on screen
streamlit.dataframe(fruityvice_normalized)

# Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)


