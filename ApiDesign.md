# **Specification file:** Weather App API

## Table of Contents
1. [Overview](#1-overview)
2. [Database Schema](#2-database-schema)
3. [Endpoints](#3-endpoints)
   - [3.1 Weather Forecast](#31-weather-forecast)
   - [3.2 Monthly Weather Forecast](#32-monthly-weather-forecast)
   - [3.3 Average Monthly Temperature](#33-average-monthly-temperature)
   - [3.4 Precipitations](#34-precipitations)
   - [3.5 Temperature Extremes](#35-temperature-extremes)
## **1. Overview**
**The Weather App API** is an application that provides users with hourly updated weather data and allows the client to decide on the sophistication of the requested information. The functionality of the program is broken down into the following feature sets to reduce complexity:

- **Weather Forecast** - allows guest users to retrieve all the available weather data for a city and users with admin role to create, update and delete the related data. [3.1 Weather Forecast](#31-weather-forecast)

- **Monthly Weather Forecast** - allows users to retrieve the monthly weather data of a city, for a specific month and year. [3.2 Monthly Weather Forecast](#32-monthly-weather-forecast)

- **Average Monthly Temperature** - provides the average monthly temperature of a specified city, starting from a provided year. [3.3 Average Monthly Temperature](#33-average-monthly-temperature)

- **Precipitations** - provides the user with the total daily precipitations amount of a specified city and month. [3.4 Precipitations](#34-precipitations)

- **Extremes** - provides the minimum and maximum temperature extremes for a specified year or period of years. [3.5 Temperature Extremes](#35-temperature-extremes)

## **2. Database Schema**

### Weather Data 
| attributes |
| ------ |
| **id:** INT _primary_ |
| **city_name:** VARCHAR(255) |
| **date_time:** DATETIME |
| **temperature:** FLOAT |
| **relative_humidity:** FLOAT |
| **apparent_temperature:** FLOAT |
| **precipitation:** FLOAT |
| **rain:** FLOAT |
| **snowfall:** FLOAT |
| **wind_speed_10_m:** FLOAT |

## **3. Endpoints**

The base URI of the API is https://localhost:4000/api, followed by the endpoint of the desired feature set and operation. If not specified otherwise, retrieval of record(s) is done in **JSON** format, to receive the information in **CSV** format instead, include the `Accept: text/csv` header value in your request. Consider using snake_case notation when passing parameters, for example when passing the city name "abu_dhabi", the system will intrepret it and store it in the database as "Abu Dhabi". To test the API connection, access the base API URI.
##### **GET /api**

```json
{"message":"Welcome to the Weather App!"}
```

### **3.1 Weather Forecast**

The endpoint of the feature set is **/weather**. The optional parameter **city_name** represents the city to query (in snake case notation), if not provided, the system returns all available records.

##### **GET /weather**
To apply a limit to the query, use the **limit** paramter.\
**Example request - response:**\
`
/weather?city_name=abu_dhabi&limit=1
`
```json
{
   "id": 5,
   "city_name": "Abu Dhabi",
   "date_time": "2000-08-31-05:00:00",
   "temperature": 17.9,
   "relative_humidity": 0.9,
   "apparent_temperature": 18.3,
   "precipitation": 0.0,
   "rain": 0.1,
   "snowfall": 0.0,
   "wind_speed_10_m": 1.0
}
```

By default all attributes are shown, to override this behaviour include the parameter **hide_{{attribute_name}}=true**\
**Example request - response:**\
`
/weather?city_name=paris&hide_id=true&hide_date_time=true&limit=1
`
```json
{
   "city_name": "Paris",
   "temperature": 17.9,
   "relative_humidity": 0.9,
   "apparent_temperature": 18.3,
   "precipitation": 0.0,
   "rain": 0.1,
   "snowfall": 0.0,
   "wind_speed_10_m": 1.0
}
```

   **Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 200  | Successful operation | [Weather Data ](#Weather Data) |
   | 400  | Path parameter not passed | None |
   | 404  | Path parameter not found | None |
   | 500  | Internal Server Error | None |


   ##### **GET /weather/id**

   To alter or modify a record, the **id** attribute will be required, to retrieve it, access this endpoint with the **city_name** and **date_time** parameters and the system will return you the ID of the record with the matching attributes. The city_name must be in snake_case notation and the date_time must follow the '**YYYY-MM-DD_HH:MM:SS**' format.\
   **Example request - response:**\
`
/weather/id?city_name=abu_dhabi&date_time=2024-12-01_17:50:19
`
```json
{
   "id": 18
}
```


##### **PUT /weather/**

The put method can be used to alter the weather data with the specified **id** parameter.\
**Example request, request body**\
`
/weather?id=19
`
```json
{
   "city_name": "Paris",
   "date_time": "2024-12-31_05:00:00",
   "temperature": 17.9,
   "relative_humidity": 0.9,
   "apparent_temperature": 18.3,
   "precipitation": 0.0,
   "rain": 0.1,
   "snowfall": 0.0,
   "wind_speed_10_m": 1.0
}
```

   **Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 200  | Successful alter of weather data | [Weather Data ](#Weather Data) |
   | 400  | Path parameter not passed | None |
   | 409  | Missing request body | None |
   | 500  | Internal Server Error | None |

##### **PATCH /weather**

The patch method can be used to modify any piece of the weather data information. Specify the **id** of the record you want to modify and include in the body the fields you want to replace. The response will be the newly modified object.\
**Example request, request body**\
`
/weather?id=18
`
`
```json
{
  "rain": 0.1
}
```

**Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 200  | Successful update of weather data | [Weather Data ](#Weather Data) |
   | 400  | Path parameter not passed | None |
   | 404  | Path parameter not found | None |
   | 409  | Missing request body | None |
   | 500  | Internal Server Error | None |

##### **POST /weather**

To add a new record to the database, send a json body representing the new record. The only required fields for a successful response are **city_name** and **temperature**. If the **date_time** attribute is not specified, the current timestamp will be inserted.\
**Example request, request body**\
`
/weather
`
```json
{
  "city_name": "Helsinki",
  "temperature": 9.6
}
```

   **Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 201  | Weather data created | [Weather Data ](#Weather Data) |
   | 400  | Required parameters not passed | None |
   | 500  | Internal Server Error | None |

##### **DELETE /weather**

In order to delete a record, the **id** query parameter must be provided.\
**Example request - response:**\
`
/weather/id=2
`
```json
{"message": "Weather data deleted successfully"}
```

   **Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 200  | Weather data successfully deleted | None |
   | 400  | ID not passed | None |
   | 404  | ID not found | None |
   | 500  | Internal Server Error | None |

---

### **3.2 Monthly Weather Forecast**

The endpoint of the feature set is */monthly/{city-name}. The feature set will provide information about the weather for every day of the specified month and year. The **month* and *year* parameters take the current month and year by default and are not required to be part of the request. To costumize the data you receive for each day, the parameters from section 3.1 Daily Weather Forecast are reutilized. The endpoint also allows you to include the *include_hourly* parameter (boolean, by default false) which will display the hourly information (can be heavy with complex daily weather data information). In the case of the current month as the *month* parameter, the data is capped at the current date and time. Also,
*show_date_time=true* operation performs displayin inforamtion about date and time (boolean, by default false). If not selected will not retrieve date and time.

##### **GET /monthly/{city_name}**

The request with no passed in parameters will take in the current **month** and **year** values and the basic daily weather information (temperature only, advice section 3.1 for more information).\
**Example request - response:**\
`
/monthly/london
`
```json
[
  [
    {
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 18.9,
      "wind_speed_10_m": 5.5
    }
  ],
  [
    {
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 18.9,
      "wind_speed_10_m": 5.5
    },
    {
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 100,
      "wind_speed_10_m": 5.5
    }
  ]
]
```

The user can also specify a custom **year** and **month** query parameter.\
**Example request - response:**\
`
/monthly/london?year=2023&month=12
`
```json
[
  [
    {
      "precipitation": 100,
      "rain": 100,
      "snowfall": 100,
      "temperature": 100,
      "wind_speed_10_m": 100
    }
  ]
]
```

To further costumize the daily weather data, show_date_time* operation added which will result of showing date and time.\
**Example request - response:**\
`
/monthly/london?year=2024&show_date_time=true
`\
```json
[
  [
    {
      "date_time": "2024-12-01 12:00:00",
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 18.9,
      "wind_speed_10_m": 5.5
    }
  ],
  [
    {
      "date_time": "2024-12-02 12:00:00",
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 18.9,
      "wind_speed_10_m": 5.5
    },
    {
      "date_time": "2024-12-02 14:02:15",
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 100,
      "wind_speed_10_m": 5.5
    }
  ]
]
```

The endpoint can also provide the hourly information, for each day of the month, using the **include_hourly=true** parameter. Keep in mind that such requests can be heavy if paired with complex weather details.\
**Example request - response:**\
`
/monthly/london?include_hourly=true
`\
```json
[
  [
    {
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 18.9,
      "wind_speed_10_m": 5.5
    }
  ],
  [
    {
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 18.9,
      "wind_speed_10_m": 5.5
    },
    {
      "precipitation": 0,
      "rain": 0,
      "snowfall": 0,
      "temperature": 100,
      "wind_speed_10_m": 5.5
    }
  ]
]
```
This is just sample for previous output use include_hourly but now output is in csv format.\
**Example request - response:**\
/monthly/london?include_hourly=true
`
```csv
temperature,precipitation,rain,snowfall,wind_speed_10_m
18.9,0.0,0.0,0.0,5.5
18.9,0.0,0.0,0.0,5.5
100.0,0.0,0.0,0.0,5.5
```

   **Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 200  | Successful operation | [Weather Data ](#Weather Data) |
   | 400  | Path parameter not passed | None |
   | 404  | Path parameter not found | None |
   | 500  | Internal Server Error | None |

---

### **3.3 Average Monthly Temperature**

The endpoint for this feature set is */average/{city_name}. The endpoint returns the average temperature of the current month and can also take in an optional parameter **year*  which will enable the system to return the average temperature of every month from the specified year (or capped at first record) until present. If *month* paramater is also given, then it retrieves specifically for that *month* and *year.  In case only **month* selected then it takes current year as default.

##### **GET /average/{city_name}**

Without any query parameters, the response will simply include the average temperature (float) of the current month in the specified city.\
**Example request - response:**\
`
/average/London
`
```json
{
  "average_temperature": 45.93,
  "city": "London",
  "month": "December",
  "year": 2024
}
```

To get the average of every month starting from a specific year, the **year** parameter can be used.\
**Example request - response:**\
`
/average/London?year=2024
`
```json
{
  "average_temperature": 45.93,
  "city": "London",
  "month": "December",
  "year": 2024
}
```
If the month and specified year is given, it will only give information for specific month. In case only month is selected, then it will select this year as default.\
*Example request - response:*\
`
/average/London?year=2023&month=12
`
```json
{
  "average_temperature": 100,
  "city": "London",
  "month": "December",
  "year": 2023
}
```

This is previous sample output but this time output is performed in csv format.\
*Example request - response:*\
`
/average/London?year=2023&month=12
`
```csv
City,Year,Month,Average Temperature
London,2023,December,100.0
```
   **Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 200  | Successful operation | [Weather Data ](#Weather Data) |
   | 400  | Path parameter not passed | None |
   | 404  | Path parameter not found | None |
   | 500  | Internal Server Error | None |

---

### **3.4 Precipitations**

Feature set endpoint: */precipitations/{city_name}* returns the amount of total precipitations per day of the specified parameter *month* (by default, current month) and retrieves data for every year this exact months' daily total precipitations. If the *year* is also selected when *month* selected, then it outputs exactly that months' and years'  daily total precipitations. If only year selected then it selects current month as default, prints this years' and current months' daily total precipitations.

##### **GET /precipitations/{city_name}**

Without any query parameters, the response will include the daily, total precipitations amount of the specified city in the current month for all years.\
*Example request - response:*\
`
/precipitations/london
`
```json
{
  "2023": {
    "December": [
      {
        "day": "01",
        "total_precipitation": 100
      }
    ]
  },
  "2024": {
    "December": [
      {
        "day": "01",
        "total_precipitation": 0
      },
      {
        "day": "02",
        "total_precipitation": 0
      }
    ]
  }
}
```

To get the precipitations amount of a selected month for every current year, the *month* parameter can be used.\
*Example request - response:*\
`
/precipitations/london?month=12
`

```json
{
  "2023": {
    "December": [
      {
        "day": "01",
        "total_precipitation": 100
      }
    ]
  },
  "2024": {
    "December": [
      {
        "day": "01",
        "total_precipitation": 0
      },
      {
        "day": "02",
        "total_precipitation": 0
      }
    ]
  }
}
```
To get the precipitations amount of a selected month and selected year, the *month*  and *year* parameter can be used.\
*Example request - response:*\
`
/precipitations/london?month=12&year=2023
`
```json
{
  "2023": {
    "December": [
      {
        "day": "01",
        "total_precipitation": 100
      }
    ]
  }
}
```
To get the precipitations amount of selected year and this time it selects month as default current month, only *year* parameter can be used.\
*Example request - response:*\
`
/precipitations/london?year=2024
`
```csv
Year,Month,Day,Total Precipitation
2024,December,01,0.0
2024,December,02,0.0
```

   **Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 200  | Successful operation | [Weather Data ](#Weather Data) |
   | 400  | Path parameter not passed | None |
   | 404  | Path parameter not found | None |
   | 500  | Internal Server Error | None |

---

### **3.5 Temperature Extremes**

The endpoint **/extremes** returns the maximum temperatures list in the case the top or bottom order. The **type** determines if top or bottom list of records to provide. If type is not determined, it will select top as default. The **N** parameter determines how many items should be included in the list. The **year** parameter determines the year the data should be based on and the **M** parameter enables the data to be based on multiple years (last x years specified in the period parameter, capped at the earliest available record). If both year and M parameters will be present in the request, the system will process the year and M period from that year. All aforementioned parameters are optinal and by default take the current values: order_desc=true, limit=1, year={current}, period=1.

##### **GET /extremes**

Included parameters, N=2 means show 2 records, for selected year 2024, and type=top means show top records.\

**/extremes?N=2&year=2024&type=top**


```json
[
  {
    "city_name": "London",
    "date_time": "2024-12-02 14:02:15",
    "temperature": 100
  },
  {
    "city_name": "bogota",
    "date_time": "2024-11-26 20:12:26",
    "temperature": 28.3
  }
]
```

Included parameters, N=3 means show 3 records, M=3 means for last 3 years and type=bottom means show bottom records.\

**/extremes?N=3&M=3&type=bottom**


```json
[
  {
    "city_name": "helsinki",
    "date_time": "2024-11-24 14:00:00",
    "temperature": 9.6
  },
  {
    "city_name": "newyork",
    "date_time": "2024-11-24 14:00:00",
    "temperature": 9.6
  },
  {
    "city_name": "london",
    "date_time": "2024-11-26 20:21:20",
    "temperature": 18.6
  }
]
```


Included parameters, N=3 means show 3 records and type=bottom means show top records. Also -H "Accept: text/csv" included to print in csv format.

  **/extremes?N=3&type=top**


  ```csv
  city_name,date_time,temperature
  London,2023-12-01 10:10:10,100.0
  London,2024-12-02 14:02:15,100.0
  bogota,2024-11-26 20:12:26,28.3
  ```

   **Response Codes**:
   | Code | Description | Schema |
   | ---- | ----------- | ------ |
   | 200  | Successful operation | [Weather Data ](#Weather Data) |
   | 400  | Path parameter not passed | None |
   | 404  | Path parameter not found | None |
   | 500  | Internal Server Error | None |

---
**Developed by:** s4058003, s5558727, s5622360\
**Date:** 24/11/2024\
**Version:** 1.0


