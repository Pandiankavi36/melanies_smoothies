# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)
#option = st.selectbox(
 #   'What is your favorite fruit?',
  #  ('Banana','Strawberries','Peaches','Apples','Grapes'))

#st.write('Your favorite fruit is:', option)

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be :', name_on_order)

#Display the Fruit Options List in Your Streamlit in Snowflake (SiS) App. 

cnx = st.connection("snowflake")
session =  cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data= my_dataframe, use_container_width=True)
#st.stop()

#Convert the snowpark Datafarme to a Pandas Dataframe so we can use the LOC Function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredinets_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredinets_list:
    #st.write(ingredinets_list)
    #st.text(ingredinets_list)

    ingredients_string = ''

    for fruit_chosen in ingredinets_list:
        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ' , search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutriton Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st_df =  st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +"""')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!",  icon="✅")




    
