*** Settings ***
Library          test_lib.py
Library          OperatingSystem

*** Variables ***
${PRIVKEYFUNDS}     0xA627B30DDD00137ADFA9B74D14213BB77F7352B5E863F9C407BBD58FCCD86C4A
${PRIVKEYCLIENT}    0x9b35940ce8506c5cb9092812fb848ab5646c055fa3800217a7a6094723994572
${PRIVKEYPROV}      0x754da43cb3f6e32fff7a01f446cc206063e90c1142d69fc9942550df132f8ada
${MULTISIGADDRESS}  0xDebb7f0fd233b9240D7a7C51833cBB690153aD0E
${PRICINGADDRESS}   0x59064e55b1c9d070B38cE3Dd61ED368Fe64AB905


*** Test Cases ***
Charge with balance
    ${initial_balance}=  Set Balance  ${PRIVKEYFUNDS}  ${PRIVKEYPROV}  ${PRIVKEYCLIENT}  ${MULTISIGADDRESS}  ${PRICINGADDRESS}  ${2}

    Run  cd docile-charge-point && sbt 'run -c "5f016720-d0e0-40c5-b803-929759a366ff" -v 1.6 ws://localhost:8180/steve/websocket/CentralSystemService/ examples/ocpp1x/do-a-transaction.scala'

    
    Wait Until Keyword Succeeds  30s  1s
    ...   Check Final Balance  ${initial_balance-1}

Charge with balance, stop remote
    ${initial_balance}=  Set Balance  ${PRIVKEYFUNDS}  ${PRIVKEYPROV}  ${PRIVKEYCLIENT}  ${MULTISIGADDRESS}  ${PRICINGADDRESS}  ${2}

    Run  cd docile-charge-point && sbt 'run -c "5f016720-d0e0-40c5-b803-929759a366ff" -v 1.6 ws://localhost:8180/steve/websocket/CentralSystemService/ examples/ocpp1x/do-a-transaction-metervalues.scala'


    Wait Until Keyword Succeeds  30s  1s
    ...   Check Final Balance  ${0}


*** Keywords ***
Check Final Balance
    [Arguments]   ${target_balance}

    ${final_balance}=  Get Balance  ${MULTISIGADDRESS}

    Should Be Equal As Numbers  ${target_balance}  ${final_balance}
