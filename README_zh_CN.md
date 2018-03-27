# 构建真正的 RESTful 应用

**表现层状态转移(REST)** 是一种结构风格，它基于 HTTP 定义了一组约束和属性。符合 RESTful 架构风格的 Web 服务使得 Internet 上计算机之间具有了互通性。符合 REST 的 Web 服务允许请求通过统一预定义的**无状态**操作来访问文本化的 Web 资源。

很长一段时间我只是在简单的使用 REST 服务的一部分。我只用了 **GET** 和 **POST** 方法来做一切事情，因为用起来实在太简单了。这种模式下，我所构建的 URL 是这样的：

```bash
# 使用 HTTP GET 来获取数据
http://example.com/{user_id}/
# 使用 HTTP POST 来更新数据
http://example.com/{user_id}/update
# 使用 HTTP GET 来删除数据
http://example.com/{user_id}/delete
```

我需要做的仅仅是利用 **GET** 或者 **POST** 请求一下上面的 URL，服务器会做好一切事情。

最近，我重新审视了 RESTful 的定义，并且感觉自己之前的做法并不是很合理。因为我仅仅用了 **GET**、**POST** 方法，完全忽视了 **PUT**、**PATCH**、**DELETE** 等方法。这也使得我的 URL 中包含了无用的字段。

事实上，RESTful 服务的 URL 应该是这样：

```bash
# 使用 HTTP GET 来获取数据
http://example.com/{user_id}/
# 使用 HTTP PUT 来更新数据
http://example.com/{user_id}/
# 使用 HTTP DELETE 来删除数据
http://example.com/{user_id}/
```

所以我产生了一个把这些示例写下来的想法，一方面是为了更好的掌握，另一方面也是为了将来能够在用到的时候方便查阅。

PS:

在 RESTful 服务中，身份验证是十分重要的。但是 HTTP 不能安全的传递密码信息，所以需要一个安全措施来保护我们的数据。最常用的做法是 **Token**，代码中会给出相关示例。

## 目录

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

生成与验证 Token:

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

生成与验证 Token：

```py
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def generate_token(self, expiration=3600):
    # default expiration time: 1 hour
    serializer = Serializer(Config.SECRET_KEY, expires_in=expiration)
    return serializer.dumps({
        'username': self.username
    })

@staticmethod
def verify_token(token):
    serializer = Serializer(Config.SECRET_KEY)
    try:
        data = serializer.loads(token) # type: dict
        return User.query.get(data.get('username'))
    except Exception as e:
        print(e)
        return None
```
