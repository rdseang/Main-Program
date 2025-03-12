"""
Microservice that handles the user file creation, validation
"""

import zmq
import json

# make connection to main program
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5100")


def look_for_user(username):
    """
    Looks for a user by trying to open a file
    :param username: a string
    :return: None
    """
    try:
        with open(f'{username}.json', 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        return 'User not found!'

    # if file is found, then it can be opened
    return 'Found'

def create_user_file(new_username):
    """
    Creates a new user file with given username, with default empty collection: 'My Collection'
    :param new_username: string
    :return: None
    """

    # if a user with that name already exists
    found = look_for_user(new_username)
    if found == 'Found':
        # dont make the user
        return 'Name already taken.'

    else:
        user_data = [{"collection_name": "My Collection", "card_list": []}]
        with open(f'{new_username}.json', 'w') as outfile:
            json.dump(user_data, outfile)
        return 'User created.'

while True:

    message, username = socket.recv_json()
    print("Receiving Message")
    print(message)
    print(username)

    # for validating username
    if message == 1:
        message = look_for_user(username)

        if message == 'User not found!':
            socket.send_string(message)

        if message == 'Found':
            socket.send_string(message)

    # for creating a new user
    elif message == 2:
        new_username = username
        message = create_user_file(new_username)
        socket.send_string(message)

