from flask import jsonify, request, Response
from datetime import datetime
from projectFiles.data import WeatherData
from projectFiles.utils import snake_case_to_name
from io import StringIO
import csv

def get_monthly_weather(city_name):
    year = request.args.get('year', default=datetime.now().year, type=int)
    month = request.args.get('month', default=datetime.now().month, type=int)
    include_hourly = request.args.get('include_hourly', default='false').lower() == 'true'
    show_date_time = request.args.get('show_date_time', default='false').lower() == 'true'
    
    city_name = snake_case_to_name(city_name)

    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

    try:
        weather_data_query = WeatherData.query.filter(
            WeatherData.city_name == city_name,
            WeatherData.date_time >= start_date,
            WeatherData.date_time < end_date
        ).order_by(WeatherData.date_time)

        if request.headers.get('Accept') == 'text/csv':
            output = StringIO()

            fieldnames = ["temperature", "precipitation", "rain", "snowfall", "wind_speed_10_m"]
            if show_date_time:
                fieldnames.insert(0, "date_time")  
            
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            for weather in weather_data_query:
                row = {
                    "temperature": weather.temperature,
                    "precipitation": weather.precipitation,
                    "rain": weather.rain,
                    "snowfall": weather.snowfall,
                    "wind_speed_10_m": weather.wind_speed_10_m
                }
                if show_date_time:
                    row["date_time"] = weather.date_time.strftime('%Y-%m-%d %H:%M:%S')
                
                writer.writerow(row)
            
            output.seek(0)
            return Response(output.getvalue(), mimetype='text/csv')

        monthly_data = []
        daily_data = {}

        for weather in weather_data_query:
            date_str = weather.date_time.strftime('%Y-%m-%d')

            if date_str not in daily_data:
                daily_data[date_str] = []

            row = {
                "temperature": weather.temperature,
                "precipitation": weather.precipitation,
                "rain": weather.rain,
                "snowfall": weather.snowfall,
                "wind_speed_10_m": weather.wind_speed_10_m
            }

            if show_date_time:
                row["date_time"] = weather.date_time.strftime('%Y-%m-%d %H:%M:%S')
            
            daily_data[date_str].append(row)

        for day, data in daily_data.items():
            monthly_data.append(data)

        return jsonify(monthly_data)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500