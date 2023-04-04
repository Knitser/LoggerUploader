import cantools
import can
import queue

# ----------------------------------------------------------------------------------------------------------------------
# Realtime settings
# ----------------------------------------------------------------------------------------------------------------------
REALTIME_DATA = {"message_counter": 0}
RT_INTERVAL = 0.2  # sec.
REALTIME_MAP = {
    "D1_DC_Bus_Voltage": "bus_voltage",
    "D4_DC_Bus_Current": "bus_current",
    "D1_Analog_Input_1": "analog_in_1",
    "D3_Motor_Temperature": "motor_temperature",
    "D3_Id": "motor_id",
    "D4_Iq": "motor_iq",

    "D6_TOTAL_VOLTAGE__3rd_byte_": "total_voltage",
    "D1_MAX_CELL_TEMPERATURE": "max_cell_temp",
    "D0_MIN_CELL_VOLTAGE": "min_cell_temp",

    "gps_lat": "gps_lat",
    "gps_lon": "gps_lon",

    "Rondetijd": "lap_time",
    "Rolling_Time": "rolling_time",
    "Rolling_Sess_Time": "rolling_sess_time",
    "Lap_Number": "lap_number",
    "GPS_Speed": "gps_speed",
    "Best_Time": "best_time",
    "Bat_Voltage_12V": "bat_12v",

    "aim_gps_lat": "aim_lat",
    "aim_gps_lon": "aim_lon",
}


def realtime_processing_task():
    # set dbc file
    tesla_model_3 = cantools.db.load_file('TeslaModel3.dbc')

    q = queue.Queue()

    # filter id's
    inverter_filter = [0xA7, 0xA6, 0xA2, 0xA8, 0xA5, 0xA3]

    while True:
        # Check if there is a message in queue
        if not q.empty():
            # get can message
            message = q.get()

            # Create new can message
            msg = can.Message(arbitration_id=message.arbitration_id, data=message.data)

            # Filter only on needed id's - inverter
            if message.arbitration_id in inverter_filter:
                decoded = RealTime.decode_msg(tesla_model_3, msg.arbitration_id, msg.data)

                if decoded != -1:
                    for item in decoded:
                        if item in REALTIME_MAP:
                            REALTIME_DATA[REALTIME_MAP[item]] = decoded[item]
                    print(REALTIME_DATA)


class RealTime:
    @staticmethod
    def decode_msg(db, msg_id, msg):
        try:
            decoded_message = db.decode_message(msg_id, msg)
            return decoded_message
        except Exception as e:
            print(f"Error occurred while decoding CAN message with ID {msg.arbitration_id}: {e}")
            return -1
