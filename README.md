# Build Real RESTful Application

**REpresentational State Transfer(REST)** is an architectural style that defines a set of constraints and properties based on [HTTP](https://en.wikipedia.org/wiki/HTTP). Web Services that confirm to the REST architectural style, or **RESTful** web services provide interoperability between computer systems on the Internet. REST-compliant web services allow the requesting systems to access and manipulate textual representations of web resources by using a uniform and predefined set of [stateless](https://en.wikipedia.org/wiki/Stateless_protocol) operations.

For a long time I'm using REST service hastily. I'm just using method **GET** and **POST** for almost every thing such as **UPDATE**, **DELETE**. In this way, the url I built is likes this:

```bash
# for GET, using HTTP GET to request
http://example.com/{user_id}/
# for UPDATE, using HTTP POST to request
http://example.com/{user_id}/update
# FOR DELETE, using HTTP GET to request
http://example.com/{user_id}/delete
```

All things I need to do is to request the url, and the server will do it well.

Recently, I have reviewed that what RESTful service is. And I was surprised to find that other HTTP method such as **PUT**, **PATCH**, **DELETE** was deprecated because of my ignorant.

Actually, RESTful service should be represented as follows:

```bash
# for GET, using HTTP GET to request
http://example.com/{user_id}/
# for UPDATE, using HTTP PUT to request
http://example.com/{user_id}/
# FOR DELETE, using HTTP DELETE to request
http://example.com/{user_id}/
```

So it comes to me an idea that to write them out. Write out is a good way to have these concepts in my hand. Also, write out will make them an example for the future development.

PS:

In RESTful Services, auth is very import. And we all know that http is not safe for password transfer, so we need to find a way to protect our data. The most common way is **Token**, some examples will show how to use. 

## Table of Contents

- [中文](README_zh_CN.md)
- [Java Spring version](#java-spring-version)
- [Python Flask version](#python-flask-version)

## Java Spring Version

See the code:

```java
package me.xlui.rest.web;

import me.xlui.rest.entity.User;
import me.xlui.rest.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class Controller {
    @Autowired
    private UserRepository userRepository;

    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public User getUsername(@PathVariable Long id) {
        return userRepository.findById(id);
    }

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public List<User> get() {
        return userRepository.findAll();
    }

    @RequestMapping(value = "/", method = RequestMethod.POST)
    public User post(@RequestBody User user) {
        User newUser = new User(user.getUsername(), user.getPassword());
        return userRepository.save(newUser);
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.PUT)
    public User put(@PathVariable Long id, @RequestBody User user) {
        User currentUser = userRepository.findById(id);
        currentUser.setUsername(user.getUsername());
        currentUser.setPassword(user.getPassword());
        return userRepository.save(currentUser);
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.PATCH)
    public User patch(@PathVariable Long id, @RequestBody User user) {
        User currentUser = userRepository.findById(id);
        if (user.getUsername() != null) {
            currentUser.setUsername(user.getUsername());
        }
        if (user.getPassword() != null) {
            currentUser.setPassword(user.getPassword());
        }
        return userRepository.save(currentUser);
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.DELETE)
    public void delete(@PathVariable Long id) {
        userRepository.delete(id);
    }
}
```

Token generate and verify:

```java
package me.xlui.rest.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;

import java.time.Duration;
import java.util.Date;

public class JWTUtils {
	public static boolean verify(String token, String username, String password) {
		Algorithm algorithm = Algorithm.HMAC256(password.getBytes());
		JWTVerifier verifier = JWT.require(algorithm)
				.withClaim("username", username)
				.build();
		try {
			verifier.verify(token);
			return true;
		} catch (Exception e) {
			return false;
		}
	}

	public static String getUsername(String token) {
		try {
			DecodedJWT decodedJWT = JWT.decode(token);
			return decodedJWT.getClaim("username").asString();
		} catch (Exception e) {
			return null;
		}
	}

	public static String sign(String username, String password) {
		Algorithm algorithm = Algorithm.HMAC256(password.getBytes());
		try {
			return JWT.create()
					.withClaim("username", username)
					.withExpiresAt(new Date(expire()))
					.sign(algorithm);
		} catch (Exception e) {
			return null;
		}
	}

	private static long expire() {
		return System.currentTimeMillis() + Duration.ofDays(1).toMillis();
	}
}
```

## Python Flask Version

See the code:

```py
from flask import Flask, request, jsonify

from app import db
from app.models import User
from app.my_exception import MyException
from conf.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    json = [user.get_json() for user in users]
    return jsonify(json)


@app.route('/<user_id>', methods=['GET'])
def get_one(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(user.get_json())
    else:
        raise MyException('user id is invalid!')


@app.route('/', methods=['POST'])
def post():
    if not request.json or not ('username' in request.json and 'password' in request.json):
        raise MyException('request payload must be JSON format and ALL field off entity `user` should be included!')
    user = User.query.get(request.json.get('username'))
    if user:
        raise MyException('username already exist!')
    else:
        user = User(username=request.json.get('username'),
                    password=request.json.get('password'))
        db.session.add(user)
        db.session.commit()
        return jsonify(user.get_json())


@app.route('/<user_id>', methods=['PUT'])
def put(user_id):
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        raise MyException('request payload must be JSON format and all field off entity `user` should be included!')
    user = User.query.get(user_id)
    if user:
        user.username = request.json.get('username')
        user.password = request.json.get('password')
        return jsonify(user.get_json())
    else:
        raise MyException('user id is invalid!')


@app.route('/<user_id>', methods=['PATCH'])
def patch(user_id):
    if not request.json:
        raise MyException('request payload must be JSON format!')
    user = User.query.get(user_id)
    if user:
        # check username or password is contained or not
        username = request.json.get('username')
        password = request.json.get('password')
        if not username and not password:
            raise MyException('At least include one field off entity `user`!')

        if username:
            user.username = username
        if password:
            user.password = password
        return jsonify(user.get_json())
    else:
        print('User id is invalid!')
        raise MyException('user id is invalid!', 400)


@app.route('/<user_id>', methods=['DELETE'])
def delete(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        return jsonify({
            'message': 'Successfully delete user {id}'.format(id=user_id)
        })
    else:
        raise MyException('user id is invalid!')


@app.errorhandler(MyException)
def handle_my_exception(error: MyException):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run()
```