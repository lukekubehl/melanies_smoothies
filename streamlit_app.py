# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title('🥤 Customize Your Smoothie! 🥤')
st.write("Choose the fruits you want in your custom Smoothie!")

# --- Step 1: Get name from user
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# --- Step 2: Fetch fruit options from Snowflake
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# --- Step 3: Let user choose fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# --- Step 4: Build SQL insert string
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    # --- Step 5: Button to confirm order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
