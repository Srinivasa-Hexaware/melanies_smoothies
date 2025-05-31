# Import python packages
import requests
import streamlit as st
import snowflake.connector
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":tropical_drink: Customize Your Smoothie! :tropical_drink:")
st.write(
  """Choose the fruits you want in your custom smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name input on smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()             

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen+' '
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit Order')

    
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered {name_on_order}!', icon="✅")
