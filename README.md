#Operation can be performed via terminal

curl -X GET "http://localhost:6969/weather/all"                         
curl -X DELETE "http://localhost:6969/weather/del"
curl -X POST "http://localhost:6969/daily/helsinki" -H "Content-Type: application/json" -d '{"temperature": 9.6}'
curl -X GET "http://localhost:6969/daily/helsinki" -H "Accept: text/csv"
curl -X GET "http://localhost:6969/daily/helsinki?show_city_name=true&show-date-time=true&show-precipitation=true"
curl -X GET "http://localhost:6969/daily/helsinki?time-offset=2"
curl -X GET "http://localhost:6969/daily/helsinki"

For post requests, csv type might be added
for get add if statements for printing csv output
 
