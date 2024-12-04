from time import localtime, strftime
import struct

class NTPPacket:

    def __init__(self) -> None:
        self.t1 = 0.0  # Originate Timestamp
        self.t2 = 0.0  # Receive Timestamp
        self.t3 = 0.0  # Transmit Timestamp
        self.t4 = 0.0  # Destination Timestamp

        self.leap_indicator = 0
        self.version = 4
        self.mode = 3  # Client mode
        self.stratum = 0
        self.poll = 0
        self.precision = -6
        self.root_delay = 0
        self.root_dispersion = 0
        self.reference_identifier = 0
    
    def calculate_offset(self):
        print(((self.t2 - self.t1) + (self.t3 - self.t4)) / 2)
        return ((self.t2 - self.t1) + (self.t3 - self.t4)) / 2
    
    def calculate_delay(self):
        return (self.t2 - self.t1) - (self.t3 - self.t4)
    
    def synchronize(self):
        return self.t4 + self.calculate_offset()

    def set_t1(self, t1: int) -> None:
        self.t1 = t1
    
    def set_t2(self, t2: int) -> None:
        self.t2 = t2

    def set_t3(self, t3: int) -> None:
        self.t3 = t3
    
    def set_t4(self, t4: int) -> None:
        self.t4 = t4

    def to_binary(self) -> bytes:
        """
        Convert the NTPPacket into a 48-byte binary representation.
        """
        # Combine leap, version, and mode into one byte
        li_vn_mode = (self.leap_indicator << 6) | (self.version << 3) | self.mode

        # Convert timestamps to seconds and fractions
        t1_sec, t1_frac = divmod(self.t1, 1)
        t2_sec, t2_frac = divmod(self.t2, 1)
        t3_sec, t3_frac = divmod(self.t3, 1)
        t4_sec, t4_frac = divmod(self.t4, 1)

        # Pack the binary structure
        packet = struct.pack(
            "!B B B b I I I I I I I I I I I",
            li_vn_mode,               # Leap Indicator, Version, Mode
            self.stratum,             # Stratum
            self.poll,                # Poll Interval
            self.precision,           # Precision
            int(self.root_delay),     # Root Delay
            int(self.root_dispersion),# Root Dispersion
            self.reference_identifier,  # Reference Identifier
            int(t1_sec), int(t1_frac * (2**32)),  # Originate Timestamp (seconds, fraction)
            int(t2_sec), int(t2_frac * (2**32)),  # Receive Timestamp (seconds, fraction)
            int(t3_sec), int(t3_frac * (2**32)),  # Transmit Timestamp (seconds, fraction)
            int(t4_sec), int(t4_frac * (2**32)),  # Receive Timestamp (seconds, fraction)
        )
        return packet



    @classmethod
    def from_binary(cls, data: bytes) -> "NTPPacket":
        """
        Parse a 48-byte binary packet into an NTPPacket object.
        """
        if len(data) != 48:
            raise ValueError("NTP packet must be exactly 48 bytes long")
        
        # Unpack the binary data
        unpacked = struct.unpack("!B B B b I I I I I I I I I I I", data)

        # Extract the first byte for LI, VN, and Mode
        li_vn_mode = unpacked[0]
        leap_indicator = (li_vn_mode >> 6) & 0b11
        version = (li_vn_mode >> 3) & 0b111
        mode = li_vn_mode & 0b111

        # Create a new NTPPacket instance and populate fields
        packet = cls()
        packet.leap_indicator = leap_indicator
        packet.version = version
        packet.mode = mode
        packet.stratum = unpacked[1]
        packet.poll = unpacked[2]
        packet.precision = unpacked[3]
        packet.root_delay = unpacked[4]
        packet.root_dispersion = unpacked[5]
        packet.reference_identifier = unpacked[6]
        
        # Extract timestamps
        packet.t1 = unpacked[7] + unpacked[8] / (2**32)
        packet.t2 = unpacked[9] + unpacked[10] / (2**32)
        packet.t3 = unpacked[11] + unpacked[12] / (2**32)
        packet.t4 = unpacked[13] + unpacked[14] / (2**32)

        return packet



    def __str__(self) -> str:
        return (
            f"t1: {self.t1}, t2: {self.t2}, t3: {self.t3}, t4: {self.t4}, "
            f"leap_indicator: {self.leap_indicator}, version: {self.version}, mode: {self.mode}, "
            f"stratum: {self.stratum}, poll: {self.poll}, precision: {self.precision}, "
            f"root_delay: {self.root_delay}, root_dispersion: {self.root_dispersion}"
        )

