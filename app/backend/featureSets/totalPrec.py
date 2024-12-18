from flask import jsonify, request, Response
from datetime import datetime
from projectFiles.data import WeatherData
from projectFiles.utils import snake_case_to_name
from sqlalchemy import func
from io import StringIO
import csv

def get_total_precipitations(city_name):
    city_name = snake_case_to_name(city_name)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    try:
        filters = [WeatherData.city_name == city_name]

        if year:
            filters.append(func.extract('year', WeatherData.date_time) == year)
        if month:
            filters.append(func.extract('month', WeatherData.date_time) == month)
        else:
            current_date = datetime.now()
            filters.append(func.extract('month', WeatherData.date_time) == current_date.month)

        weather_data_query = WeatherData.query.filter(*filters).with_entities(
            func.extract('year', WeatherData.date_time).label('year'),
            func.extract('month', WeatherData.date_time).label('month'),
            func.date(WeatherData.date_time).label('day'),
            func.sum(WeatherData.precipitation).label('total_precipitation')
        ).group_by(
            func.extract('year', WeatherData.date_time),
            func.extract('month', WeatherData.date_time),
            func.date(WeatherData.date_time)
        ).order_by(
            func.extract('year', WeatherData.date_time),
            func.extract('month', WeatherData.date_time),
            func.date(WeatherData.date_time)
        )

        precipitation_data = {}
        for year_result, month_result, day, total_precipitation in weather_data_query:
            month_name = datetime(year=int(year_result), month=int(month_result), day=1).strftime('%B')
            year_result = str(int(year_result))

            if year_result not in precipitation_data:
                precipitation_data[year_result] = {}

            if month_name not in precipitation_data[year_result]:
                precipitation_data[year_result][month_name] = []

            precipitation_data[year_result][month_name].append({
                'day': day.strftime('%d'),
                "total_precipitation": total_precipitation
            })

        if request.headers.get('Accept') == 'text/csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['Year', 'Month', 'Day', 'Total Precipitation'])
            for year_result, months in precipitation_data.items():
                for month_name, days in months.items():
                    for record in days:
                        writer.writerow([year_result, month_name, record["day"], record["total_precipitation"]])
            output.seek(0)
            return Response(output.getvalue(), mimetype='text/csv',
                            headers={'Content-Disposition': 'attachment; filename=precipitations.csv'})

        return jsonify(precipitation_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
