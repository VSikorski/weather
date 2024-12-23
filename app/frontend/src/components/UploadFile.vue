<template>
  <div class="container">
    <h1>Upload Weather Data CSV File</h1>
    <form @submit.prevent="uploadFile">

        <div class="form-row">
          <input id="uploadedFile" type="file" @change="onChangedFile"/>
        </div>


      <button type="submit">Upload</button>
    </form>

    <div v-if="responseMessage" class="response-message">
      {{ responseMessage }}
    </div>
    <div v-if="errorMessage" class="response-message error">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'UploadFile',
  data() {
    return {
        responseMessage: '',
        errorMessage: ''
    };
  },
  methods: {
    onChangedFile() {
        const input = document.getElementById('uploadedFile') as HTMLInputElement;
        if (input.files && input.files[0] && !input.files[0].name.endsWith('.csv')) {
            this.errorMessage = "Please select a CSV file format";
            return;
        }
        this.errorMessage = '';
    },
    async uploadFile() {
        const input = document.getElementById('uploadedFile') as HTMLInputElement;

        if (!input.files || (input.files && input.files.length === 0)) {
            this.errorMessage = "Please select a file";
            return;
        }
        if (input.files.length > 1) {
            this.errorMessage = "Please select one file at a time";
            return;
        }
        if (input.files[0] && !input.files[0].name.endsWith('.csv')) {
            this.errorMessage = "Please select a CSV file format";
            return;
        }

        let weatherObjects;
        try {
            weatherObjects = await this.parseCSVtoObjects(input.files[0]);
        } catch (error: any) {
            this.errorMessage = error.message;
            return;
        }

        if (!weatherObjects) {
            this.errorMessage = 'Weather data cannot be empty';
        }

        try {
            const response = await axios.post('http://localhost:4000/api/weather', weatherObjects, {
                headers: {
                    Accept: 'application/json'
                },
            });
            if (response.status === 201) {
                this.responseMessage = 'Weather data added successfully!';
                this.errorMessage = '';
            } else {
                this.errorMessage = JSON.stringify(response, null, 2);
                this.responseMessage = '';
            }
        } catch (error: any) {
            if (error.response) {
                this.errorMessage = JSON.stringify(error.response.data, null, 2);
            } else {
                this.errorMessage = error.message;
            }
            this.responseMessage = '';
        }
    },
    parseCSVtoObjects(file: File): Promise<Record<string, any>[]> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = (e) => {
                const data = e.target?.result as string;

                if (!data) {
                    reject(new Error("File cannot be empty"));
                    return;
                }

                const lines = data.split('\n').map(line => line.trim()).filter(line => line.length > 0);
                if (lines.length < 2) {
                    reject(new Error("Empty file or no data"));
                    return;
                }

                const header = lines[0].split(',');

                const weatherData = lines.slice(1).map(line => {
                    const values = line.split(',');
                    const entry: Record<string, any> = {};

                    header.forEach((hd, idx) => {
                        if (hd === 'date_time') {
                            entry[hd] = values[idx];
                        } else {
                            entry[hd] = isNaN(parseFloat(values[idx])) ? values[idx] : parseFloat(values[idx]);
                        }
                    });

                    return entry;
                });

                resolve(weatherData);
            };

            reader.onerror = () => {
                reject(new Error("Error reading the file"));
            };

            reader.readAsText(file);
        });
    }
  }
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

.response-message.error {
  color: red;
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
