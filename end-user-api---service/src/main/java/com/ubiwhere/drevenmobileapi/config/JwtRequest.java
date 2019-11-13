package com.ubiwhere.drevenmobileapi.config;

import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.io.Serializable;

@NoArgsConstructor
@Getter
@Setter
public class JwtRequest implements Serializable {

    private static final long serialVersionUID = 5926468583005150707L;
    private String username;
    private String password;
}