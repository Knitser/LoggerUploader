import can
import time


class Obd:
    @staticmethod
    def get_vin(bus):
        """Get VIN over OBD"""

        # Set up constants
        VEHICLE_VIN = 0x02
        PID_REQUEST = 0x7DF
        PID_REPLY = 0x7E8
        FLOW_CONTROL = 0x7E0

        # Send PID request to get VIN
        msg = can.Message(arbitration_id=PID_REQUEST,
                          data=[0x02, 0x09, VEHICLE_VIN, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
        bus.send(msg)
        time.sleep(0.05)

        # Wait for response and process VIN
        vin = ""
        message = bus.recv()
        if message is not None and message.arbitration_id == PID_REPLY:
            vin = ''.join(format(x, '02x') for x in message.data)[10:]

            # Continue processing VIN
            msg = can.Message(arbitration_id=FLOW_CONTROL,
                              data=[0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
            bus.send(msg)
            time.sleep(0.05)

            message = bus.recv()
            if message is not None and message.arbitration_id == PID_REPLY:
                vin2 = ''.join(format(x, '02x') for x in message.data)[2:]
                vin += vin2

                message = bus.recv()
                if message is not None and message.arbitration_id == PID_REPLY:
                    vin3 = ''.join(format(x, '02x') for x in message.data)[2:]
                    vin += vin3

        # Decode VIN and return
        try:
            decoded_vin = bytes.fromhex(vin).decode("utf-8")
            return decoded_vin
        except ValueError:
            print("Error decoding VIN")
            return ""
