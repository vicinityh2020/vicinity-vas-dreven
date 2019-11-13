package com.ubiwhere.drevenmiddleware;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@SpringBootApplication
@EnableAsync
public class DrevenMiddlewareApplication {

	@Bean("threadPoolTaskExecutor-gw")
	public TaskExecutor getAsyncExecutorGateway() {
		ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
		executor.setCorePoolSize(1); //TODO: handle unordered messages?
		executor.setMaxPoolSize(1);
		executor.setQueueCapacity(500);
		executor.setWaitForTasksToCompleteOnShutdown(true);
		executor.setThreadNamePrefix("Async-gw");
		return executor;
	}

	@Bean("threadPoolTaskExecutor-msp")
	public TaskExecutor getAsyncExecutorMsp() {
		ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
		executor.setCorePoolSize(1); //TODO: handle unordered messages?
		executor.setMaxPoolSize(1);
		executor.setQueueCapacity(500);
		executor.setWaitForTasksToCompleteOnShutdown(true);
		executor.setThreadNamePrefix("Async-msp");
		return executor;
	}

	public static void main(String[] args) {
		SpringApplication.run(DrevenMiddlewareApplication.class, args);
	}
}
