package com.ubiwhere.drevenmobileapi.repository;

import com.ubiwhere.drevenmobileapi.dto.ChargerDto;
import com.ubiwhere.drevenmobileapi.entity.Charger;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import javax.persistence.Tuple;
import java.util.List;

@Repository
public interface ChargerRepository extends JpaRepository<Charger, Integer> {
    @Query(value = "select infrastructures.id, infrastructures.\"name\", infrastructures.address,\n" +
            "infrastructures.latitude, infrastructures.longitude, providers.id as providerId,\n" +
            "providers.\"name\" as providerName, \"pricingContracts\".address as pricingAddress,\n" +
            "T.address as contractAddress\n" +
            "from infrastructures \n" +
            "left join providers on infrastructures.provider_id = providers.id\n" +
            "left join \"pricingContracts\" on providers.id = \"pricingContracts\".provider_id\n" +
            "left join  (select provider_id, address from \"multisigContracts\" where enduser_id = (select id from endusers where email = :email)) as T\n" +
            "on T.provider_id = \"pricingContracts\".provider_id", nativeQuery = true)
    public List<Tuple> findAllChargers(@Param("email")String email);
}
