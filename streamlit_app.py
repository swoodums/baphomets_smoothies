# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Tantalus' Tantalizations :cup_with_straw:")
st.write(
  """Fresh from the frozen-over fields of Tartarus!
  You won't need to bend or reach to get these frozen treats!
  """
)

session = get_active_session()
fruit_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name_on_order = st.text_input('Label yourself, heretic.')
st.write('The condemned is called:', name_on_order)

ingredient_list = st.multiselect(
    'Choose your devilish delights.  The gods will not allow more than five fruits.',
    fruit_dataframe,
    max_selections=5
)

if ingredient_list:
    ingredients_string = ''     # initialize empty string
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '      # append item with space between

    insert_statement = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    # st.write(insert_statement)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(insert_statement).collect()

        st.success('The Earth groans as it accepts the blood sacrifice for ' + name_on_order, icon="✅")