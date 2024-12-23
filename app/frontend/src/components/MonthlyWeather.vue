<template>
    <div class="container">
      <h1>Monthly Weather Data</h1>
      <form @submit.prevent="fetchMonthlyWeatherData" class="weather-form">
        <div class="form-row">
          <div class="form-group">
            <label for="city_name">City Name:</label>
            <input id="city_name" v-model="city" required />
          </div>
          <div class="form-group">
            <label for="year">Year:</label>
            <input id="year" v-model.number="year" required type="number" min="1900" max="2100" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="month">Month:</label>
            <input id="month" v-model.number="month" required type="number" min="1" max="12" />
          </div>
        </div>
        <div class="form-group">
          <input id="include_hourly" type="checkbox" v-model="includeHourly" />
          <label for="include_hourly">Include Hourly Data</label>
        </div>
        <div class="form-group">
          <input id="show_date_time" type="checkbox" v-model="showDateTime" />
          <label for="show_date_time">Show Date and Time</label>
        </div>
        <button type="submit" class="submit-button">Fetch Data</button>
      </form>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="response-message">
        {{ successMessage }}
      </div>
      <div v-if="dataTimestamp" class="timestamp">
        Data fetched on: {{ dataTimestamp }}
      </div>
        <div v-if="weatherData" class="weather-data">
        <h2>Weather Data:</h2>
        <pre>{{ weatherData }}</pre>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import axios from 'axios';
  
  export default defineComponent({
    name: "MonthlyWeatherData",
    data() {
      return {
        city: "",
        year: new Date().getFullYear(),
        month: new Date().getMonth() + 1,
        includeHourly: false,
        showDateTime: false,
        successMessage: "",
        errorMessage: "",
        dataTimestamp: "",
        weatherData: null,
      };
    },
    methods: {
      async fetchMonthlyWeatherData(): Promise<void> {
        this.successMessage = "";
        this.errorMessage = "";
        this.dataTimestamp = "";
        this.weatherData = null;
  
        try {
          const response = await axios.get(
            `http://localhost:4000/monthly/${this.city}`,
            {
              params: {
                year: this.year,
                month: this.month,
                hourly: this.includeHourly,
                show_date_time: this.showDateTime,
              },
            }
          );
  
          if (response.data && response.data.length > 0) {
            this.weatherData = response.data;
            this.successMessage = `Weather data for ${this.city} (${this.year}-${this.month}) successfully retrieved.`;
            this.dataTimestamp = new Date().toLocaleString();
          } else {
            this.successMessage = `No weather data found for ${this.city} (${this.year}-${this.month}).`;
          }
        } catch (error: any) {
          console.error("Error occurred while fetching data", error);
          this.errorMessage =
            error.response?.data?.error || "Fail occured while fetching data..";
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

input,
  select {
    padding: 0.8rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
  }
  
  input:focus,
  select:focus {
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
  
  .error-message {
    margin-top: 1rem;
    font-weight: bold;
    text-align: center;
    color: #dc3545;
  }
  
  .timestamp {
    margin-top: 1rem;
    text-align: center;
    font-size: 0.9rem;
    color: #555;
  }
  
  .weather-data {
    margin-top: 1rem;
    padding: 1rem;
    background-color: #e9ecef;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    font-size: 0.9rem;
    color: #333;
  }

  </style>