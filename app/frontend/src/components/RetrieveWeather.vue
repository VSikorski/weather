<template>
  <div>
    <h1>Weather Data</h1>

    <div v-if="error" style="color: red">{{ error }}</div>
    <div v-else-if="loading">Loading...</div>
    <div v-else>
      <!-- Toggle for Representation Mode -->
      <div class="toggle-mode">
        <label for="mode">View as:</label>
        <select v-model="representationMode" id="mode">
          <option value="json">JSON</option>
          <option value="csv">CSV</option>
        </select>
      </div>

      <!-- Data representation -->
      <div class="data-box">
        <pre v-if="representationMode === 'json'">{{ formattedCurrentItem }}</pre>
        <pre v-else>{{ formattedCsv }}</pre>
      </div>

      <div class="pagination">
        <button :disabled="currentIndex === 0" @click="prevItem">Previous</button>
        <button :disabled="currentIndex === data.length - 1" @click="nextItem">Next</button>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

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
      loading: false, 
      error: '' as string | null, 
      currentIndex: 0, 
      representationMode: 'json',
    };
  },
  computed: {
    // Format the current item as JSON with indentation
    formattedCurrentItem(): string {
      return JSON.stringify(this.data[this.currentIndex], null, 2);
    },
    // Format the current item as CSV
    formattedCsv(): string {
      const currentItem = this.data[this.currentIndex];
      const headers = Object.keys(currentItem).join(', ');
      const values = Object.values(currentItem).join(', ');
      return `${headers}\n${values}`;
    },
  },
  methods: {
    async fetchData(): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get<WeatherRecord[]>('http://localhost:4000/api/weather');
        this.data = response.data; // Store fetched data
        this.currentIndex = 0; // Start with the first item
      } catch (err: any) {
        this.error = 'Failed to fetch weather data.';
      } finally {
        this.loading = false;
      }
    },
    // Navigate to the previous item
    prevItem(): void {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    // Navigate to the next item
    nextItem(): void {
      if (this.currentIndex < this.data.length - 1) {
        this.currentIndex++;
      }
    },
  },
  mounted() {
    this.fetchData(); 
  },
});
</script>


<style scoped>
.data-box {
  background-color: #f9f9f9;
  color: #333;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  overflow-x: auto;
}

.toggle-mode {
  margin-bottom: 1rem;
}

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

