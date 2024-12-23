<template>
  <div class="container">
    <h1>Add Weather Data</h1>

    <form @submit.prevent="submitWeatherData" class="weather-form">
      <div class="form-row">
        <div class="form-group">
          <label for="city_name">City Name:</label>
          <input id="city_name" v-model="weatherData.city_name" required />
        </div>
        <div class="form-group">
          <label for="temperature">Temperature:</label>
          <input id="temperature" v-model.number="weatherData.temperature" required type="number" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="date_time">Date & Time:</label>
          <input id="date_time" v-model="weatherData.date_time" type="datetime-local" />
        </div>
        <div class="form-group">
          <label for="relative_humidity">Relative Humidity:</label>
          <input id="relative_humidity" v-model.number="weatherData.relative_humidity" type="number" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="apparent_temperature">Apparent Temperature:</label>
          <input id="apparent_temperature" v-model.number="weatherData.apparent_temperature" type="number" />
        </div>
        <div class="form-group">
          <label for="precipitation">Precipitation:</label>
          <input id="precipitation" v-model.number="weatherData.precipitation" type="number" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="rain">Rain:</label>
          <input id="rain" v-model.number="weatherData.rain" type="number" />
        </div>
        <div class="form-group">
          <label for="snowfall">Snowfall:</label>
          <input id="snowfall" v-model.number="weatherData.snowfall" type="number" />
        </div>
      </div>

      <div class="form-group">
        <label for="wind_speed_10_m">Wind Speed (10m):</label>
        <input id="wind_speed_10_m" v-model.number="weatherData.wind_speed_10_m" type="number" />
      </div>

      <button type="submit" class="submit-button">Submit</button>
    </form>

    <div v-if="responseMessage" class="response-message">
      {{ responseMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

interface WeatherData {
  city_name: string;
  temperature: number;
  date_time?: string | null;
  relative_humidity?: number | null;
  apparent_temperature?: number | null;
  precipitation?: number | null;
  rain?: number | null;
  snowfall?: number | null;
  wind_speed_10_m?: number | null;
}

export default defineComponent({
  name: 'AddWeatherData',
  data() {
    return {
      weatherData: {
        city_name: '',
        temperature: 0,
        date_time: null,
        relative_humidity: null,
        apparent_temperature: null,
        precipitation: null,
        rain: null,
        snowfall: null,
        wind_speed_10_m: null,
      } as WeatherData,
      responseMessage: '',
    };
  },
  methods: {
    async submitWeatherData(): Promise<void> {
      try {
        const response = await axios.post('http://localhost:4000/api/weather', this.weatherData, {
          headers: {
            Accept: 'application/json', 
          },
        });
        this.responseMessage = 'Weather data added successfully!';
      } catch (error: any) {
        this.responseMessage = error.response?.data?.error || 'Failed to add weather data.';
      }
    },
  },
});
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 1rem;
}

.weather-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.form-group {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 45%;
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #555;
}

input {
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
}

input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 3px rgba(0, 123, 255, 0.3);
}

.submit-button {
  padding: 0.8rem;
  font-size: 1rem;
  color: white;
  background-color: #28a745;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #218838;
}

.response-message {
  margin-top: 1rem;
  font-weight: bold;
  text-align: center;
  color: #28a745;
}
</style>
