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
)

def get_clothing_advice(city_name, description, temp_f, feels_like_f):
    """
    Sends the weather data to Google's Gemini (or PaLM) model and 
    returns clothing suggestions or other tips.
    """
    # Starting fresh chat session 
    chat_session = model.start_chat(history=[])

    # prompt with weather data
    prompt = f"""
The current weather in {city_name} is described as "{description}" with a temperature of {temp_f:.1f}°F (feels like {feels_like_f:.1f}°F).

In a short 1-2 sentence response, provide:
1) Appropriate clothing recommendations.
2) Additional helpful tips for dealing with these conditions.
"""

    response = chat_session.send_message(prompt)
    return response.text

