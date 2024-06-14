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
    ModemConfig,
)


# global objects
lora = LoRa(
    spi_port=RFM95_PORT,
    spi_channel=RFM95_CS,
    interrupt_pin=RFM95_INT,
    my_address=CLIENT_ADDRESS,
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

        # # insert data to database
        # entry = db.sensorreading.update(
        #     where={"id": current_index},
        #     data={
        #         "nodeId": device_id,
        #         "temperature": temp,
        #         "humidity": hum,
        #         "lux": light,
        #         "tips": tip,
        #     },
        # )

        # if entry is None:
        #     print("[Error]: Cannot find db entry.")

        entry = db.sensorreading.create(
            data={
                "nodeId": device_id,
                "temperature": temp,
                "humidity": hum,
                "lux": light,
                "tips": tip,
            }
        )

        print("[Success]: Data inserted to database.")

    except:
        print("[Error]: Ignoring data since it's unreadable.")


# job buat schedule send data
def job() -> None:
    """Job function to send data to all nodes."""

    global current_index

    print("[Schedule]: Begin to request data from all nodes.")

    entry: SensorReading = db.sensorreading.create(
        data={
            "nodeId": None,
            "temperature": None,
            "humidity": None,
            "lux": None,
            "tips": None,
        }
    )
    # set current index
    current_index = entry.id

    # gtau bisa send ini apa nggak

    # 0x69 packet untuk request data
    lora.send(0x69, 255)  # broadcast message to all nodes


def setup() -> None:
    """Setup function only called once per lifetime"""

    global lora, db

    print("[setup]: connecting to sqlite database")
    db.connect()

    print("[setup]: setting up LoRa module")
    lora.set_mode_rx()
    lora.on_recv = on_recv

    # assign job ke scheduler
    print("[setup]: setting up scheduler")

    # scheduler will be unused since we use esp timer
    # schedule.every().hour.at(":00").do(job)

    print("[setup]: setup done...")


def main() -> None:
    """Main Program Loop"""

    print("[Main]: Running main program loop...")

    try:
        while True:
            schedule.run_pending()
            sleep(2)

    except KeyboardInterrupt:
        db.disconnect()
        pass


setup()
main()
