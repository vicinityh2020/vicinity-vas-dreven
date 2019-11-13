package com.ubiwhere.drevenmobileapi.service;

import com.ubiwhere.drevenmobileapi.dto.*;
import com.ubiwhere.drevenmobileapi.entity.*;
import com.ubiwhere.drevenmobileapi.repository.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.Tuple;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Slf4j
public class DrevenMobileApiService {

    @Autowired
    UserRepository userRepository;

    @Autowired
    WalletRepository walletRepository;

    @Autowired
    ChargerRepository chargerRepository;

    @Autowired
    ProviderRepository providerRepository;

    @Autowired
    ContractRepository contractRepository;

    @Autowired
    ContractDetailsRepository contractDetailsRepository;

    @Autowired
    PasswordEncoder bCryptPasswordEncoder;

    @Value("${abi.id.pricing}")
    private Integer abiIdPricing;

    @Value("${abi.id.multisig}")
    private Integer abiIdMulti;

    @Value("${abi.id.factory}")
    private Integer abiIdFactory;


    @Transactional
    public AccountDto createAccount(CreateAccountDto createAccountDto) {
        Wallet wallet = new Wallet();
        wallet.setAddress(createAccountDto.getWalletAddress());

        User user = new User();
        user.setEmail(createAccountDto.getEmail());
        user.setName(createAccountDto.getName());
        user.setWallet(wallet);
        user.setIdTag(createAccountDto.getIdTag());
        user.setPassword(bCryptPasswordEncoder.encode(createAccountDto.getPassword()));

        walletRepository.save(wallet);
        userRepository.save(user);

        AccountDto accountDto = new AccountDto();
        accountDto.setName(user.getName());
        accountDto.setIdTag(user.getIdTag());
        accountDto.setEmail(user.getEmail());
        accountDto.setWalletAddress(user.getWallet().getAddress());
        return accountDto;
    }

    public AccountDto getAccount(String email) {
        User user = userRepository.findByEmail(email);
        AccountDto accountDto = new AccountDto();
        accountDto.setName(user.getName());
        accountDto.setIdTag(user.getIdTag());
        accountDto.setEmail(user.getEmail());
        accountDto.setWalletAddress(user.getWallet().getAddress());
        return accountDto;
    }

    /**
     *
     * @param latitude
     * @param longitude
     * @param distance - in Kilometers
     * @return
     */
    public List<ChargerDto> getChargers(String email, Double latitude, Double longitude, Double distance) {
        List<ChargerDto> chargerDtos = new ArrayList<>();
        for(Tuple t :chargerRepository.findAllChargers(email)) {
            if(distance(latitude, longitude, (Double)t.get("latitude"), (Double)t.get("longitude")) <= (distance*1000)) {
                chargerDtos.add(new ChargerDto(
                        (Integer)t.get(0),
                        (String)t.get(1),
                        (String)t.get(2),
                        (Double)t.get(3),
                        (Double)t.get(4),
                        (Integer)t.get(5),
                        (String)t.get(6),
                        (String)t.get(7),
                        (String)t.get(8)));
            }
        }
        return chargerDtos;
    }

    private double distance(Double lat1, Double lon1, Double lat2, Double lon2) {
        double R = 6371e3; // metres
        double φ1 = Math.toRadians(lat1);
        double φ2 = Math.toRadians(lat2);
        double Δφ = Math.toRadians(lat2-lat1);
        double Δλ = Math.toRadians(lon2-lon1);

        double a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
                   Math.cos(φ1) * Math.cos(φ2) *
                   Math.sin(Δλ/2) * Math.sin(Δλ/2);

        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

        double d = R * c;
        return d;
    }

    public List<ProviderDto> getProviders(String email) {
        List<ProviderDto> providerDtos = new ArrayList<>();
        for(Tuple t : providerRepository.findAllProviders(email)) {
            providerDtos.add(new ProviderDto((Integer)t.get(0), (String)t.get(1), (String)t.get(2), (String)t.get(3)));
        }
        return providerDtos;
    }

    public ContractDto createContract(String email, CreateContractDto createContractDto) {
        User user = userRepository.findByEmail(email);
        Provider provider = providerRepository.getOne(createContractDto.getProviderId());
        Contract contract = new Contract();
        contract.setAddress(createContractDto.getContractAddress());
        contract.setUser(user);
        contract.setProvider(provider);
        contract = contractRepository.save(contract);

        return new ContractDto(contract.getId());
     }

    public String getABI(Integer id) {
        Optional<ContractDetails> opt = contractDetailsRepository.findById(id);
        if(opt.isPresent()) {
            return opt.get().getAbi();
        } else {
            return "";
        }
    }

    public String getABIPricing() {
        return getABI(abiIdPricing);
    }

    public String getABIMulti() {
        return getABI(abiIdMulti);
    }

    public String getABIFactory() {
        return getABI(abiIdFactory);
    }

    public String getAddressFactory() {
        Optional<ContractDetails> opt = contractDetailsRepository.findById(abiIdFactory);
        if(opt.isPresent()) {
            return opt.get().getType();
        } else {
            return "";
        }
    }
}
