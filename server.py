# Flask instance that is running server, main file for application
from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

# makes app a flask app
app = Flask(__name__)

# clothing recs function
def get_clothing_recs(temp_f, condition):
    tips = ""
    # Temperature-based logic (Fahrenheit thresholds)
    if temp_f < 32:
        tips += "Wear a heavy coat, scarf, gloves, and hat. "
    elif temp_f < 50:
        tips += "Wear a coat or thick jacket. "
    elif temp_f < 68:
        tips += "Wear a light jacket or sweater. "
    elif temp_f < 86:
        tips += "A T-shirt or light top is recommended. "
    else:
        tips += "Shorts and a tank top—stay cool! "

    # Condition-based logic
    condition_lower = condition.lower()
    if "rain" in condition_lower:
        tips += "Don't forget an umbrella or waterproof jacket. "
    elif "snow" in condition_lower:
        tips += "Wear warm boots and stay dry. "
    elif "drizzle" in condition_lower:
        tips += "A light waterproof jacket might be handy. "
    elif "thunderstorm" in condition_lower:
        tips += "Better to stay indoors until the storm passes. "

    return tips.strip()


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

    # Getting clothing tips
    clothing_tips = get_clothing_recs(temp_f, condition_main)


    return render_template(
        "weather.html",
        title=city_name,
        status=status_description,
        temp=f"{temp_f:.1f}",
        feels_like=f"{feels_like_f:.1f}",
        clothing_tips=clothing_tips
    )


# if being run out of this file
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)







