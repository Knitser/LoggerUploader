import zmq

# create a ZeroMQ context
context = zmq.Context()

# create a ZeroMQ socket of type REQ (request)
socket = context.socket(zmq.REQ)

# connect the socket to the server address and port
socket.connect("tcp://localhost:5555")

# prompt the user for a command
command = input("Enter a command: ")

# send the command to the server
socket.send(command.encode())

# wait for a reply from the server
response = socket.recv()

# print the response from the server
print(response.decode())
