val chargeTokenId = "04EC2CC2552280"
val auth = authorize(chargeTokenId).idTag

if (auth.status == AuthorizationStatus.Accepted) {
  statusNotification(status = ChargePointStatus.Occupied(Some(OccupancyKind.Preparing)))
  val transId = startTransaction(meterStart = 123, idTag = chargeTokenId).transactionId
  statusNotification(status = ChargePointStatus.Occupied(Some(OccupancyKind.Charging)))

  //prompt("Press ENTER to send meter value")
  meterValues()
  //prompt("Press ENTER to stop charging")

  statusNotification(status = ChargePointStatus.Occupied(Some(OccupancyKind.Finishing)))
  stopTransaction(meterStop = 543, transactionId = transId, idTag = Some(chargeTokenId))
  statusNotification(status = ChargePointStatus.Available())

} else {
  fail("Not authorized")
}

// vim: set ts=4 sw=4 et:
