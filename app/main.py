from pyLoraRFM9x import LoRa  # type: ignore // gabisa di install di win64
from typing import Any
from time import sleep
import schedule
from prisma import Prisma
from prisma.models import SensorReading
from struct_helper import read_struct
from config import (
    RFM95_PORT,
    RFM95_CS,
    RFM95_INT,
    RFM95_RST,
    RF95_FREQ,
    RF95_POW,
    CLIENT_ADDRESS,
    NODE_ADDRESSES,
    ModemConfig,
)


# global objects
lora = LoRa(
    RFM95_PORT,
    RFM95_CS,
    RFM95_INT,
    CLIENT_ADDRESS,
    reset_pin=RFM95_RST,
    freq=RF95_FREQ,
    tx_power=RF95_POW,
    modem_config=ModemConfig.Bw125Cr45Sf2048,
    acks=True,
    receive_all=False,
)

db = Prisma()
current_index = 0


def on_recv(payload: Any) -> None:
    """Callback function when data received from the LoRa module"""
    global current_index

    try:
        payload_struct = payload.message
        device_id, temp, hum, light, tip = read_struct(payload_struct)

        print("From:", device_id)
        print("Received:", f"{temp=}, {hum=}, {light=}, {tip=}")
        print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

        # insert data to database
        entry = db.sensorreading.update(
            where={"id": current_index},
            data={
                "nodeId": device_id,
                "temperature": temp,
                "humidity": hum,
                "lux": light,
                "tips": tip,
            },
        )

        if entry is None:
            print("[Error]: Cannot find db entry.")

    except:
        print("[Error]: Ignoring data since it's unreadable.")


# job buat schedule send data
def job() -> None:
    """Job function to send data to all nodes."""

    global current_index

    print("[Schedule]: Begin to request data from all nodes.")

    entry: SensorReading = db.sensorreading.create()
    # set current index
    current_index = entry.id

    # gtau bisa send ini apa nggak

    # 0x69 packet untuk request data
    lora.send(0x69, 255)  # broadcast message to all nodes


def setup() -> None:
    """Setup function only called once per lifetime"""

    global lora, db

    db.connect()

    lora.set_mode_rx()
    lora.on_recv = on_recv

    # assign job ke scheduler
    schedule.every(30).minutes.do(job)


def main() -> None:
    """Main Program Loop"""

    try:
        while True:
            schedule.run_pending()
            sleep(2)

    except KeyboardInterrupt:
        db.disconnect()
        pass


setup()
main()
