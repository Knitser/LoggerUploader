import os


class EspFlasher:
    def __init__(self, port, baudrate, chip_type):
        self.port = port
        self.baudrate = baudrate
        self.chip_type = chip_type

    def flash_firmware(self, firmware_path):
        cmd = f"esptool.exe --chip {self.chip_type} " \
              f"--port {self.port} " \
              f"--baud {self.baudrate} " \
              f"write_flash 0x1000 {firmware_path}"
        print("Flashing firmware:", firmware_path)

        result = os.system(cmd)

        if result != 0:
            error_message = f"Firmware flashing failed with error code {result} for firmware {firmware_path}."
            raise RuntimeError(error_message)

        print("Firmware flashed successfully:", firmware_path)


flasher = EspFlasher(port="COM5", baudrate=115200, chip_type="esp32")
flasher.flash_firmware(firmware_path="flash/firmware.bin")
