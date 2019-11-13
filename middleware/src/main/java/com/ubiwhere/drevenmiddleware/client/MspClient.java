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
public class MspClient {

    @Value("${msp.url}")
    private String mspURL;

    @Value("${msp.url.starttx}")
    private String mspURLStartTX;

    @Value("${msp.url.stoptx}")
    private String mspURLStopTX;

    @Value("${msp.url.metervalue}")
    private String mspURLMeterValue;

    @Autowired
    @Qualifier("restMsp")
    RestTemplate restTemplate;

    @Bean
    RestTemplate restMsp(RestTemplateBuilder restTemplateBuilder) {
        return restTemplateBuilder.build();
    }

    public void postStartTX(String idTag, String vicinityOid, long meterValueWh) {
        Map body = Map.of("meterValue", meterValueWh,
                          "vicinityOid", vicinityOid,
                          "idTag", idTag);
        post(mspURLStartTX, body);
    }

    public void postStopTX(String idTag, String vicinityOid, long meterValueWh) {
        Map body = Map.of("meterValue", meterValueWh,
                          "vicinityOid", vicinityOid,
                          "idTag", idTag);
        post(mspURLStopTX, body);
    }

    @Async("threadPoolTaskExecutor-msp")
    public void post(String relativeurl, Map body) {
        String url = mspURL+relativeurl;

        log.debug("Post to {} with {}", url, body);
        ResponseEntity<Map> response = restTemplate.postForEntity(url, body, Map.class);
        log.debug("Response for {} with {} is {}", url, body, response);
    }

    @Async("threadPoolTaskExecutor-msp")
    public void putMeterValue(String idTag, String vicinityOid, long meterValueWh) {
        String url = mspURL+mspURLMeterValue;
        Map body = Map.of("meterValue", meterValueWh,
                "vicinityOid", vicinityOid,
                "idTag", idTag);

        HttpEntity<Map> request = new HttpEntity<>(body);

        log.debug("Put to {} with {}", url, body);
        ResponseEntity<Map> response = restTemplate.exchange(url, HttpMethod.PUT, request, Map.class);
        log.debug("Response for {} with {} is {}", url, body, response);
    }
}
