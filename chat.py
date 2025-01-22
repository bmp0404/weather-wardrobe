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
  system_instruction="""You are a helpful, fashion-savvy assistant. 
Your primary goal is to begin your response with a single, short sentence listing only the recommended clothing items. 
The first sentence must:
1) List heavier/main garments first (e.g., coats, jackets, pants).
2) List lesser items/accessories last (e.g., hats, scarves, gloves).
3) Not exceed 10 words.
4) Use only commas for separation (no additional words or punctuation).
After this first sentence, you may provide further recommendations in subsequent sentences.
"""
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
The weather in {city_name} is "{description}" with {temp_f}°F (feels like {feels_like_f}°F). 
In your response:
1) Begin with a single sentence listing heavier clothing items first and accessories last, separated only by commas.
2) Keep it under 10 words (e.g., “Coat, jacket, pants, hat”).
3) Provide any extra advice or detail in subsequent sentences only.

"""

    response = chat_session.send_message(prompt)
    return response.text

