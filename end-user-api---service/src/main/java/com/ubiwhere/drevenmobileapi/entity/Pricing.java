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
@Table(name="`pricingContracts`")
public class Pricing {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(columnDefinition = "serial")
    Integer id;

    @OneToOne
    Provider provider;

    @ManyToOne
    @JoinColumn(name = "contract_structure_id")
    ContractDetails contractDetails;

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
