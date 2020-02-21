package com.ubiwhere.drevenmobileapi.client;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class OcppClient {
    @Value("${ocpp.url.idtag}")
    private String ocppUrlIdTag;

    @Value("${gateway.auth.user}")
    private String user;

    @Value("${gateway.auth.password}")
    private String password;

    @Value("${gateway.url}")
    private String gatewayURL;

    @Value("${gateway.url.ocp}")
    private String gatewayURLocp;

    @Autowired
    RestTemplate restTemplate;

    @Bean
    RestTemplate restGateway(RestTemplateBuilder restTemplateBuilder) {
        return restTemplateBuilder.basicAuthentication(user, password).build();
    }

    @Async
    public void createIdtTag(String idTag) {
        try {
            ResponseEntity<Map> getResponse = restTemplate.getForEntity(gatewayURL+gatewayURLocp, Map.class);
            Map responsebody = getResponse.getBody();
            List<Map> l = (List)responsebody.get("message");
            Map m = l.get(0);
            String ocpIpPort = (String)m.get("ocpIpPort");

            Map<String, String> body = new HashMap();
            body.put("idTag", idTag);

            ResponseEntity<Map> postResponse = restTemplate.postForEntity("http://"+ocpIpPort+ocppUrlIdTag, body, Map.class);        
	    log.info("Response code: {} body: {}", postResponse.getStatusCodeValue(), postResponse.getBody());
        } catch (Exception e) {
            log.error("", e);
        }
    }
}
