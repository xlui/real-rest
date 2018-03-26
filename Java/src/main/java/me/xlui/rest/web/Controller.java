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
