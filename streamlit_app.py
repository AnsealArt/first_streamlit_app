import streamlit
import snowflake.connector

import pandas
import requests

# Snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])


streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


# New Section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# Take Fruityvice JSON and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Display normalized Fruityvice data
streamlit.dataframe(fruityvice_normalized)

# Get data from Snowflake
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()

streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Adding fruit
streamlit.text("What fruit would you like to add?")
add_my_fruit = ""
add_my_fruit = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
if not add_my_fruit == "" and len(add_my_fruit) > 0:
  my_cur.execute("INSERT INTO fruit_load_list VALUE ", add_my_fruit)
  streamlit.text("Thanks for adding " + "".join(add_my_fruit)) 

