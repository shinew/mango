# README # This is the web framework for our server backend at Beyond.

## General Notes ##
All requests sent to the server should have header `Content-type: application/json`. All fields must be sent, and optional fields can be sent with value of `null`. Encoding should be UTF-8. If authentication (for those endpoints that require it) fails, a response code of 400 would be sent.

## Interacting with Kiwi ##
The workflow of a client that wants to interact with the server is as follows:

### User Creation ###
Create a new user by sending a PUT request to [/user/add](http://devapi.getbeyond.me/v1.0/user/add) with fields of *UserName* and *Password*. For example:
```
#!json
{
    "UserName": "shine",
    "Password": "password"
}
```
Returns a response code of `201`, and the new user's ID number (as JSON in `{"ID": 9000}`) if the creation was successful. If not (i.e. username taken), returns `403`.

Note: The client should hash the password beforehand to prevent request interception (we don't store the password as plaintext server-side).

### User Verification ###
Verifies that an (ID, password) pair exists on our server by sending a POST request to [/user/verify](http://devapi.getbeyond.me/v1.0/user/verify) with fields of *UserID* and *Password*. For example:
```
#!json
{
    "UserID": 1,
    "Password": "password"
}
```
Returns a `200` if the pair exists. Otherwise returns a `403`.

### Sending Heart Rate Data ###
Send some heart rate data to our server with a PUT request to [/heart](http://devapi.getbeyond.me/v1.0/heart). The format is a bit complicated, and best explained with an example:
```
#!json
{
	"ID": 1,
	"Password": "password",
	"Samples": [{
		"Device": "Wahoo TICKR",
		"Time": "2014-11-27 16:22:33",
		"Movement": false,
		"HR": 69,
		"HRV": [654, 805]
	}]
}
```
Returns a response code of `201` if successful.

Note: The payload has a field called *Samples*, which corresponds with the data format of current devices. This allows for batched sending of device data (over 30s intervals rather than per second). Also, *HR* and *HRV* are optional fields (as we're not sure if all devices have this information), but don't bother sending any requests with both `null`. Finally, *HRV* is an `Array` because multiple heartbeats can occur within a second, while *HR* is a `Number` because it is the average heart rate over that second.

### Asking for Stress Score ###
Query for the stress score over the time period with a POST request to [/score](http://devapi.getbeyond.me/v1.0/score). Send with fields of *ID*, *Password*, *StartTime*, and *EndTime*. Example:
```
#!json
{
	"ID": 1,
	"Password": "password",
	"StartTime": "2014-11-27 16:22:33",
	"EndTime": "2014-11-27 16:26:33"
}
```
Returns a response code of `200` and the stress score (as JSON in `{"Score": 75}`) if the calculation was succcessful. Returns `428` if not.

Note: It is the client's responsibility to make sure sufficient and consistent heart rate data has been sent over that time period. Usually, a lower bound of 250 HRV intervals is required for a meaningful score.


### (Bonus) Sending Training Intervals ###
Training intervals for our machine learning algorithm can be added by specifying an interval with a PUT request to [/training](http://devapi.getbeyond.me/v1.0/training). For example, to add a "relaxed" training interval:
```
#!json
{
    "ID": 1,
	"Password": "password",
	"StartTime": "2014-11-27 16:22:33",
	"EndTime": "2014-11-27 16:26:33",
    "Category": 1,
    "IsDefaultSet": false 
}
```
*Category* is defined as: `1` = relaxed, `2` = stressed. *IsDefaultSet* is set to `true` if you want to use this interval to train other users' scores. This should be set to `false` for most cases (besides migration).

### (Bonus) Bulk Interval Retrieval ###
When a user logs into a new device, he would like to see his recent data. To faciliate this, send a POST request to [/score/bulk](http://devapi.getbeyond.me/v1.0/score/bulk). The spec is the same as for [/score](http://devapi.getbeyond.me/v1.0/score). Returns JSON as in:

```
#!json
{
    "Scores": [
        {
            "Score": 6,
            "StartTime": "2014-11-20 12:33:45",
            "EndTime": "2014-11-20 12:36:45"
        },
        ...
    ]
}
```

Note: It is the client's responsibility that these scores were previously calculated using [/score](http://devapi.getbeyond.me/v1.0/score).

### (Bonus) Metrics ###
For debugging purposes, you can view some metrics when you go to [/metrics](http:/devapi.getbeyond.me/v1.0/metrics). *Last Scores* are the last 5 intervals generated in the last hour. *User Counts* shows how many scores each user generated in the last hour.