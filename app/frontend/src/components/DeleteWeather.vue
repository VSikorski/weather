<template>
  <div>
    <h1>Weather Data</h1>

    <div v-if="error" style="color: red">{{ error }}</div>
    <div v-else-if="loading">Loading...</div>
    <div v-else>
      <ul>
        <li v-for="(record, index) in data" :key="record.id">
          {{ record.city_name }} - {{ record.temperature }}°C
          <button @click="deleteRecord(record.id)">Delete</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

interface WeatherRecord {
  id: number;
  city_name: string;
  temperature: number;
}

export default defineComponent({
  name: 'WeatherData',
  data() {
    return {
      data: [] as WeatherRecord[], 
      loading: false,
      error: null as string | null,
    };
  },
  methods: {
    async fetchData(): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get<WeatherRecord[]>('http://localhost:4000/api/weather');
        this.data = response.data;
      } catch (err: any) {
        this.error = 'Failed to fetch weather data.';
      } finally {
        this.loading = false;
      }
    },
    async deleteRecord(id: number): Promise<void> {
      try {
        await axios.delete(`http://localhost:4000/api/weather`, { params: { id } });
        this.data = this.data.filter((record) => record.id !== id); 
      } catch (err: any) {
        alert('Failed to delete record.');
      }
    },
  },
  mounted() {
    this.fetchData();
  },
});
</script>

<style scoped>
button {
  margin-left: 1rem;
  color: white;
  background-color: red;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
}

button:hover {
  opacity: 0.8;
}
</style>
