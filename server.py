# Flask instance that is running server, main file for application
from flask import Flask, render_template, request
from weather import get_current_weather
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

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )


# if being run out of this file
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)

