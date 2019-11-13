package com.ubiwhere.drevenmobileapi.entity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Generated;
import org.hibernate.annotations.GenerationTime;

import javax.persistence.*;
import java.time.Instant;
import java.util.Date;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name="`multisigContracts`")
public class Contract {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(columnDefinition = "serial")
    Integer id;

    @ManyToOne
    @JoinColumn(name = "contract_structure_id")
    ContractDetails contractDetails;

    @ManyToOne
    Provider provider;

    @ManyToOne
    @JoinColumn(name = "enduser_id")
    User user;

    String address;

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
