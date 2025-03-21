import os
import google.generativeai as genai
from dotenv import load_dotenv
from weather import get_current_weather

load_dotenv()

# configuring gemini with api key
genai.configure(api_key=os.getenv("GEMINI_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="""
You are a friendly and fashion-savvy assistant who helps people decide what to wear based on the weather. 
Your responses should be clear, concise, and easy to read. 
Include specific clothing recommendations based on temperature and conditions, and offer helpful tips such as layering, accessory suggestions, or ways to stay comfortable.
Keep a warm and approachable tone throughout your response.
"""
)

def get_clothing_advice(city_name, description, temp_f, feels_like_f):
    """
    Sends the weather data to Gemini and returns a readable clothing recommendation.
    """
    chat_session = model.start_chat(history=[])

    prompt = (
        f"The weather in {city_name} is \"{description}\" with a temperature of {temp_f}°F "
        f"(feels like {feels_like_f}°F).\n"
        "What clothing should someone wear in this weather?\n"
        "Please provide a friendly, easy-to-read recommendation with helpful style or comfort tips."
    )

    response = chat_session.send_message(prompt)
    return response.text
