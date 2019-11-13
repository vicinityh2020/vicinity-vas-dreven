package com.ubiwhere.drevenmobileapi.repository;

import com.ubiwhere.drevenmobileapi.entity.Wallet;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface WalletRepository extends JpaRepository<Wallet, Integer> {
}
