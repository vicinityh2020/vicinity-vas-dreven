package com.ubiwhere.drevenmobileapi.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class ChargerDto {
    Integer id;
    String name;
    String address;
    Double latitude;
    Double longitude;
    Integer providerId;
    String providerName;
    String pricingAddress;
    String contractAddress;
}
