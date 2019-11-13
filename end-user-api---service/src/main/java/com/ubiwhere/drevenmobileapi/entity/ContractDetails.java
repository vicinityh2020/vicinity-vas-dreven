package com.ubiwhere.drevenmobileapi.entity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Generated;
import org.hibernate.annotations.GenerationTime;

import javax.persistence.*;
import java.time.Instant;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name="`contractStructures`")
public class ContractDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(columnDefinition = "serial")
    Integer id;

    String abi;

    String bytecode;

    @Column(name = "`contract_type`")
    String type;

    @Column(name = "`created_on`")
    Long createdDate;

    @Column(name = "`updated_on`")
    Long updatedDate;

    @PrePersist
    void createdAt() {
        final Instant instant = Instant.now();
        this.createdDate = this.updatedDate = instant.toEpochMilli();
    }

    @PreUpdate
    void updatedAt() {
        final Instant instant = Instant.now();
        this.updatedDate = instant.toEpochMilli();
    }
}
