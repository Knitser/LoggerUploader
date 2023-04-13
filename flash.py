import os


class EspFlasher:
    def __init__(self, port, baudrate, chip_type):
        self.port = port
        self.baudrate = baudrate
        self.chip_type = chip_type

    def flash_firmware(self, files, before=None, after=None, no_stub=False, trace=False, override_vddsdio=None,
                       connect_attempts=None, flash_mode=None, flash_freq=None, flash_size=None):
        cmd = f"esptool.exe --chip {self.chip_type} " \
              f"--port {self.port} " \
              f"--baud {self.baudrate} "
        if before:
            cmd += f"--before {before} "
        if after:
            cmd += f"--after {after} "
        cmd += "write_flash"
        for address, file_path in files:
            cmd += f" {address} {file_path}"
        if flash_mode:
            cmd += f" --flash_mode {flash_mode}"
        if flash_freq:
            cmd += f" --flash_freq {flash_freq}"
        if flash_size:
            cmd += f" --flash_size {flash_size}"
        if no_stub:
            cmd += " --no-stub"
        if trace:
            cmd += " --trace"
        if override_vddsdio:
            cmd += f" --override-vddsdio {override_vddsdio}"
        if connect_attempts:
            cmd += f" --connect-attempts {connect_attempts}"
        print("Flashing firmware...")

        result = os.system(cmd)

        if result != 0:
            error_message = f"Firmware flashing failed with error code {result}."
            raise RuntimeError(error_message)

        print("Firmware flashed successfully")


files_to_flash = [
    # ("0x0000", "bootloader.bin"),
    # ("0x8000", "partitions.bin"),
    # ("0xe000", "boot_app0.bin"),
    ("0x10000", "flash/firmware.bin"),
]

flasher = EspFlasher(port="COM1", baudrate=115200, chip_type="esp32")
flasher.flash_firmware(files_to_flash, before='default_reset', after='hard_reset', flash_mode='dio', flash_freq='40m', flash_size='4MB')
