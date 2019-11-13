package de.rwth.idsg.steve.rest.controller;

import de.rwth.idsg.steve.ocpp.OcppTransport;
import de.rwth.idsg.steve.repository.ChargePointRepository;
import de.rwth.idsg.steve.repository.OcppTagRepository;
import de.rwth.idsg.steve.repository.TransactionRepository;
import de.rwth.idsg.steve.repository.dto.ChargePointSelect;
import de.rwth.idsg.steve.service.ChargePointService12_Client;
import de.rwth.idsg.steve.service.ChargePointService16_Client;
import de.rwth.idsg.steve.web.dto.Address;
import de.rwth.idsg.steve.web.dto.ChargePointForm;
import de.rwth.idsg.steve.web.dto.OcppTagForm;
import de.rwth.idsg.steve.web.dto.ocpp.RemoteStopTransactionParams;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.LinkedList;
import java.util.List;
import java.util.Map;

@Controller
@Slf4j
public class DrevenController {
    @Autowired
    OcppTagRepository ocppTagRepository;

    @Autowired
    ChargePointRepository chargePointRepository;

    @Autowired
    TransactionRepository transactionRepository;

    @Autowired
    @Qualifier("ChargePointService16_Client")
    private ChargePointService16_Client client16;

    @PostMapping(path = "/ocppTag", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public Map<String, Integer> addTag(@RequestBody OcppTagForm form) {
        return Map.of("id", ocppTagRepository.addOcppTag(form));
    }

    @PatchMapping(path = "/ocppTag", consumes = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public void updateTag(@RequestBody OcppTagForm form) {
        ocppTagRepository.updateOcppTag2(form);
    }

    @PostMapping(path = "/chargePoint", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public Map<String, Integer> addChargePoint(@RequestBody ChargePointForm form) {
        form.setAddress(new Address());
        return Map.of("id", chargePointRepository.addChargePoint(form));
    }

    @PatchMapping(path = "/transaction", consumes = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public void stopTransaction(@RequestBody ChargePointForm form) {
        String chargeBoxId = chargePointRepository.getChargeBoxId(form.getDescription());
        Integer txid = transactionRepository.getActiveTransactionIds(chargeBoxId).get(0);
        RemoteStopTransactionParams remoteStopTransactionParams = new RemoteStopTransactionParams();
        remoteStopTransactionParams.setTransactionId(txid);
        ChargePointSelect cps = new ChargePointSelect(OcppTransport.JSON, chargeBoxId);
        List<ChargePointSelect> l = new LinkedList<>();
        l.add(cps);
        remoteStopTransactionParams.setChargePointSelectList(l);
        client16.remoteStopTransaction(remoteStopTransactionParams);
    }
}
