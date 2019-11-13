package com.ubiwhere.drevenmobileapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class DrevenMobileApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(DrevenMobileApiApplication.class, args);
	}

}
