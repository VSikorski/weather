from config import db, app

class WeatherData(db.Model):
  __tablename__ = "weatherData"

  id = db.Column(db.Integer, primary_key=True)
  city_name = db.Column(db.String(255), nullable=False)
  date_time = db.Column(db.DateTime, nullable=False)
  temperature = db.Column(db.Float, nullable=False)
  relative_humidity = db.Column(db.Float, nullable=True)
  apparent_temperature = db.Column(db.Float, nullable=True)
  precipitation = db.Column(db.Float, nullable=True)
  rain = db.Column(db.Float, nullable=True)
  snowfall = db.Column(db.Float, nullable=True)
  wind_speed_10_m = db.Column(db.Float, nullable=True)

  def __init__(self, city_name, date_time, temperature, relative_humidity=None, apparent_temperature=None, precipitation=None, rain=None, snowfall=None, wind_speed_10_m=None):
    self.city_name = city_name
    self.date_time = date_time
    self.temperature = temperature
    self.relative_humidity = relative_humidity
    self.apparent_temperature = apparent_temperature
    self.precipitation = precipitation
    self.rain = rain
    self.snowfall = snowfall
    self.wind_speed_10_m = wind_speed_10_m

  def json(self):
    return {
      "id": self.id,
      "city_name": self.city_name,
      "date_time": self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
      "temperature": self.temperature,
      "relative_humidity": self.relative_humidity,
      "apparent_temperature": self.apparent_temperature,
      "precipitation": self.precipitation,
      "rain": self.rain,
      "snowfall": self.snowfall,
      "wind_speed_10_m": self.wind_speed_10_m
    }
  
  def csv(self):
    return f"{self.id},{self.city_name},{self.date_time.strftime('%Y-%m-%d %H:%M:%S')},{self.temperature},{self.relative_humidity},{self.apparent_temperature},{self.precipitation},{self.rain},{self.snowfall},{self.wind_speed_10_m}"


# create the database
with app.app_context():
    db.create_all()