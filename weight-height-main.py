import streamlit as st
import openai
from fpdf import FPDF
import base64


pdf = FPDF()  # pdf object
pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_page()
pdf.set_font("Arial", size = 15)
pdf.set_xy(10.0, 20)



# Set the OpenAI API key
openai.api_key = st.secrets["OPENAI"]

st.title("Personalized Diet Plan Generator")
st.write("""
This application generates a personalized diet plan for you based on your age, height, weight, gender, and other factors. 
Please fill in the information below and click 'Generate Diet Plan'.
""")

# Create two columns for inputs
col1, col2 = st.columns(2)

# Create input fields for age and height
age = col1.number_input('Enter your age', min_value=1, max_value=100)

with col1:
    colh1 , colh2 = st.columns(2)
    height_feet = colh1.number_input('Enter your height in ft', min_value=0.0, max_value=10.0)
    height_inches = colh2.number_input('Enter your height in inches', min_value=0.0, max_value=12.0, step = 0.01)
# height = col1.number_input('Enter your height in ft', min_value=0.0, max_value=10.0, step = 0.01)

weight = col1.number_input('Enter your weight in lbs', min_value=1, max_value=2000)

# Create input fields for gender, goal weight and cooking skill level
gender = col2.selectbox('Select your gender', ('Male', 'Female', 'Other'))
cooking_skill = col2.selectbox('Select your cooking skill level', ('Beginner', 'Intermediate', 'Expert'))
goal_weight = col2.number_input('Enter your goal weight in lbs', min_value=1, max_value=2000)

# Create input fields for dietary preferences, allergies, and health conditions

dietary_pref = st.text_input('Enter any dietary preferences / Allergies / Health Conditions (optional)')
# allergies = st.text_input('Enter any allergies (optional)')
# health_conditions = st.text_input('Enter any health conditions (optional)')

# Create a button that the user can click to generate a diet plan
if st.button('Generate Diet Plan'):
    # Create the prompt
    prompt = f"""I want you to be a diet coach. I will give you several aspects of a person and I want you to make a weekly diet plan for them. Make it as detailed as possible. It should also tell the time it would take to reach the goal weight. Format it like a professional and customized diet plan.
            Here are the details:
            Age : {age}
            Current Weight : {weight} lbs,
            Goal Weight : {goal_weight} lbs,
            Height : {height_feet, height_inches} ft,
            Gender : {gender}
            Cooking Skills : {cooking_skill}
            Dietry Preferances : {dietary_pref}
            -------------------"""

    # Send the prompt to the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2500
    )

    # model = "gpt-3.5-turbo"
    # response = openai.ChatCompletion.create(
    # model=model,
    # messages=prompt,
    # temperature=0,
    # )

    # Display the response
    diet_plan = response.choices[0].text.strip()
    st.text(diet_plan)

    # pdf.multi_cell(0, 10, diet_plan)

    # st.download_button(
    # "Download Plan",
    # data=pdf.output(dest='S').encode('iso-8859-15'),
    # file_name="Output.pdf",
    # )

    text_contents = diet_plan
    st.download_button('Download Diet Plan', text_contents)
