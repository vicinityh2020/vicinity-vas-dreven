package com.ubiwhere.drevenmiddleware.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ubiwhere.drevenmiddleware.client.GatewayClient;
import com.ubiwhere.drevenmiddleware.client.MspClient;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.Map;

@Service
@Slf4j
public class MiddlewareService {
    @Autowired
    ObjectMapper mapper;

    @Autowired
    GatewayClient gwClient;

    @Autowired
    MspClient mspClient;

    @Value("${gateway.metervalue.measurand}")
    private String gatewayMeterValueMeasurand;

    public void createOCPPReq(Object[] OCPPReq) {
        if(OCPPRequest.validOCCPRequest(OCPPReq)) {
           OCPPRequest or = new OCPPRequest(OCPPReq);
           switch (or.action) {
               case OCPPRequest.STARTTRANSACTION:
                   gwClient.putStartTX(or.chargeBoxId, or.getTimestamp());
                   mspClient.postStartTX(or.getIdTag(),  or.vicinityOid, or.getMeterStart());
                   break;
               case OCPPRequest.STOPTRANSACTION:
                   gwClient.putStopTX(or.chargeBoxId, or.getTimestamp());
                   mspClient.postStopTX(or.getIdTag(),  or.vicinityOid, or.getMeterStop());
                   break;
               case OCPPRequest.STATUSNOTIFICATION:
                   gwClient.putSatus(or.chargeBoxId, or.getStatus());
                   break;
               case OCPPRequest.METERVALUES:
                   String value = or.getMeterValue(gatewayMeterValueMeasurand);
                   if(value == null) {
                       log.warn("Measurand: {} not found in {}", gatewayMeterValueMeasurand,  Arrays.toString(OCPPReq));
                   } else {
                       gwClient.putMeterValue(or.chargeBoxId, value.replaceAll("\\D", ""));
                       mspClient.putMeterValue(or.outerIdTag, or.vicinityOid, Long.valueOf(value.replaceAll("\\D", "")));
                   }
                   break;
               default:
                   log.warn("Request type not implemented {}",  Arrays.toString(OCPPReq));
           }
        } else {
            log.warn("Received invalid request {}",  Arrays.toString(OCPPReq));
        }
    }
}
