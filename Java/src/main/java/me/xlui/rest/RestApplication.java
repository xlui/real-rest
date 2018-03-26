package me.xlui.rest;

import me.xlui.rest.entity.User;
import me.xlui.rest.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class RestApplication implements CommandLineRunner {
	@Autowired
	private UserRepository userRepository;

	public static void main(String[] args) {
		SpringApplication.run(RestApplication.class, args);
	}

	@Override
	public void run(String... strings) throws Exception {
		User user = new User("1", "dev");
		userRepository.save(user);
		System.out.println("Init user success!");
	}
}
