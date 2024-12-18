<template>
  <div>
    <h1>Weather Data</h1>
    <button @click="fetchData">Fetch Weather Data</button>

    <div v-if="error" style="color: red">{{ error }}</div>
    <div v-else-if="loading">Loading...</div>
    <div v-else>
      <ul>
        <!-- Display only the data for the current page -->
        <li v-for="item in paginatedData" :key="item.id">
          <strong>{{ item.city_name }}</strong> ({{ item.date_time }}):<br />
          Temperature: {{ item.temperature }}°C<br />
          Apparent Temperature: {{ item.apparent_temperature }}°C<br />
          Precipitation: {{ item.precipitation }} mm<br />
          Wind Speed: {{ item.wind_speed_10_m }} m/s<br />
        </li>
      </ul>
      
      <!-- Pagination Controls -->
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="prevPage">Previous</button>
        <button :disabled="currentPage === totalPages" @click="nextPage">Next</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

// Define the type for a single weather record
interface WeatherRecord {
  id: number;
  city_name: string;
  date_time: string;
  temperature: number;
  apparent_temperature: number;
  precipitation: number;
  rain: number;
  relative_humidity: number;
  snowfall: number;
  wind_speed_10_m: number;
}

export default defineComponent({
  name: 'WeatherData',
  data() {
    return {
      data: [] as WeatherRecord[], // Array of weather records
      loading: false, // Loading state
      error: '' as string | null, // Error message
      currentPage: 1, // Current page number
      itemsPerPage: 3, // Number of items per page
    };
  },
  computed: {
    // Calculate the total number of pages
    totalPages(): number {
      return Math.ceil(this.data.length / this.itemsPerPage);
    },
    // Get the data for the current page
    paginatedData(): WeatherRecord[] {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.data.slice(start, end);
    },
  },
  methods: {
    async fetchData(): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get<WeatherRecord[]>('http://localhost:4000/api/weather');
        this.data = response.data; // Update the data array
      } catch (err: any) {
        this.error = 'Failed to fetch weather data.';
      } finally {
        this.loading = false;
      }
    },
    // Navigate to the previous page
    prevPage(): void {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    // Navigate to the next page
    nextPage(): void {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
  },
});
</script>

<style scoped>
.pagination {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

