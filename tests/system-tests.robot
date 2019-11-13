*** Settings ***
Library          test_lib.py
Library          OperatingSystem

*** Variables ***
${PRIVKEYFUNDS}     0xA627B30DDD00137ADFA9B74D14213BB77F7352B5E863F9C407BBD58FCCD86C4A
${PRIVKEYCLIENT}    0xA627B30DDD00137ADFA9B74D14213BB77F7352B5E863F9C407BBD58FCCD86C4A
${PRIVKEYPROV}      0x81987B7C6E80160EEB1DEC5D5FACF91F0D314160E702932F1687352AB0A8E787
${MULTISIGADDRESS}  0xacA22D92063494216f526Be56cf403016093B537
${PRICINGADDRESS}   0x3d859547ef7e007BE7cE4c51123ba222F4B2Fab2

*** Test Cases ***
Charge with balance
    ${initial_balance}=  Set Balance  ${PRIVKEYFUNDS}  ${PRIVKEYPROV}  ${PRIVKEYCLIENT}  ${MULTISIGADDRESS}  ${PRICINGADDRESS}  ${2}

    Run  cd docile-charge-point && sbt 'run -c "ddd12da2-8e73-43dd-b8f0-cc8730580882" -v 1.6 ws://localhost:8182/steve/websocket/CentralSystemService/ examples/ocpp1x/do-a-transaction.scala'

    
    Wait Until Keyword Succeeds  30s  1s
    ...   Check Final Balance  ${initial_balance-1}

Charge with balance, stop remote
    ${initial_balance}=  Set Balance  ${PRIVKEYFUNDS}  ${PRIVKEYPROV}  ${PRIVKEYCLIENT}  ${MULTISIGADDRESS}  ${PRICINGADDRESS}  ${2}

    Run  cd docile-charge-point && sbt 'run -c "ddd12da2-8e73-43dd-b8f0-cc8730580882" -v 1.6 ws://localhost:8182/steve/websocket/CentralSystemService/ examples/ocpp1x/do-a-transaction-metervalues.scala'


    Wait Until Keyword Succeeds  30s  1s
    ...   Check Final Balance  ${0}


*** Keywords ***
Check Final Balance
    [Arguments]   ${target_balance}

    ${final_balance}=  Get Balance  ${MULTISIGADDRESS}

    Should Be Equal As Numbers  ${target_balance}  ${final_balance}
