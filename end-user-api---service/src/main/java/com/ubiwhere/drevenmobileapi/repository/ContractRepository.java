package com.ubiwhere.drevenmobileapi.repository;

import com.ubiwhere.drevenmobileapi.entity.Contract;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ContractRepository extends JpaRepository<Contract, Integer> {
}
