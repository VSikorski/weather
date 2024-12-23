<template>
  <div class="container">
    <h1>Update Weather Data</h1>
    <form @submit.prevent="updateData">
      <div class="form-group full-width">
        <label for="id">ID (required):</label>
        <input id="id" v-model="id" required />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="city_name">City Name:</label>
          <input id="city_name" v-model="fields.city_name" />
        </div>

        <div class="form-group">
          <label for="temperature">Temperature:</label>
          <input id="temperature" v-model.number="fields.temperature" type="number" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="date_time">Date & Time:</label>
          <input id="date_time" v-model="fields.date_time" type="datetime-local" />
        </div>

        <div class="form-group">
          <label for="relative_humidity">Relative Humidity:</label>
          <input id="relative_humidity" v-model.number="fields.relative_humidity" type="number" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="apparent_temperature">Apparent Temperature:</label>
          <input id="apparent_temperature" v-model.number="fields.apparent_temperature" type="number" />
        </div>

        <div class="form-group">
          <label for="precipitation">Precipitation:</label>
          <input id="precipitation" v-model.number="fields.precipitation" type="number" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="rain">Rain:</label>
          <input id="rain" v-model.number="fields.rain" type="number" />
        </div>

        <div class="form-group">
          <label for="snowfall">Snowfall:</label>
          <input id="snowfall" v-model.number="fields.snowfall" type="number" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="wind_speed_10_m">Wind Speed (10m):</label>
          <input id="wind_speed_10_m" v-model.number="fields.wind_speed_10_m" type="number" />
        </div>
      </div>

      <button type="submit">Update</button>
    </form>

    <div v-if="responseMessage" class="response-message">
      {{ responseMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'UpdateWeather',
  data() {
    return {
      id: '',
      fields: {
        city_name: null,
        temperature: null,
        date_time: null,
        relative_humidity: null,
        apparent_temperature: null,
        precipitation: null,
        rain: null,
        snowfall: null,
        wind_speed_10_m: null,
      },
      responseMessage: '',
    };
  },
  methods: {
    async updateData() {
      if (!this.id) {
        this.responseMessage = 'ID is required to update data.';
        return;
      }

      const updatePayload = Object.fromEntries(
        Object.entries(this.fields).filter(([_, value]) => value !== null)
      );

      if (Object.keys(updatePayload).length === 0) {
        this.responseMessage = 'No fields specified for update.';
        return;
      }

      try {
        const response = await axios.put(
          `http://localhost:4000/api/weather?id=${this.id}`,
          updatePayload,
          {
            headers: {
              'Content-Type': 'application/json',
              Accept: 'application/json',
            },
          }
        );
        this.responseMessage = 'Weather data updated successfully!';
      } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          this.responseMessage =
            error.response?.data?.error || 'Failed to update weather data.';
        } else if (error instanceof Error) {
          this.responseMessage = error.message;
        } else {
          this.responseMessage = 'An unknown error occurred.';
        }
      }
    },
  },
});
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  color: #000000;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333333;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 250px;
}

.full-width {
  flex: 100%;
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  display: block;
}

input {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
  color: #000000;
}

input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 4px rgba(0, 123, 255, 0.5);
}

button {
  padding: 0.75rem;
  font-size: 1rem;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #0056b3;
}

.response-message {
  margin-top: 1rem;
  text-align: center;
  font-weight: bold;
  color: green;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }

  .form-group {
    min-width: 100%;
  }
}
</style>
