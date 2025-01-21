# Flask instance that is running server, main file for application
from flask import Flask, render_template, request
from weather import get_current_weather
from chat import get_clothing_advice
from waitress import serve

# makes app a flask app
app = Flask(__name__)

# defining routes that would be accessed on web
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # check for empty string or string w/only spaces
    if not bool(city.strip()):
        city = "Austin"

    weather_data = get_current_weather(city)

    # city is not found by api
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    # Extracting needed data from JSON
    city_name = weather_data["name"]
    status_description = weather_data["weather"][0]["description"].capitalize()
    temp_f = float(weather_data['main']['temp'])            # Fahrenheit
    feels_like_f = float(weather_data['main']['feels_like']) # Fahrenheit
    condition_main = weather_data['weather'][0]['main']     # e.g., "Rain", "Clear", etc.

    # Gemini method
    # Ask Gemini/PaLM for clothing advice
    gemini_response = get_clothing_advice(
        city_name=city_name,
        description=status_description,
        temp_f=temp_f,
        feels_like_f=feels_like_f
    )


    return render_template(
        "weather.html",
        title=city_name,
        status=status_description,
        temp=f"{temp_f:.1f}",
        feels_like=f"{feels_like_f:.1f}",
        clothing_tips=clothing_tips,
        gemini_response=gemini_response
    )


# if being run out of this file
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)







