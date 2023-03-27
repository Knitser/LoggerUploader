import can
import time

BALENA_VIN = "NOVIN"

# PID
PID_REQUEST = 0x7DF
PID_REPLY = 0x7E8
OBD_INDEX = 0
OBD_PID_REQ_INTERVAL = 0.03  # interval time in ms

PID_ARR = [
    0x0D, 0x4A, 0x0C, 0x04, 0x05, 0x11, 0x0B, 0x0E, 0x0F,
    0x10, 0x23, 0x33, 0x42, 0x43, 0x46, 0x4F, 0x2F, 0x14
]

def obd_tx_task():
    while True:
        for pid in PID_ARR:
            obd_send_pid_msg(pid)
        time.sleep(0.1)


def obd_send_pid_msg(pid):
    # send obd message
    msg = can.Message(arbitration_id=PID_REQUEST, data=[0x02, 0x01, pid, 0x00, 0x00, 0x00, 0x00, 0x00],
                      extended_id=False)

    try:
        bus_obd.send(msg)
    except Exception as ex:
        print('Failed sending obd msg')
        print(ex)
    else:
        # add obd message to log file
        obd_q.put(msg)
        time.sleep(0.05)


# ----------------------------------------------------------------------------------------------------------------------
# Get answer on PID request
# ----------------------------------------------------------------------------------------------------------------------

def obd_get_pid_msg(msg, pid):
    if msg.arbitration_id == PID_REPLY and msg.data[2] == pid:
        obd_c = '{0:f} {3}  {1:03x}        Rx D {2:x}  '.format(msg.timestamp, msg.arbitration_id, msg.dlc,
                                                                config["log_channel"]["obd"])
        obd_s = ''

        for i in range(msg.dlc):
            obd_s += '{0:02x}  '.format(msg.data[i])

        out = obd_c + obd_s

        # Put can channel in message on last place in array
        msg.data.append(config["log_channel"]["obd"])

        # Put data in queue
        q.put(msg)

        return out
