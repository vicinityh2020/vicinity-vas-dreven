package com.ubiwhere.drevenmiddleware.service;

import java.time.Instant;
import java.util.List;
import java.util.Map;

public class OCPPRequest {
    // [2,"1","MeterValues",{"connectorId":1,"meterValue":[{"timestamp":"2019-10-01T10:12:13.0477583Z","sampledValue":[{"value":"10","measurand":"Current.Import","unit":"A"}]}]}]
    // [2,"6","StopTransaction",{"transactionId":1,"idTag":"04EC2CC2552280","timestamp":"2019-10-01T10:12:20.424965Z","meterStop":310}]
    // [2,"4","StatusNotification",{"connectorId":1,"status":"Charging","errorCode":"NoError","timestamp":"2019-10-01T10:12:14.6287944Z"}]
    // [2,"3","StartTransaction",{"connectorId":1,"idTag":"04EC2CC2552280","timestamp":"2019-10-01T10:12:14.3072324Z","meterStart":300}]

    public static final String STARTTRANSACTION = "StartTransaction";
    public static final String STOPTRANSACTION = "StopTransaction";
    public static final String STATUSNOTIFICATION = "StatusNotification";
    public static final String METERVALUES = "MeterValues";

    Integer MessageTypeId;
    String uniqueId;
    String action;
    Map payload;
    String chargeBoxId;
    String vicinityOid;
    String outerIdTag;

    public OCPPRequest(Object[] OCPPReq) {
        MessageTypeId = (Integer)OCPPReq[0];
        uniqueId = (String)OCPPReq[1];
        action = (String)OCPPReq[2];
        payload = (Map)OCPPReq[3];
        chargeBoxId = (String)OCPPReq[4];
        vicinityOid = (String)OCPPReq[5];
        outerIdTag = (String)OCPPReq[6];
    }

    public static boolean validOCCPRequest(Object[] OCPPReq){
        return OCPPReq.length == 7 &&
                OCPPReq[0] instanceof Integer &&
                OCPPReq[1] instanceof String &&
                OCPPReq[2] instanceof String &&
                OCPPReq[3] instanceof Map &&
                OCPPReq[4] instanceof String &&
                OCPPReq[5] instanceof String &&
                OCPPReq[6] instanceof String;
    }

    public long getTimestamp() {
        return Instant.parse((String)payload.get("timestamp")).toEpochMilli();
    }

    public String getStatus() {
        String status = (String)payload.get("status");
        return status;
    }

    public String getIdTag() {
        String idTag = (String)payload.get("idTag");
        return idTag;
    }

    public long getMeterStart(){
        Object v = payload.get("meterStart");
        if(v instanceof Integer) {
            return (Integer)v;
        } else {
            return (Long)v;
        }
    }

    public long getMeterStop(){
        Object v = payload.get("meterStop");
        if(v instanceof Integer) {
            return (Integer)v;
        } else {
            return (Long)v;
        }
    }

    public String getMeterValue(String gatewayMeterValueMeasurand) {
        List<Map> meterValues = (List)payload.get("meterValue");
        for(Map mv: meterValues){
            List<Map> sampledValues = (List<Map>)mv.get("sampledValue");
            for(Map sv: sampledValues) {
                String measurand = (String)sv.getOrDefault("measurand", "Energy.Active.Import.Register");
                if(measurand.equals(gatewayMeterValueMeasurand)) {
                    return (String)sv.get("value");
                }
            }
        }
        return null;
    }
}
