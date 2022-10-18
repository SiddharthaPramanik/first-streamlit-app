import pandas as pd
import requests
import snowflake.connector
import streamlit
from urllib.error import URLError

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

streamlit.header('View Our Fruit List - Add Your Favorites')

# Fruityvice Section

# Write function to fetch fruityvice data
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + this_fruit_choice)
  return pd.json_normalize(fruityvice_response.json())

try:
  # User input
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    # Write the normalized response to table on screen
    streamlit.dataframe(fruityvice_normalized)
except:
  streamlit.error()

# Snowflake Section

# Write a fucntion to fetch fruit_load_lisy
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()
  
# Write a function to add a fruit to the load_list
def add_fruit_to_load_list(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit

# Add a button to load the fruits
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

# Add a button to add fruit to the load list
add_my_fruit = streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add Fruit to List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  fruit_add_response = add_fruit_to_load_list(add_my_fruit)
  my_cnx.close()
  streamlit.text(fruit_add_response)


