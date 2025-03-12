import zmq
import json

"""
Allows two users to trade with each other
"""

# make connection to main program
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5200")

def trade_cards(collections_user1, collections_user2, card_user1, card_user2):
    """
    Trades cards between users
    :param collections_user1: a list of collections
    :param collections_user2: a list of collections
    :param card_user1: a card object
    :param card_user2: a card object
    :return: a tuple of two updated collection lists to write to json file
    """
    # delete cards from both user collections
    for collection in collections_user1:
        card_list = collection["card_list"]
        for card in card_list:
            if card == card_user1:
                card_list.remove(card)

    for collection in collections_user2:
        card_list = collection["card_list"]
        for card in card_list:
            if card == card_user2:
                card_list.remove(card)

    # for each user, make new collection "Traded Cards", (if don't already have one) and add the cards there
    make_traded_collection(collections_user1)
    make_traded_collection(collections_user2)

    card_user1["collection_name"] = "Traded Cards"
    card_user2["collection_name"] = "Traded Cards"

    for collection in collections_user1:
        if collection["collection_name"] == "Traded Cards":
            card_list = collection["card_list"]
            card_list.append(card_user2)

    for collection in collections_user2:
        if collection["collection_name"] == "Traded Cards":
            card_list = collection["card_list"]
            card_list.append(card_user1)

    return collections_user1, collections_user2



def make_traded_collection(user_collections):
    """
    Makes a new collection of traded cards if one is not already there
    :param user_collections: a list of collections
    :return: None
    """
    coll_made = False
    for collection in user_collections:

        # if the collection was found
        if collection["collection_name"] == "Traded Cards":
            coll_made = True

    # if collection not found, make a new collection
    if coll_made is False:
        user_collections.append({"collection_name": "Traded Cards", "card_list": []})

    return


while True:

    message = socket.recv_json()
    print("Message received")
    print(message)
    id, data = message[0], message[1]

    if id == 1:
        print("Received data for user 1")
        collections_user1 = data
        socket.send_string('received')

    elif id == 2:
        print("Received data for user 2")
        collections_user2 = data
        socket.send_string('received')

    elif id == 3:
        print("Received card data for both users")
        card_user1, card_user2 = data[0], data[1]
        # now have all the data to trade cards
        update = trade_cards(collections_user1, collections_user2, card_user1, card_user2)
        print("cards traded")
        socket.send_json(update)






