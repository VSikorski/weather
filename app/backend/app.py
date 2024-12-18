from projectFiles import app
from featureSets import crud, monthlyWeather, avTemp, totalPrec, extremes

# ---------     REST API Section      ------------------------------------------------------

# endpoint to test the connection
@app.route("/api", methods=["GET"])
def welcome():
    return crud.welcome()

# endpoint to retrieve the ID of a weather data (assuming city_name and date_time is a unique combination)
@app.route("/api/weather/id", methods=["GET"])
def get_weather_data_id():
   return crud.get_weather_data_id()

# endpoint to retrieve weather data
@app.route("/api/weather", methods=["GET"])
def get_weather_data():
    return crud.get_weather_data()

# endpoint to update data
@app.route("/api/weather", methods=["PATCH"])
def patch_weather_data():
   return crud.patch_weather_data()

# endpoint to alter data
@app.route("/api/weather", methods=["PUT"])
def put_weather_data():
    return crud.put_weather_data()

# endpoint to delete
@app.route("/api/weather", methods=["DELETE"])
def delete_weather_data():
    return crud.delete_weather_data()

@app.route("/api/weather", methods=["POST"])
def get_data():
    return crud.insert_weather_data()

#-------- Get Monthly Weather ---------------------------------------------------------

@app.route("/monthly/<city_name>", methods=["GET"])
def get_monthly_weather(city_name):
    return monthlyWeather.get_monthly_weather(city_name)

#-------- Get Avarage Temperature ---------------------------------------------------------

@app.route("/average/<city_name>", methods=["GET"])
def get_average_temperature(city_name):
    return avTemp.get_average_temperature(city_name)

#-------------- Total Precipitation ----------------------  
@app.route("/precipitations/<city_name>", methods=["GET"])
def get_total_precipitations(city_name):
   return totalPrec.get_total_precipitations(city_name)

#----- Extreme top or bottom temp --------------------

@app.route("/extremes", methods=["GET"])
def temperature_extremes():
    return extremes.temperature_extremes()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)
