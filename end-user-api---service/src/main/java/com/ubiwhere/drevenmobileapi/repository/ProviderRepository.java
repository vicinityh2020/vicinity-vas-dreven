package com.ubiwhere.drevenmobileapi.repository;

import com.ubiwhere.drevenmobileapi.dto.ProviderDto;
import com.ubiwhere.drevenmobileapi.entity.Provider;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import javax.persistence.Tuple;
import java.util.List;

@Repository
public interface ProviderRepository extends JpaRepository<Provider, Integer> {
    @Query(value = "select providers.id as id, providers.\"name\" as name, \"pricingContracts\".address as pricingAddress, T.address as contractAddress\n" +
            "from providers \n" +
            "left join \"pricingContracts\" on providers.id = \"pricingContracts\".provider_id\n" +
            "left join  (select provider_id, address from \"multisigContracts\" where enduser_id = (select id from endusers where email = :email)) as T\n" +
            "on T.provider_id = \"pricingContracts\".provider_id", nativeQuery = true)
    public List<Tuple> findAllProviders(@Param("email") String email);
}
