module.exports = {
    type: "credentials",
    users: function (username) {
        return new Promise(function (resolve) {
            // Do whatever work is needed to check username is a valid
            // user.
            if (username != null) {
                // Resolve with the user object. It must contain
                // properties 'username' and 'permissions'
                var user = { username: username, permissions: "*" };
                resolve(user);
            } else {
                // Resolve with null to indicate this user does not exist
                resolve(null);
            }
        });
    },
    authenticate: function (username, password) {
        const request = require("request");

        let URL = process.env.AITENEA_URL_BACKEND + "/api/auth/login/";
        const data = {
            username: username,
            password: password,
        };

        let opts = {
            method: 'POST',
            url: URL,
            timeout: 5000,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        };

        return new Promise(function (resolve) {
            request.post(opts, function (error, response, body) {
                // Do whatever work is needed to validate the username/password
                // combination.
                if (error != null) {
                    console.error('error:', error); // Print the error if one occurred
                    resolve(null);
                }
                else {
                    let body_json = JSON.parse(body)
                    if (body_json.hasOwnProperty('token')) {
                        let user = { username: body_json["user"]["username"], permissions: "*" };
                        resolve(user);
                    }
                    else {
                        resolve(null);
                    }
                }
            });
        });
    },
    default: function () {
        return new Promise(function (resolve) {
            // Resolve with the user object for the default user.
            // If no default user exists, resolve with null.
            resolve(null);
        });
    }
}
