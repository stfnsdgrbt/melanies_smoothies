# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd



# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """choose your fruits 
    """
)

import requests



name_on_order = st.text_input('name on Smoothie')
st.write('The name on youer smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
st.datafame(pd_df)
st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients'
                                 , my_dataframe
                                  , max_selections=5
                              )
ingredients_string= ''   
if ingredients_list:
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' Nutrition Information'
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        st_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
    st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order+ """' )"""
st.write(my_insert_stmt)
#st.stop()

time_to_insert = st.button('submit order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


