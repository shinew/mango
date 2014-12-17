This API reference is organized by resource type. URIs relative to https://api.getbeyond.me/v2.0/users, unless otherwise noted.

# Sensors #
## Sending Sensor Data ##
HTTP Request: POST /{userID}/sensors

Description: Sends sensor data for a user to our servers, so stress score requests can be handled.

### Request Body ###
In the request body, supply an array of sensor resources with the following properties:

Property name | Value | Description
:--- | :--- | :---
sensorType | string | The type of sensor. Acceptable values are: `"heartRate"`, `"hrv"` (heart rate variability).
time | string | The time when the sensor data was recorded. Format should conform to `"yyyy-MM-dd HH:mm:ss"`.
value | int or array of ints | If sensorType is `"heartRate"`, this is an int measured in beats/min. If sensorType is `"hrv"`, this is an array of ints measured in ms.

### Response ###
Returns 200 if the data was accepted. Returns 400 if the data could not be accepted (generally due to incorrect format).

### Example ###
```json
{
    "resources": [
        {
            "sensorType": "hr",
            "time": "2014-11-21 16:55:22",
            "value": 65
        },
        {
            "sensorType": "hrv",
            "time": "2014-11-21 16:55:22",
            "value": [1034, 938]
        }
    ]
}
```

# Scores #
## Retrieving Stress Scores ##

HTTP Request: POST /{userID}/scores

Description: Retrieves a stress score for a user at a specific point in time. It is necessary for about 5 minutes' worth of heart rate and HRV data to be sent in the prior time interval.

### Request Body ###
In the request body, supply the time and format of the score with the following fields:

Property name | Value | Description
:--- | :--- | :---
time | string | The time of the stress score. Format should conform to `"yyyy-MM-dd HH:mm:ss"`.
format | string | The format for the response. Acceptable values are: `"state"`, `"score"`.

### Response body ###
If the request was successful, returns 200 and JSON payload with either one of the the following fields, depending on the format field in the request body:

Property name | Value | Description
:--- | :--- | :---
state | string/null | The stress state of a user. Values are: `"calm"`, `"tense"`, or `"stressed"`. If a score could not be calculated due to insufficient data, null will be returned.
score | int/null | The stress score of a user. Scores will be between 0 - 100 inclusive, where 0 is very calm and 100 is very stressed. If a score could not be calculated, null will be returned.

### Example ###
Request:
```json
{
    "time": "2014-11-21 16:55:22",
    "format": "state"
}
```

Response:
```json
{
    "state": "calm"
}
```
```json
{
    "score": null
}
```
