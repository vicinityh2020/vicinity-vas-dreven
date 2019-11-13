package com.ubiwhere.drevenmobileapi.entity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Generated;
import org.hibernate.annotations.GenerationTime;

import javax.persistence.*;
import java.time.Instant;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Date;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name="`infrastructures`")
public class Charger {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(columnDefinition = "serial")
    Integer id;

    String name;

    String vicinity_oid;

    @ManyToOne
    Provider provider;

    @Column(name = "`lastStartTransaction`")
    Long lastStartTransaction;

    @Column(name = "`lastStopTransaction`")
    Long lastStopTransaction;

    @Column(name = "`meterValue`")
    Integer meterValue;

    @Column(name = "`lastStartMeterValue`")
    Integer lastStartMeterValue;

    String status;

    String address;

    Double latitude;

    Double longitude;

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
