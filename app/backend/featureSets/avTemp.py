from flask import jsonify, request, Response
from datetime import datetime
from projectFiles.data import WeatherData
from projectFiles.utils import snake_case_to_name
from io import StringIO
import csv

def get_average_temperature(city_name):
    year = request.args.get('year', default=datetime.now().year, type=int)
    month = request.args.get('month', default=datetime.now().month, type=int)

    city_name = snake_case_to_name(city_name) 

    try:
        if month < 1 or month > 12:
            return jsonify({"error": "Invalid month. Must be between 1 and 12."}), 400

        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) 
        else:
            end_date = datetime(year, month + 1, 1)

        weather_data_query = WeatherData.query.filter(
            WeatherData.city_name == city_name,
            WeatherData.date_time >= start_date,
            WeatherData.date_time < end_date
        )

        temperatures = [data.temperature for data in weather_data_query]
        
        if not temperatures:
            return jsonify({"error": "No weather data found for this city and date range."}), 404
        
        average_temperature = sum(temperatures) / len(temperatures)

        average_temperature = round(average_temperature, 2)

        if request.headers.get('Accept') == 'text/csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['City', 'Year', 'Month', 'Average Temperature'])
            month_name = start_date.strftime('%B') 
            writer.writerow([city_name, year, month_name, average_temperature])
            
            output.seek(0)
            return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=average_temperature.csv'})

        month_name = start_date.strftime('%B')  
        return jsonify({
            "city": city_name,
            "year": year,
            "month": month_name,
            "average_temperature": average_temperature  
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500