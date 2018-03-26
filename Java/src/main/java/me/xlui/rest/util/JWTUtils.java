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
