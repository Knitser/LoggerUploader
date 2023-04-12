import esptool

port = "/dev/ttyUSB0"
baudrate = 115200
chip_type = "esp32"
firmware_path = "/path/to/firmware.bin"

# Create an instance of the esptool.ESP32Serial class
esp = esptool.ESP32Serial(port=port, baudrate=baudrate)

esptool.write_flash(
    esp,
    0,
    firmware_path,
    chip_type=chip_type,
    verify=True,
    erase_all=True
)

print("Firmware flashed successfully!")
