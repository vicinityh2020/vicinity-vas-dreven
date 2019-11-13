package com.ubiwhere.drevenmiddleware.client;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.text.MessageFormat;
import java.util.Map;

@Slf4j
@Component
public class GatewayClient {
    @Value("${gateway.auth.infrastructure-id}")
    private String infrastructureId;

    @Value("${gateway.auth.adapter-id}")
    private String adapterId;

    @Value("${gateway.auth.user}")
    private String user;

    @Value("${gateway.auth.password}")
    private String password;

    @Value("${gateway.url}")
    private String gatewayURL;

    @Value("${gateway.url.starttx}")
    private String gatewayURLStartTX;

    @Value("${gateway.url.stoptx}")
    private String gatewayURLStopTX;

    @Value("${gateway.url.status}")
    private String gatewayURLStatus;

    @Value("${gateway.url.metervalue}")
    private String gatewayURLMeterValue;

    @Autowired
    @Qualifier("restGateway")
    RestTemplate restTemplate;

    @Bean
    RestTemplate restGateway(RestTemplateBuilder restTemplateBuilder) {
        return restTemplateBuilder.basicAuthentication(user, password).build();
    }

    public void putStartTX(String chargeBoxId, long ts) {
        put(chargeBoxId, gatewayURLStartTX, Map.of("lastStartTransaction",ts));
    }

    public void putStopTX(String chargeBoxId, long ts) {
        put(chargeBoxId, gatewayURLStopTX, Map.of("lastStopTransaction", ts));
    }

    public void putSatus(String chargeBoxId, String status) {
        put(chargeBoxId, gatewayURLStatus, Map.of("status", status));
    }

    public void putMeterValue(String chargeBoxId, String value) {
        put(chargeBoxId, gatewayURLMeterValue, Map.of("meterValue", value));
    }

    //curl --anyauth --user "1d2f666d-9281-4498-b548-acd4d6112f5f":"i3nK4+WMPbOw3DPlN9Y0pXKqZwpgqifhH/egh3I/KE8=" -d "{\"lastStartTransaction\":1569943521223}" -H "infrastructure-id: OCPP" -H "adapter-id: EVCharger-adapter" -H "Content-Type: application/json" -X PUT http://192.168.2.110:8181/api/objects/b9c75610-2ef0-43e9-861d-add06d6a5759/properties/lastStartTransaction
    @Async("threadPoolTaskExecutor-gw")
    public void put(String chargeBoxId, String relativeurl, Map body) {
        String url = MessageFormat.format(gatewayURL+relativeurl, chargeBoxId);

        HttpHeaders headers = new HttpHeaders();
        headers.set("gateway.auth.infrastructure-id", infrastructureId);
        headers.set("gateway.auth.adapter-id", adapterId);

        HttpEntity<Map> request = new HttpEntity<>(body, headers);

        log.debug("Put to {} with {}", url, body);
        ResponseEntity<Map> response = restTemplate.exchange(url, HttpMethod.PUT, request, Map.class);
        log.debug("Response for {} with {} is {}", url, body, response);
    }
}
