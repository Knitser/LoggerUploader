import socket
import time

IMEI = "123456789012345"
FW_VERSION = "1.00.0001"
HOST = "backend.example.com"
PORT = 1234


def login():
    while True:
        try:
            # Step 1: Open a TCP and create an active TCP connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                # Step 2: Send the login message
                message = f"#LinkedCar|{IMEI}|MVP1|{FW_VERSION}\n".encode()
                s.sendall(message)
                # Step 3: Wait for the response
                response = s.recv(1024)
                if response == b"\x06":
                    print('login successfully')
                    return True
                elif response == b"\x21":
                    print('login failed, wait 1 minute and try again')
                    time.sleep(60)
                else:
                    pass
        except ConnectionRefusedError:
            # Connection error, retry immediately
            pass
        except socket.timeout:
            # Timeout error, retry immediately
            pass
        except OSError:
            # OS error, retry immediately
            pass
        except KeyboardInterrupt:
            # User interrupt, exit immediately
            print("User interrupt")
            return False
