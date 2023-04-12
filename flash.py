import subprocess


class EspFlasher:
    def __init__(self, port, baudrate, chip_type):
        self.port = port
        self.baudrate = baudrate
        self.chip_type = chip_type

    def flash_firmware(self, firmware_path):
        cmd = [
            "esptool.exe",
            "--chip", self.chip_type,
            "--port", self.port,
            "--baud", str(self.baudrate),
            "write_flash", "0x0", firmware_path
        ]
        print(cmd)

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print("Error flashing firmware:")
            print(result.stderr.decode())
        else:
            print("Firmware flashed successfully!")


flasher = EspFlasher(port="COM5", baudrate=115200, chip_type="esp32")
flasher.flash_firmware(firmware_path="firmware.bin")
