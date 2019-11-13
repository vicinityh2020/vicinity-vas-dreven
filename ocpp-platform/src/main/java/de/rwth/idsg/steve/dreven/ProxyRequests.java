package de.rwth.idsg.steve.dreven;

import com.fasterxml.jackson.databind.ObjectMapper;
import de.rwth.idsg.steve.SteveConfiguration;
import de.rwth.idsg.steve.repository.ChargePointRepository;
import de.rwth.idsg.steve.repository.TransactionRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class ProxyRequests {
    @Autowired
    RestTemplate restTemplate;
    @Autowired
    ObjectMapper mapper;

    @Autowired
    ChargePointRepository chargePointRepository;

    @Autowired
    TransactionRepository transactionRepository;

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public ObjectMapper mapper() {
        return new ObjectMapper();
    }

    @Async("threadPoolTaskExecutor")
    public void proxyRequests(String chargeBoxId, String incomingString) {
        try {
            List<Integer> txIds = transactionRepository.getTransactionIds(chargeBoxId);
            String idTag = "";

            if(!txIds.isEmpty()){
                Integer txId = txIds.get(0);
                idTag = transactionRepository.getDetails(txId).getTransaction().getOcppIdTag();
            }

            Map<String, Integer> idPks  = chargePointRepository.getChargeBoxIdPkPair(List.of(chargeBoxId));
            String vicinityoid = chargePointRepository.getDetails(idPks.get(chargeBoxId)).getChargeBox().getDescription();
            log.info("Proxing request {} {} {} {}", chargeBoxId, vicinityoid, idTag, incomingString);
            List<Object> json = mapper.readValue(incomingString, List.class);
            json.add(chargeBoxId);
            json.add(vicinityoid);
            json.add(idTag);
            ResponseEntity<List> postResponse = restTemplate.postForEntity(SteveConfiguration.CONFIG.getDrevenMiddlewareUrl(), json, List.class);
            log.info("Response code: {} body: {}", postResponse.getStatusCodeValue(), postResponse.getBody());
        } catch (Exception e) {
            log.error("", e);
        }
    }
}