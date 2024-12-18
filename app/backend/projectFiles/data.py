from datetime import datetime
from projectFiles.utils import name_to_snake_case, snake_case_to_name
from projectFiles import db

class WeatherData(db.Model):
  __tablename__ = "weatherData"
  id = db.Column(db.Integer, primary_key=True)
  city_name = db.Column(db.String(255), nullable=False)
  temperature = db.Column(db.Float, nullable=False)
  date_time = db.Column(db.DateTime, nullable=False)
  relative_humidity = db.Column(db.Float, nullable=True)
  apparent_temperature = db.Column(db.Float, nullable=True)
  precipitation = db.Column(db.Float, nullable=True)
  rain = db.Column(db.Float, nullable=True)
  snowfall = db.Column(db.Float, nullable=True)
  wind_speed_10_m = db.Column(db.Float, nullable=True)

  def __init__(self, city_name, temperature, date_time=None, relative_humidity=None, apparent_temperature=None, precipitation=None, rain=None, snowfall=None, wind_speed_10_m=None):
    self.city_name = snake_case_to_name(city_name)
    self.temperature = temperature
    self.date_time = date_time or datetime.now()
    self.relative_humidity = relative_humidity
    self.apparent_temperature = apparent_temperature
    self.precipitation = precipitation
    self.rain = rain
    self.snowfall = snowfall
    self.wind_speed_10_m = wind_speed_10_m

  def json(self, hide_id=False, hide_city_name=False, hide_temperature=False, hide_date_time=False, hide_relative_humidity=False, hide_apparent_temperature=False, hide_precipitation=False, hide_rain=False, hide_snowfall=False, hide_wind_speed_10_m=False):
    weather_json = {}

    if not hide_id:
      weather_json["id"] = self.id
    if not hide_city_name:
      weather_json["city_name"] = self.city_name
    if not hide_temperature:
      weather_json["temperature"] = self.temperature
    if not hide_date_time:
      weather_json["date_time"] = self.date_time.strftime("%Y-%m-%d %H:%M:%S")
    if not hide_relative_humidity:
      weather_json["relative_humidity"] = self.relative_humidity
    if not hide_apparent_temperature:
      weather_json["apparent_temperature"] = self.apparent_temperature
    if not hide_precipitation:
      weather_json["precipitation"] = self.precipitation
    if not hide_rain:
      weather_json["rain"] = self.rain
    if not hide_snowfall:
      weather_json["snowfall"] = self.snowfall
    if not hide_wind_speed_10_m:
      weather_json["wind_speed_10_m"] = self.wind_speed_10_m

    return weather_json

  def csv(self, hide_id=False, hide_city_name=False, hide_temperature=False, hide_date_time=False, hide_relative_humidity=False,hide_apparent_temperature=False, hide_precipitation=False, hide_rain=False, hide_snowfall=False,hide_wind_speed_10_m=False):
    csv_data = []

    if not hide_id:
      csv_data.append(str(self.id))
    if not hide_city_name:
      csv_data.append(self.city_name)
    if not hide_temperature:
      csv_data.append(str(self.temperature))
    if not hide_date_time:
      csv_data.append(str(self.date_time.strftime('%Y-%m-%d %H:%M:%S')))
    if not hide_relative_humidity:
      csv_data.append(str(self.relative_humidity) if self.relative_humidity is not None else 'None')
    if not hide_apparent_temperature:
      csv_data.append(str(self.apparent_temperature) if self.apparent_temperature is not None else 'None')
    if not hide_precipitation:
      csv_data.append(str(self.precipitation) if self.precipitation is not None else 'None')
    if not hide_rain:
      csv_data.append(str(self.rain) if self.rain is not None else 'None')
    if not hide_snowfall:
      csv_data.append(str(self.snowfall) if self.snowfall is not None else 'None')
    if not hide_wind_speed_10_m:
      csv_data.append(str(self.wind_speed_10_m) if self.wind_speed_10_m is not None else 'None')

    return ','.join(csv_data)

  @staticmethod
  def csv_header(hide_id=False, hide_city_name=False, hide_temperature=False, hide_date_time=False, hide_relative_humidity=False,hide_apparent_temperature=False, hide_precipitation=False, hide_rain=False, hide_snowfall=False,hide_wind_speed_10_m=False):
    csv_data = []

    if not hide_id:
      csv_data.append('id')
    if not hide_city_name:
      csv_data.append('city_name')
    if not hide_temperature:
      csv_data.append('temperature')
    if not hide_date_time:
      csv_data.append('datetime')
    if not hide_relative_humidity:
      csv_data.append('relative_humidity')
    if not hide_apparent_temperature:
      csv_data.append('apparent_temperature')
    if not hide_precipitation:
      csv_data.append('precipitation')
    if not hide_rain:
      csv_data.append('rain')
    if not hide_snowfall:
      csv_data.append('snowfall')
    if not hide_wind_speed_10_m:
      csv_data.append('wind_speed_10_m')

    return ','.join(csv_data)