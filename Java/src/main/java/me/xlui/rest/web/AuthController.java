package me.xlui.rest.web;

import me.xlui.rest.entity.User;
import me.xlui.rest.repository.UserRepository;
import me.xlui.rest.util.JWTUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class AuthController {
	@Autowired
	private UserRepository userRepository;

	@RequestMapping(value = "/login", method = RequestMethod.POST)
	public String login(@RequestBody User user) {
		User target = userRepository.findByUsername(user.getUsername());
		if (target == null) {
			return "Username is invalid!";
		}
		if (target.getPassword().equals(user.getPassword())) {
			return JWTUtils.sign(user.getUsername(), user.getPassword());
		} else {
			return "Password is incorrect!";
		}
	}

	@RequestMapping(value = "/verify", method = RequestMethod.GET)
	public String verify(@RequestParam(value = "token") String token) {
		String username = JWTUtils.getUsername(token);
		User user = userRepository.findByUsername(username);
		if (user == null) {
			return "Invalid token!";
		} else {
			boolean result = JWTUtils.verify(token, user.getUsername(), user.getPassword());
			if (result) {
				return "Successfully login!";
			} else {
				return "Error! Token auth failed!";
			}
		}
	}
}
