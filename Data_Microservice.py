"""
Handles the data writing and reading to the user's json file
"""

import zmq
import json

# make connection to main program
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5020")


def get_data(username):
    """
    Returns all the data in the user's json file for handling (this data gets changed from the moment
    the pokemon tracker instance is created
    :return:
    """

    with open(f'{username}.json', 'r') as file:
        data = json.load(file)

    return data
def write_data(message):
    """
    Updates all the data in the json file
    :return:
    """

    username, update = message[1], message[2]
    with open(f'{username}.json', 'w') as file:
        file.write(json.dumps(update, indent=4))

while True:

    message = socket.recv_json()
    
    print("Receiving Message")
    print(message)

    if message[0] == 'data':
        username = message[1]

        data = get_data(username)
        socket.send_json(data)

    elif message[0] == 'update':
        write_data(message)
        socket.send_string('updated')




