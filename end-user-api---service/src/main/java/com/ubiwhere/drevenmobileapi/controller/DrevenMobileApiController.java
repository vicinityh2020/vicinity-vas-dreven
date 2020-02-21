package com.ubiwhere.drevenmobileapi.controller;

import com.ubiwhere.drevenmobileapi.client.OcppClient;
import com.ubiwhere.drevenmobileapi.config.JwtRequest;
import com.ubiwhere.drevenmobileapi.config.JwtResponse;
import com.ubiwhere.drevenmobileapi.config.JwtTokenUtil;
import com.ubiwhere.drevenmobileapi.dto.*;
import com.ubiwhere.drevenmobileapi.service.DrevenMobileApiService;
import io.swagger.annotations.Api;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;


import javax.validation.Valid;
import java.util.List;

@Slf4j
@RestController
@Api(value = "Dreven mobile API")
public class DrevenMobileApiController {
    @Autowired
    DrevenMobileApiService drevenMobileApiService;

    @Autowired
    AuthenticationManager authenticationManager;

    @Autowired
    OcppClient ocppClient;

    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    @PostMapping(value = "/authenticate", consumes = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public ResponseEntity<?> createAuthenticationToken(@RequestBody JwtRequest authenticationRequest) throws Exception {
        log.info("Authenticating {}", authenticationRequest.getUsername());
        authenticate(authenticationRequest.getUsername(), authenticationRequest.getPassword());
        String token = jwtTokenUtil.generateToken(authenticationRequest.getUsername());
        return ResponseEntity.ok(new JwtResponse(token));
    }

    private void authenticate(String username, String password) throws Exception {
        try {
            authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(username, password));
        } catch (DisabledException e) {
            throw new Exception("USER_DISABLED", e);
        } catch (BadCredentialsException e) {
            throw new Exception("INVALID_CREDENTIALS", e);
        }
    }

    @PostMapping(path = "/account", consumes = MediaType.APPLICATION_JSON_UTF8_VALUE, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public AccountDto createAccount(@Valid @RequestBody CreateAccountDto createAccountDto) {
        log.info("Creating account {}", createAccountDto.toString());
        AccountDto accountDto = drevenMobileApiService.createAccount(createAccountDto);
        ocppClient.createIdtTag(accountDto.getIdTag());
        return accountDto;
    }

    @GetMapping(path = "/account", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public AccountDto getAccount() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	log.info("Get account info {}", (String) auth.getPrincipal());
        return drevenMobileApiService.getAccount((String) auth.getPrincipal());
    }

    @GetMapping(path = "/charger", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public List<ChargerDto> getChargers(@RequestParam Double latitude, @RequestParam Double longitude, @RequestParam Double distance) {
        log.info("Get chargers lat:{} lon:{} dist:{}", latitude, longitude, distance);
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return drevenMobileApiService.getChargers((String) auth.getPrincipal(), latitude, longitude, distance);
    }

    @GetMapping(path = "/provider", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public List<ProviderDto> getProviders() {
	log.info("Get providers");
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return drevenMobileApiService.getProviders((String) auth.getPrincipal());
    }

    @PostMapping(path = "/contract", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public ContractDto createContract(@Valid @RequestBody CreateContractDto createContractDto) {
	log.info("Create contract {}", createContractDto.toString());
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return drevenMobileApiService.createContract((String) auth.getPrincipal(), createContractDto);
    }

    @GetMapping(path = "/abi/pricing", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public String getABIPricing() {
        return drevenMobileApiService.getABIPricing();
    }

    @GetMapping(path = "/abi/multisig", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public String getABIMulti() {
        return drevenMobileApiService.getABIMulti();
    }

    @GetMapping(path = "/abi/factory", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public String getABIFactory() {
        return drevenMobileApiService.getABIFactory();
    }

    @GetMapping(path = "/address/factory", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public String getAddressFactory() {
        return drevenMobileApiService.getAddressFactory();
    }
}
