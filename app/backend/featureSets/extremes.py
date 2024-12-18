from flask import jsonify, request, Response
from datetime import datetime
from projectFiles.data import WeatherData
from sqlalchemy import func
from io import StringIO
import csv

def temperature_extremes():
    N = request.args.get('N', type=int)
    year = request.args.get('year', type=int)
    M = request.args.get('M', type=int)
    type = request.args.get('type', default='top', type=str).lower()

    if N is None or N < 1:
        return jsonify({"error": "N has to be a positive"}), 400
    
    if type not in ['top', 'bottom']:
        return jsonify({"error": "type has to be either top or bottom"}), 400

    try:
        filters = []

        if year:
            filters.append(func.extract('year', WeatherData.date_time) == year)

        if M:
            current_year = datetime.now().year
            year_range = [current_year - i for i in range(M)]
            filters.append(func.extract('year', WeatherData.date_time).in_(year_range))

        query = WeatherData.query.filter(*filters).with_entities(
            WeatherData.city_name,
            WeatherData.date_time,
            WeatherData.temperature
        ).order_by(WeatherData.temperature.desc() if type == 'top' else WeatherData.temperature.asc())

        extremes = query.limit(N).all()

        if request.headers.get('Accept') == 'text/csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['city_name', 'date_time', 'temperature']) 
            for record in extremes:
                writer.writerow([record.city_name, record.date_time.strftime('%Y-%m-%d %H:%M:%S'), record.temperature])
            
            output.seek(0)
            return Response(output.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=temperature_extremes.csv"})

        result = []
        for record in extremes:
            result.append({
                "city_name": record.city_name,
                "date_time": record.date_time.strftime('%Y-%m-%d %H:%M:%S'),
                "temperature": record.temperature
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500