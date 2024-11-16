from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the generative AI library by providing API key
genai.configure(api_key=os.getenv("API_KEY"))

# Function to load Google Gemini 1.5 Flash API and get a response
def get_gemini_response(input_text, image):
    try:
        # Initialize the Generative Model with the new model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate the content
        response = model.generate_content([input_text, image[0]])
        
        # Access the text attribute from the response
        return response.text  # Correct way to access the response text
    except Exception as e:
        return f"Error generating response: {e}"

# Function to set up the input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        # Prepare image data for the API
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="WellnessAI Advisor")

st.header("WellnessAI Advisor 👨‍⚕️")
uploaded_file = st.file_uploader("Choose an image..", type=["jpg", "jpeg", "png"])
image = ""

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to submit the image and input prompt
submit = st.button("Tell me about my meal")

# Input prompt for the nutrition analysis
# Input prompt for the nutrition analysis with improved structure
input_prompt = """
You are an expert nutritionist. Look at the food items from the image, and calculate the total calories. 
Provide the details of every food item with calorie intake in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----

After that, mention whether the meal is healthy or not. Also, include the percentage split of carbohydrates, proteins, fats, sugar, and calories in the meal.

Next, provide suggestions on the following points:
1. Which item should be removed from the meal, if any.
2. Which item should be added to make the meal healthier, if necessary.

Finally, give recommendations to balance the nutrients better if the meal is not fully balanced.
"""

# Rest of the code remains unchanged


# If submit button is clicked
if submit:
    if uploaded_file is not None:
        # Prepare image data for the API
        image_data = input_image_setup(uploaded_file)

        # Get the response from the Gemini 1.5 Flash model
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.error("Please upload an image before submitting.")
