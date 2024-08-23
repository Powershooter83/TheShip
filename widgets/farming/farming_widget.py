from functools import partial
from typing import Dict, Callable

from models.Station import Station

AMOUNT = 12
STATION_START = Station.CORE
STATION_END = Station.VESTA

def set_amount(new_amount: int):
    global AMOUNT
    AMOUNT = new_amount

def set_station_start(new_start_station: Station):
    global STATION_START
    STATION_START = new_start_station

def set_station_end(new_end_station: Station):
    global STATION_END
    STATION_END = new_end_station


methods_dict: Dict[str, Callable[[], str]] = {
    'setStartStationBtn_VESTA': partial(set_station_start, new_start_station=Station.VESTA),
    'setStartStationBtn_CORE': partial(set_station_start, new_start_station=Station.CORE),
    'setEndStationBtn_VESTA': partial(set_station_end, new_end_station=Station.VESTA),
    'setEndStationBtn_CORE': partial(set_station_end, new_end_station=Station.CORE),
    'increaseAmountBtn': partial(set_amount, new_amount=(AMOUNT + 1)),
    'decreaseAmountBtn': partial(set_amount, new_amount=(AMOUNT - 1)),
}

#!/usr/bin/python3
import socket
import json

with open(__file__, 'r') as f:
    this_file = f.read()
doc = '```python\n' + this_file + '\n```'

with open('widget.json', 'r') as file:
    widget_data = json.load(file)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("192.168.100.21", 2002))
    s.sendall(json.dumps(widget_data).encode('utf-8'))
    s.sendall(b'\0')  # null-byte -> end of message
    s.sendall(json.dumps({
        'kind': 'update_doc',        'doc': doc,
    }).encode('utf-8'))
    s.sendall(b'\0')  # null-byte -> end of message
    buffer = bytes()
    while True:
        received = s.recv(1)
        if len(received) == 0:
            print('disconnected')
            break
        if received == b'\0':
            print(buffer)
            s.sendall(json.dumps({'kind': 'keepalive'}).encode('utf-8'))
            s.sendall(b'\0')
            buffer = bytes()
        else:
            buffer += received

