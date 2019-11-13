package com.ubiwhere.drevenmiddleware.controller;

import com.ubiwhere.drevenmiddleware.service.MiddlewareService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;

@Slf4j
@RestController
@RequestMapping("/api/v1")
public class MiddlewareController {
    @Autowired
    MiddlewareService middlewareService;

    @PostMapping(path = "/ocppreqs/", consumes = MediaType.APPLICATION_JSON_UTF8_VALUE)
    @ResponseStatus(HttpStatus.OK)
    public void createOCPPReq(@RequestBody final Object[] OCPPReq) {
        log.debug("Request received {}",  Arrays.toString(OCPPReq));
        middlewareService.createOCPPReq(OCPPReq);
    }

}
