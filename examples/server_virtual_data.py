#!/usr/bin/env python3

# An example of Modbus/TCP server with virtual data
#
# Map the system date and time to @ 0 to 5 on the "holding registers" space. Only the reading
# of these registers in this address space is authorized. All other requests return an illegal
# data address except.

import argparse
from pyModbusTCP.server import ModbusServer, DefaultDataBank
from datetime import datetime


class MyDataBank(DefaultDataBank):
    def __init__(self):
        super().__init__(coils=False, d_inputs=False, h_regs=False, i_regs=False)

    def get_holding_registers(self, address, number=1):
        now = datetime.now()
        virtual_d = {0: now.day, 1: now.month, 2: now.year,
                     3: now.hour, 4: now.minute, 5: now.second}
        try:
            return [virtual_d[a] for a in range(address, address+number)]
        except KeyError:
            return None


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='localhost', help='Host')
    parser.add_argument('-p', '--port', type=int, default=502, help='TCP port')
    args = parser.parse_args()
    # init modbus server and start it
    server = ModbusServer(host=args.host, port=args.port, data_bank=MyDataBank())
    server.start()

