**Login**
----
  Returns user data that identifies a single user for future requests

* **URL**

  /auth/login

* **Method:**

  `POST`
  
*  **Parameters**

   **Required:**
   `email=[string:regex(^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$)]` (user's email address; must match regex) <br />
   `password=[string:max(64)]` (the user's plain-text password; must be less than 64 characters) <br />
   
   **Optional:**
   `should_expire=[integer:0:1]` (should the token expire after 30 minutes; 0 for no; 1 or empty for yes)
   
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `
    ```json
    { 
    	"id": [integer:primary_key],
        "first_name": [string:max(64)],
        "last_name": [string:max(64)],
        "email": [string:max(128)],
        "bearer_token": [string],
        "expires_at": [date_time:optional]
	}
	```
 
* **Error Responses:**

  * **Code:** 400 BAD REQUEST <br />
  **Content:** `{ "error" : [string] }` (if email or password are missing)

  OR
  
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ "error" : [string] }` (if email or password do not match)

  OR
  
  * **Code:** 422 UNPROCESSABLE ENTITY <br />
    **Content:** `{ "error" : [string] }` (if the email or password look invalid)

    
* **Sample Call:**

  ```javascript
    request({
        uri: 'myapp.com',
        method: 'POST',
        json: {
          "email": "abc1234@psu.edu",
          "password": "password123"
        }
      }, function (error, response, body) {
        if (!error && response.statusCode == 200) {
          // Handle the error.
        }
      
        // Otherwise, do something with data
      }
    );
  ```
  
* **Notes:**

  * The `bearer_token` is unique to the user and is randomly regenerated every time the user logs in. 
  It should be a random string of random length that proves you are logged in. You will need to save this token every time it is sent to you.
  
  * The `id` is the primary key. It is automatically generated by MySQL and is the next available ID.

  * The `should_expire` parameter should only be included if the token should **not** expire until the user logs in on a new device.

  * The `expires_at` response content will only be returned if the content has an expiration (secret key could still change at some point).