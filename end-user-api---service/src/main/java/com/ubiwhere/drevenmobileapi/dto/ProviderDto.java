package com.ubiwhere.drevenmobileapi.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class ProviderDto {
    Integer id;
    String name;
    String pricingAddress;
    String contractAddress;
}
