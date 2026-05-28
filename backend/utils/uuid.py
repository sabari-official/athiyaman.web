import time
import os
import uuid

def uuidv7() -> uuid.UUID:
    """
    Generates a standard-compliant UUIDv7 (timestamp-ordered UUID).
    Uses a 48-bit timestamp in milliseconds and 74 bits of secure randomness.
    """
    # 48-bit timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    
    # 12-bit random value (rand_a)
    rand_a = int.from_bytes(os.urandom(2), byteorder="big") & 0x0FFF
    
    # 62-bit random value (rand_b)
    rand_b = int.from_bytes(os.urandom(8), byteorder="big") & 0x3FFFFFFFFFFFFFFF
    
    # Construct 128-bit integer
    # high: timestamp (48 bits) | version 7 (4 bits) | rand_a (12 bits) = 64 bits
    high = (timestamp << 16) | (7 << 12) | rand_a
    # low: variant 2 (2 bits) | rand_b (62 bits) = 64 bits
    low = (2 << 62) | rand_b
    
    return uuid.UUID(int=(high << 64) | low)
