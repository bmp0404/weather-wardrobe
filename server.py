from flask import Flask, render_template, request
from weather import get_current_weather
from chat import get_clothing_advice
from image import fetch_outfit_images
from waitress import serve

app = Flask(__name__)

def outfit_query(temp_f, condition):
    cond_lower = condition.lower()
    if "snow" in cond_lower:
        return "winter coat gloves"
    if "rain" in cond_lower:
        return "rain jacket umbrella"

    if temp_f < 50:
        return "heavy coat"
    elif temp_f < 70:
        return "light jacket sweater"
    elif temp_f < 85:
        return "t-shirt jeans"
    else:
        return "shorts and tank top"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city', "").strip()
    if not city:
        city = "Austin"

    # Fetch weather data
    weather_data = get_current_weather(city)
    if weather_data.get('cod') != 200:
        return render_template('city-not-found.html')

    # Extract needed info
    city_name = weather_data["name"]
    status_description = weather_data["weather"][0]["description"].capitalize()
    temp_f = float(weather_data['main']['temp'])
    feels_like_f = float(weather_data['main']['feels_like'])

    # Ask Gemini AI
    gemini_response = get_clothing_advice(
        city_name=city_name,
        description=status_description,
        temp_f=temp_f,
        feels_like_f=feels_like_f
    )

    # Build an Unsplash query & fetch up to 3 images
    user_query = outfit_query(temp_f, status_description)
    image_urls = fetch_outfit_images(user_query)  # returns a list of up to 3 URLs

    # 5) Render the template
    return render_template(
        "weather.html",
        title=city_name,
        status=status_description,
        temp=f"{temp_f:.1f}",
        feels_like=f"{feels_like_f:.1f}",
        gemini_response=gemini_response,
        outfit_pictures=image_urls  # pass the list to the template
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
