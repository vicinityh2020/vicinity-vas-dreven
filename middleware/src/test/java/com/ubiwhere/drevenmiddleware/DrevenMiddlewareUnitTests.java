package com.ubiwhere.drevenmiddleware;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ubiwhere.drevenmiddleware.service.OCPPRequest;
import org.junit.BeforeClass;
import org.junit.Test;

import javax.validation.constraints.AssertTrue;

import static org.junit.Assert.*;

import java.io.IOException;

public class DrevenMiddlewareUnitTests {

	private static Object[] invalidMsgIncorrectSize;

	private static Object[] validMeterValuesWithoutWh;
	private static Object[] validMeterValuesWithDefault;
	private static Object[] validMeterValuesWithoutDefaultWithWh;

	private static Object[] validStartTx;

	@BeforeClass
	public static void init() throws IOException {
		ObjectMapper mapper = new ObjectMapper();
		invalidMsgIncorrectSize = mapper.readValue("[]", Object[].class);

		validMeterValuesWithoutWh = mapper.readValue("[2,\"1\",\"MeterValues\",{\"connectorId\":1,\"meterValue\":[{\"timestamp\":\"2019-10-01T10:12:13.0477583Z\",\"sampledValue\":[{\"value\":\"10\",\"measurand\":\"Current.Import\",\"unit\":\"A\"}]}]}, \"chargerid\", \"vicinityoid\", \"outeridTag\"]", Object[].class);
		validMeterValuesWithDefault = mapper.readValue("[2,\"1\",\"MeterValues\",{\"connectorId\":1,\"meterValue\":[{\"timestamp\":\"2019-10-01T10:12:13.0477583Z\",\"sampledValue\":[{\"value\":\"10\"}]}]}, \"chargerid\", \"vicinityoid\", \"outeridTag\"]", Object[].class);
		validMeterValuesWithoutDefaultWithWh = mapper.readValue("[2,\"1\",\"MeterValues\",{\"connectorId\":1,\"meterValue\":[{\"timestamp\":\"2019-10-01T10:12:13.0477583Z\",\"sampledValue\":[{\"value\":\"42\",\"measurand\":\"Energy.Active.Import.Register\"}]}]}, \"chargerid\", \"vicinityoid\", \"outeridTag\"]", Object[].class);

		validStartTx = mapper.readValue("[2,\"3\",\"StartTransaction\",{\"connectorId\":1,\"idTag\":\"04EC2CC2552280\",\"timestamp\":\"2019-10-01T10:12:14.3072324Z\",\"meterStart\":300}, \"chargerid\", \"vicinityoid\", \"outeridTag\"]", Object[].class);
	}

	@Test
	public void invalidMsgIncorrectSize() {
		assertFalse(OCPPRequest.validOCCPRequest(invalidMsgIncorrectSize));
	}

	@Test
	public void validMeterValuesWithoutWh() {
		assertTrue(OCPPRequest.validOCCPRequest(validMeterValuesWithoutWh));
		OCPPRequest or = new OCPPRequest(validMeterValuesWithoutWh);
		String energy = or.getMeterValue("Energy.Active.Import.Register");
		assertNull(energy);
	}

	@Test
	public void validMeterValuesWithDefault() {
		assertTrue(OCPPRequest.validOCCPRequest(validMeterValuesWithDefault));
		OCPPRequest or = new OCPPRequest(validMeterValuesWithDefault);
		String energy = or.getMeterValue("Energy.Active.Import.Register");
		assertTrue(energy.equals("10"));
	}

	@Test
	public void validMeterValuesWithoutDefaultWithWh() {
		assertTrue(OCPPRequest.validOCCPRequest(validMeterValuesWithoutDefaultWithWh));
		OCPPRequest or = new OCPPRequest(validMeterValuesWithoutDefaultWithWh);
		String energy = or.getMeterValue("Energy.Active.Import.Register");
		assertTrue(energy.equals("42"));
	}

	@Test
	public void validStartTx() {
		assertTrue(OCPPRequest.validOCCPRequest(validStartTx));
		OCPPRequest or = new OCPPRequest(validStartTx);
		long ts = or.getTimestamp();
		assertTrue(""+ts,ts == 1569924734307L);
		long meterStart = or.getMeterStart();
		assertTrue(meterStart == 300);
		assertTrue(or.getIdTag().equals("04EC2CC2552280"));
	}

}
