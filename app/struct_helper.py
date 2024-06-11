import struct
from typing import Any, Tuple

# todo: masih ngasal ini
# 'B' for uint8_t, 'f' for float, 'i' for int, 'H' for uint16_t
STRUCT_FORMAT = "BfffH"


def read_struct(payload: bytes) -> Tuple[int, float, float, float, int]:
    """Read struct from bytes"""
    data = struct.unpack(STRUCT_FORMAT, payload)

    # id, temp, hum, light, tip
    return data[0], data[1], data[2], data[3], data[4]
