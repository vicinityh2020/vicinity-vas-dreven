package com.ubiwhere.drevenmobileapi.dto;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.validation.annotation.Validated;

import javax.validation.constraints.NotNull;

@Getter
@Setter
@ToString
public class CreateAccountDto {
    @NotNull
    String idTag;

    @NotNull
    String name;

    @NotNull
    String email;

    @NotNull
    String password;

    @NotNull
    String walletAddress;
}
