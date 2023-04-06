import can
import time

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
            print("[OBD] pid sent: ", pid)
            obd_send_pid_msg(pid)
            time.sleep(OBD_PID_REQ_INTERVAL)


def obd_send_pid_msg(pid):
    obdts = time.time()
    msg = can.Message(timestamp=obdts, arbitration_id=PID_REQUEST, data=[0x02, 0x01, pid, 0x00, 0x00, 0x00, 0x00, 0x00],
                      is_extended_id=False)
    print("[OBD] msg sent: ", msg)


obd_tx_task()
