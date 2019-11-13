/*
 * SteVe - SteckdosenVerwaltung - https://github.com/RWTH-i5-IDSG/steve
 * Copyright (C) 2013-2019 RWTH Aachen University - Information Systems - Intelligent Distributed Systems Group (IDSG).
 * All Rights Reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
package de.rwth.idsg.steve.service;

/**
 * @author Sevket Goekay <goekay@dbis.rwth-aachen.de>
 * @since 22.01.2016
 */
public interface NotificationService {
    void ocppStationBooted(String chargeBoxId, boolean isRegistered);
    void ocppStationWebSocketConnected(String chargeBoxId);
    void ocppStationWebSocketDisconnected(String chargeBoxId);
    void ocppStationStatusFailure(String chargeBoxId, int connectorId, String errorCode);
    void ocppTransactionStarted(String chargeBoxId, int transactionId, int connectorId);
    void ocppTransactionEnded(String chargeBoxId, int transactionId);

}
