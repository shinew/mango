# Introduction #
The Beyond API is a RESTful API that can be used to access Beyond Intelligence's proprietary stress assessment algorithms.

## API Overview ##
The Beyond API is a web service: it uses a RESTful API with a JSON payload. This section provides a general overview of the API features and their use. For detailed information on the API's resources and methods, refer to Beyond API reference.

### Key resources ###
The Beyond API provides two primary resource types:
* Sensors
* Scores

**Sensors** represent the raw sensor data, such as heart rate variability, body movement, and electrodermal activity. These can only be created, and not modified or deleted after creation.

**Scores** are the stress scores of a user at a specific point in time, given sufficient sensory data in the time interval ending at the time.

### Authentication ###

Currently, the Beyond API uses passwords to control access and modification for individual users. In the future, it will use OAuth 2.0 to handle authentication and authorization.

### Example use cases ###
Consider the following use case: play music based on the user's stress state. To achieve this, your app would perform the following steps:

1. Ensure that the Beyond app is opening in the background to collect heart rate data.
2. Call the API method /scores to learn whether the user is calm or stressed.
3. Play invigorating music if the user is feeling calm, or play calming music is the user is feeling stressed.

Another use case: send a notification if the user is stressed. To achieve this, do as follows:

1. Call the API method /sensors to send sufficient data so Beyond algorithms can calculate a stress score.
2. Call the API method /scores to learn whether the user is calm or stressed.
3. Send a notification if the user is stressed.