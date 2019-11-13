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
package de.rwth.idsg.steve.ocpp.ws;

import de.rwth.idsg.steve.service.ChargePointHelperService;
import de.rwth.idsg.steve.service.NotificationService;
import org.eclipse.jetty.websocket.api.WebSocketPolicy;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.web.socket.WebSocketExtension;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.HandshakeFailureException;
import org.springframework.web.socket.server.jetty.JettyRequestUpgradeStrategy;

import org.jetbrains.annotations.Nullable;
import java.security.Principal;
import java.util.List;
import java.util.Map;

/**
 * @author Sevket Goekay <goekay@dbis.rwth-aachen.de>
 * @since 13.03.2015
 */
public class OcppWebSocketUpgrader extends JettyRequestUpgradeStrategy {

    private final List<AbstractWebSocketEndpoint> endpoints;
    private final NotificationService notificationService;
    private final ChargePointHelperService chargePointHelperService;

    public OcppWebSocketUpgrader(WebSocketPolicy policy, List<AbstractWebSocketEndpoint> endpoints,
                                 NotificationService notificationService,
                                 ChargePointHelperService chargePointHelperService) {
        super(policy);
        this.endpoints = endpoints;
        this.notificationService = notificationService;
        this.chargePointHelperService = chargePointHelperService;
    }

    @Override
    public void upgrade(ServerHttpRequest request, ServerHttpResponse response,
                        String selectedProtocol, List<WebSocketExtension> selectedExtensions, Principal user,
                        WebSocketHandler wsHandler, Map<String, Object> attributes) throws HandshakeFailureException {

        // -------------------------------------------------------------------------
        // 1. Check the chargeBoxId
        // -------------------------------------------------------------------------

        String chargeBoxId = getLastBitFromUrl(request.getURI().getPath());
        if (chargePointHelperService.isRegistered(chargeBoxId)) {
            attributes.put(AbstractWebSocketEndpoint.CHARGEBOX_ID_KEY, chargeBoxId);
        } else {
            // send only if the station is not registered, because otherwise, after the connection it will send a boot
            // notification message and we handle the notifications for these normal cases in service classes already.
            notificationService.ocppStationBooted(chargeBoxId, false);

            throw new HandshakeFailureException("ChargeBoxId '" + chargeBoxId + "' is not registered");
        }

        // -------------------------------------------------------------------------
        // 2. Route according to the selected protocol
        // -------------------------------------------------------------------------

        if (selectedProtocol == null) {
            throw new HandshakeFailureException("No protocol (OCPP version) is specified.");
        }

        AbstractWebSocketEndpoint endpoint = findEndpoint(selectedProtocol);

        if (endpoint == null) {
            throw new HandshakeFailureException("Requested protocol '" + selectedProtocol + "' is not supported");
        }

        super.upgrade(request, response, selectedProtocol, selectedExtensions, user, endpoint, attributes);
    }

    @Nullable
    private AbstractWebSocketEndpoint findEndpoint(String selectedProtocol) {
        for (AbstractWebSocketEndpoint endpoint : endpoints) {
            if (endpoint.getVersion().getValue().equals(selectedProtocol)) {
                return endpoint;
            }
        }
        return null;
    }

    /**
     * Taken from: http://stackoverflow.com/a/4050276
     */
    private static String getLastBitFromUrl(final String url) {
        return url.replaceFirst(".*/([^/?]+).*", "$1");
    }
}
