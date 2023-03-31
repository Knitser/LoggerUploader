import zmq

# create a ZeroMQ context
context = zmq.Context()

# create a ZeroMQ socket of type REP (reply)
socket = context.socket(zmq.REP)

# bind the socket to a specific address and port
socket.bind("tcp://*:5555")

# run the server
while True:
    # wait for a request from the client
    message = socket.recv()

    # decode the message from bytes to string
    command = message.decode()

    # handle the command
    if command == "Start logging":
        print("Logging started!")
        response = "Logging has started."
    elif command == "Stop logging":
        print("Logging stopped!")
        response = "Logging has stopped."
    else:
        response = "Unknown command."

    # send a reply back to the client
    socket.send(response.encode())
