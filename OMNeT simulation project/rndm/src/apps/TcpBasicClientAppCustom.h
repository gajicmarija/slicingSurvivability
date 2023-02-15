//
// Copyright (C) 2004 OpenSim Ltd.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

#ifndef __INET_TcpBasicClientAppCustom_H
#define __INET_TcpBasicClientAppCustom_H

#include "inet/applications/tcpapp/TcpAppBase.h"
#include "inet/common/lifecycle/ILifecycle.h"
#include "inet/common/lifecycle/NodeStatus.h"

namespace inet {

/**
 * An example request-reply based client application.
 */
class INET_API TcpBasicClientAppCustom : public TcpAppBase
{
  protected:
    cMessage *timeoutMsg = nullptr;
    bool earlySend = false; // if true, don't wait with sendRequest() until established()
    int numRequestsToSend = 0; // requests to send in this session
    simtime_t startTime;
    simtime_t stopTime;

    std::string fileName;

    simtime_t lastCheckTime;
    int64_t lastCheckBits;

    long replyLength;
    int64_t bitsReceived;
    simtime_t downloadBegin;
    double lastMos;

    int flag = 1; //On by default

    virtual void sendRequest();
    virtual void rescheduleAfterOrDeleteTimer(simtime_t d, short int msgKind);

    virtual int numInitStages() const override { return NUM_INIT_STAGES; }
    virtual void initialize(int stage) override;
    virtual void handleTimer(cMessage *msg) override;

    virtual void socketEstablished(TcpSocket *socket) override;
    virtual void socketDataArrived(TcpSocket *socket, Packet *msg, bool urgent) override;
    virtual void socketClosed(TcpSocket *socket) override;
    virtual void socketFailure(TcpSocket *socket, int code) override;

    virtual void handleStartOperation(LifecycleOperation *operation) override;
    virtual void handleStopOperation(LifecycleOperation *operation) override;
    virtual void handleCrashOperation(LifecycleOperation *operation) override;

    virtual void close() override;

  public:
    TcpBasicClientAppCustom() {}
    virtual ~TcpBasicClientAppCustom();
};

} // namespace inet

#endif

