from flask import Flask, render_template, jsonify, request, abort
import json
import requests

app = Flask(__name__)

# Load attraction data from JSON file
with open('attractions.json') as f:
    attractions_data = json.load(f)

# OpenWeatherMap API key
API_KEY = '41fa41b89b49565da5dafd55ddd6a297'


def get_weather(city):
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'

    weather_response = requests.get(weather_url)
    forecast_response = requests.get(forecast_url)

    if weather_response.status_code == 200 and forecast_response.status_code == 200:
        weather_data = weather_response.json()
        forecast_data = forecast_response.json()

        current_weather = {
            'description': weather_data['weather'][0]['description'],
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed']
        }

        # Get the forecast for the next 5 time points
        forecast_list = forecast_data['list'][:5]
        forecast = [{'time': item['dt_txt'], 'temperature': item['main']['temp'],
                     'description': item['weather'][0]['description']} for item in forecast_list]

        return current_weather, forecast
    else:
        return None, None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/attractions')
def attractions():
    return render_template('attractions.html')


@app.route('/attraction/<attraction_id>')
def attraction(attraction_id):
    attraction_info = attractions_data.get(attraction_id)
    if attraction_info:
        city = attraction_info['title']
        current_weather, forecast = get_weather(city)
        if current_weather and forecast:
            return render_template('attraction.html', title=attraction_info['title'], image_url=attraction_info['image_url'], image_url2=attraction_info['image_url2'], description=attraction_info['description'], current_weather=current_weather, forecast=forecast)
        else:
            return render_template('attraction.html', title=attraction_info['title'], image_url=attraction_info['image_url'], image_url2=attraction_info['image_url2'], description=attraction_info['description'], current_weather=None, forecast=None)
    else:
        return "Attraction not found", 404

# API Endpoints


@app.route('/api/attractions', methods=['GET'])
def get_attractions():
    return jsonify(attractions_data)


@app.route('/api/attractions/<attraction_id>', methods=['GET'])
def get_attraction(attraction_id):
    attraction_info = attractions_data.get(attraction_id)
    if attraction_info:
        return jsonify(attraction_info)
    else:
        return abort(404, description="Attraction not found")


@app.route('/api/attractions', methods=['POST'])
def add_attraction():
    if not request.json or 'title' not in request.json:
        abort(400, description="Invalid request")
    new_id = str(len(attractions_data) + 1)
    new_attraction = {
        "title": request.json['title'],
        "image_url": request.json.get('image_url', ""),
        "image_url2": request.json.get('image_url2', ""),
        "description": request.json.get('description', ""),
        "weather": request.json.get('weather', ""),
        "forecast": request.json.get('forecast', "")
    }
    attractions_data[new_id] = new_attraction
    return jsonify(new_attraction), 201


@app.route('/api/attractions/<attraction_id>', methods=['PUT'])
def update_attraction(attraction_id):
    if attraction_id not in attractions_data:
        return abort(404, description="Attraction not found")
    if not request.json:
        abort(400, description="Invalid request")
    attraction = attractions_data[attraction_id]
    attraction['title'] = request.json.get('title', attraction['title'])
    attraction['image_url'] = request.json.get(
        'image_url', attraction['image_url'])
    attraction['image_url2'] = request.json.get(
        'image_url2', attraction['image_url2'])
    attraction['description'] = request.json.get(
        'description', attraction['description'])
    attraction['weather'] = request.json.get('weather', attraction['weather'])
    attraction['forecast'] = request.json.get(
        'forecast', attraction['forecast'])
    return jsonify(attraction)


@app.route('/api/attractions/<attraction_id>', methods=['DELETE'])
def delete_attraction(attraction_id):
    if attraction_id not in attractions_data:
        return abort(404, description="Attraction not found")
    del attractions_data[attraction_id]
    return '', 204


if __name__ == '__main__':
    app.run(debug=True, port=5001)
