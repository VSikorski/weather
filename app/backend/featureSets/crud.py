from flask import jsonify, request, Response
from datetime import datetime
from projectFiles import db
from projectFiles.data import WeatherData
from projectFiles.utils import snake_case_to_name
from io import StringIO
import csv
from sqlalchemy import func

# endpoint to test the connection
def welcome():
    if 'text/csv' in request.headers.get('Accept', ''):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["message"])
        writer.writerow(["Welcome to the Weather App API!"])
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={"Content-Disposition": "inline"},
            status=200
        )
    return jsonify({"message": "Welcome to the Weather App API!"}), 200

def get_weather_data_id():
    city_name = request.args.get('city_name')
    if city_name is None:
        return jsonify({"error": "city_name is a required parameter"}), 400

    date_time = request.args.get('date_time')
    if date_time is None:
        return jsonify({"error": "date_time is a required parameter"}), 400

    # replacing the underscore with space for correct processing
    date_time = date_time.replace('_', ' ')

    try:
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid time format. Use 'YYYY-MM-DD_HH:MM:SS'"}), 400

    weather_data = WeatherData.query.filter(WeatherData.city_name == snake_case_to_name(city_name),func.date(WeatherData.date_time) == func.date(date_time)).first()

    if weather_data:
        if 'text/csv' in request.headers.get('Accept', ''):
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['id'])
            writer.writerow([weather_data.id])
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={"Content-Disposition": "inline"},
                status=200
            )
        return jsonify({"id": weather_data.id}), 200
    else:
        return jsonify({"error": "Weather data record not found " + snake_case_to_name(city_name) + " " + date_time.strftime('%Y-%m-%d %H:%M:%S')}), 404
    

def get_weather_data():
    # checking if retrieving data is done for a city or for all and applying initial query
    city_name = request.args.get('city_name')
    if city_name is not None:
        all_weather_data = WeatherData.query.filter_by(city_name=snake_case_to_name(city_name))
    else:
        all_weather_data = WeatherData.query.all()

    # optional parameters
    limit = request.args.get('limit')
    hide_id = request.args.get('hide_id', 'false').lower() == 'true'
    hide_city_name = request.args.get('hide_city_name', 'false').lower() == 'true'
    hide_temperature = request.args.get('hide_temperature', 'false').lower() == 'true'
    hide_date_time = request.args.get('hide_date_time', 'false').lower() == 'true'
    hide_relative_humidity = request.args.get('hide_relative_humidity', 'false').lower() == 'true'
    hide_apparent_temperature = request.args.get('hide_apparent_temperature', 'false').lower() == 'true'
    hide_precipitation = request.args.get('hide_precipitation', 'false').lower() == 'true'
    hide_rain = request.args.get('hide_rain', 'false').lower() == 'true'
    hide_snowfall = request.args.get('hide_snowfall', 'false').lower() == 'true'
    hide_wind_speed_10_m = request.args.get('hide_wind_speed_10_m', 'false').lower() == 'true'

    # attempting to get the limit value and apply it to the query
    if limit is not None:
        try:
            all_weather_data = all_weather_data.limit(int(limit))
        except ValueError:
            return jsonify({"error": "Limit value must be a whole number"}), 400

    # Check if the response should be in CSV format
    if 'text/csv' in request.headers.get('Accept', ''):
        csv_data = WeatherData.csv_header(hide_id=hide_id, hide_city_name=hide_city_name, hide_temperature=hide_temperature, hide_date_time=hide_date_time, hide_relative_humidity=hide_relative_humidity, hide_apparent_temperature=hide_apparent_temperature,hide_precipitation=hide_precipitation, hide_rain=hide_rain, hide_snowfall=hide_snowfall,hide_wind_speed_10_m=hide_wind_speed_10_m) + "\n"
        for weather_data in all_weather_data:
            csv_data += weather_data.csv(hide_id=hide_id, hide_city_name=hide_city_name, hide_temperature=hide_temperature, hide_date_time=hide_date_time, hide_relative_humidity=hide_relative_humidity, hide_apparent_temperature=hide_apparent_temperature,hide_precipitation=hide_precipitation, hide_rain=hide_rain, hide_snowfall=hide_snowfall,hide_wind_speed_10_m=hide_wind_speed_10_m) + "\n"
        return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=weather_data.csv"})

    response = []
    for weather_data in all_weather_data:
        weather_json = weather_data.json(hide_id=hide_id, hide_city_name=hide_city_name, hide_temperature=hide_temperature, hide_date_time=hide_date_time, hide_relative_humidity=hide_relative_humidity, hide_apparent_temperature=hide_apparent_temperature,hide_precipitation=hide_precipitation, hide_rain=hide_rain, hide_snowfall=hide_snowfall,hide_wind_speed_10_m=hide_wind_speed_10_m)
        response.append(weather_json)
    return jsonify(response)


def patch_weather_data():
    id = request.args.get('id')
    if id is None:
        return jsonify({"error": "id is a required parameter"}), 400

    # Trying to retrieve the record with the specified id
    weather_data = WeatherData.query.get(id)
    if not weather_data:
        return jsonify({"error": "No Weather Data record with the specified id"}), 404

    # receive the payload from the user
    data = request.get_json()

    # check what attributes need to be modified
    if "city_name" in data:
        weather_data.city_name = snake_case_to_name(data["city_name"])
    if "temperature" in data:
        weather_data.temperature = data["temperature"]
    if "date_time" in data:
        try:
            weather_data.date_time = datetime.strptime(data["date_time"], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"error": "Invalid time format. Use 'YYYY-MM-DD_HH:MM:SS'"}), 400
    if "relative_humidity" in data:
        weather_data.relative_humidity = data["relative_humidity"]
    if "apparent_temperature" in data:
        weather_data.apparent_temperature = data["apparent_temperature"]
    if "precipitation" in data:
        weather_data.precipitation = data["precipitation"]
    if "rain" in data:
        weather_data.rain = data["rain"]
    if "snowfall" in data:
        weather_data.snowfall = data["snowfall"]
    if "wind_speed_10_m" in data:
        weather_data.wind_speed_10_m = data["wind_speed_10_m"]

    db.session.commit()

    if 'text/csv' in request.headers.get('Accept', ''):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([weather_data.csv_header()])
        writer.writerow([weather_data.csv()])
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={"Content-Disposition": "inline"},
            status=200
        )

    return jsonify(weather_data.json()), 200


def put_weather_data():
    id = request.args.get('id')
    if id is None:
        return jsonify({"error": "id is a required parameter"}), 400

    # Trying to retrieve the record with the specified id
    weather_data = WeatherData.query.get(id)
    if not weather_data:
        return jsonify({"error": "No Weather Data record with the specified id"}), 404

    # receive the payload from the user
    data = request.get_json()

    # city name is a required field
    if "city_name" not in data:
        return jsonify({"error": "city_name is a required field"}), 400

    # temperature is a required field
    if "temperature" not in data:
        return jsonify({"error": "temperature is a required field"}), 400

    # Altering all the fields
    weather_data.city_name = snake_case_to_name(data.get("city_name"))
    weather_data.temperature = data.get("temperature")
    weather_data.date_time = data.get("date_time", datetime.now())
    weather_data.relative_humidity = data.get("relative_humidity", None)
    weather_data.apparent_temperature = data.get("apparent_temperature", None)
    weather_data.precipitation = data.get("precipitation", None)
    weather_data.rain = data.get("rain", None)
    weather_data.snowfall = data.get("snowfall", None)
    weather_data.wind_speed_10_m = data.get("wind_speed_10_m", None)

    db.session.commit()

    if 'text/csv' in request.headers.get('Accept', ''):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([weather_data.csv_header()])
        writer.writerow([weather_data.csv()])
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={"Content-Disposition": "inline"},
            status=200
        )
    return jsonify(weather_data.json()), 200

def delete_weather_data():
    id = request.args.get('id')
    if id is None:
        return jsonify({"error": "id is a required parameter"}), 400

    # Trying to retrieve the record with the specified id
    weather_data = WeatherData.query.get(id)
    if not weather_data:
        return jsonify({"error": "No Weather Data record with the specified id"}), 404

    # Delete the record
    db.session.delete(weather_data)
    db.session.commit()

    if 'text/csv' in request.headers.get('Accept', ''):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["message"])
        writer.writerow(["Weather data deleted successfully"])
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={"Content-Disposition": "inline"},
            status=200
        )
    return jsonify({"message": "Weather data deleted successfully"}), 200

def insert_weather_data():
    # receive the payload from the user
    data = request.get_json()

    if "city_name" not in data:
        return jsonify({"error": "city_name is a required parameter"}), 400

    if "temperature" not in data:
        return jsonify({"error": "temperature is a required parameter"}), 400

    new_weather = WeatherData(
        city_name=data["city_name"],
        temperature=data["temperature"],
        date_time=data.get("date_time", datetime.now()),
        relative_humidity=data.get("relative_humidity", None),
        apparent_temperature=data.get("apparent_temperature", None),
        precipitation=data.get("precipitation", None),
        rain=data.get("rain", None),
        snowfall=data.get("snowfall", None),
        wind_speed_10_m=data.get("wind_speed_10_m", None)
    )

    db.session.add(new_weather)
    db.session.commit()

    if 'text/csv' in request.headers.get('Accept', ''):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([new_weather.csv_header()])
        writer.writerow([new_weather.csv()])
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={"Content-Disposition": "inline"},
            status=201
        )
    return jsonify(new_weather.json()), 201
