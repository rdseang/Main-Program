from PIL import Image
import zmq
import json

# setup zmq environment for client
# connects to filter microservice made by classmate
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# connects to data_microservice
context_2 = zmq.Context()
socket_2 = context_2.socket(zmq.REQ)
socket_2.connect("tcp://localhost:5020")

# connects to user_microservice
context_3 = zmq.Context()
socket_3 = context_2.socket(zmq.REQ)
socket_3.connect("tcp://localhost:5100")

# connects to trading_microservice
context_4 = zmq.Context()
socket_4 = context_4.socket(zmq.REQ)
socket_4.connect("tcp://localhost:5200")


class PokemonTracker:

    def __init__(self, username, collections=[]):
        self._username = username
        self._collections = collections

    def get_data_microservice(self, username):
        """
        Calls the data_microservice to get data
        :return: the list of collections in the user json file
        """

        # send message to microservice to get data
        socket_2.send_json(('data', username))

        # decode message received in json format
        list_collections = socket_2.recv_json()
        return list_collections

    def update_data_microservice(self, username, update):
        """
        Calls the data microservice to update data
        :return: None
        """
        # send message to microservice to update data
        socket_2.send_json(('update', username, update))
        message = socket_2.recv()           # don't really do anything with this...just needs a response


    def homepage(self):
        """
        The homepage for the pokemon tracker object
        """

        # loop input until valid input
        is_valid = False
        count = 0 # so options only show upon entering the home state

        # handles all the actions
        while is_valid is False:
            if count == 0:
                print()
                print("[HOMEPAGE]-------------------------------------------\n")
                print("Options:\n"
                    "'V' to VIEW Collections\n"
                    "'+' to ADD a card \n"
                    "'F' to view cards by FILTER parameter\n"
                    "'>> to TRADE cards with another user\n"
                    "'++' to ADD a new collection (Group your cards to organize them!)\n"
                    "'Q' to QUIT\n")
                count = 1

            # view collections
            action = input("What would you like to do? ")
            if action == 'V' or action == 'v':
                self.view_collections()
                count = 0

            # add a card
            elif action == '+':
                self.add_card_screen()
                count = 0

            elif action == 'F' or action =='f':
                self.filter_card_screen(self._username)
                count = 0

            elif action == '>>':
                self.trade_card_screen()
                count = 0

            elif action == '++':
                self.add_new_collection()
                # go into add a new collection
                count = 0

            elif action == 'Q' or action == 'q':
                print('See you next time!')
                is_valid = True
                return

            else:
                print('Please enter a valid input.\n')
                count = 1


    def view_collections(self):
        '''
        Allows the user to view their collections
        * WILL CALL MICROSERVICE FOR [COLLECTIONS] HERE * since this changes
        :return:
        '''


        is_valid = False
        count = 0
        list_collections = self.get_data_microservice(self._username)
        if list_collections is None or list_collections == []:
            print("\n**No collections to view**")
            return

        self._collections = list_collections
        while is_valid is False:
            if count == 0:

                print()
                print('[COLLECTIONS]--------------------------------------\n')

                # display all collections
                for i in range(len(list_collections)):
                    name = self._collections[i]["collection_name"]
                    print(f'({i+1}) {name}')
                print('\n(other options)')
                print("'H' to return HOME")
                print("'D' to delete a collection\n")
                count = 1

        # loop until a valid input
            print("*collections are CASE SENSITIVE*")
            action = input("Please select a collection: ")
            if action == 'H' or action == 'h':
                is_valid = True
                return  # goes back to the homepage

            elif action == 'D' or action == 'd':
                action_delete = input("Which would you like to delete? ")
                for collection in self._collections:
                    if action_delete == collection["collection_name"]:
                        action_check = input('Are you sure you want to delete this collection"\n'
                                             'There is no undoing this (Y/N) ')
                        if action_check == 'Y' or action_check == 'y':

                            # send
                            self._collections.remove(collection)
                            update = self._collections
                            self.update_data_microservice(self._username, update)   # needed to update json file
                            print('Collection deleted')
                            count = 0
                        else:
                            print('Collection not removed')
                            count = 1


            else:
                for collection in self._collections:
                    if action == collection["collection_name"]:
                            action_view = self.view_single_collection(collection)
                            if action_view == 'h' or action_view == 'H':
                                return # go back home from viewing
                            count = 0

                continue    # keep looping until valid input



    def view_single_collection(self, collection):  
        '''
        allows a user to view the cards in a single selection
        :param collection: an object with the collection name, and a list of card objects
        :return: action is H, to return home
        '''

        count = 0
        is_valid = False

        while is_valid is False:
            if count == 0:
                print(f'\n[{collection["collection_name"]}]-----------------------------------\n')
                card_list = collection["card_list"]
                
                # iterate through and print all the card names
                for i in range(len(card_list)):
                    print(f'({i+1}) {card_list[i]["card_name"]}')

                print('\n(options)')
                print("'H' to return HOME\n"
                      "'C' to return to COLLECTIONS\n")

            print("*card names are CASE SENSITIVE*")
            action = input("\nPlease select a card: ")
            action_view_info = None

            # to account for multiple cards of same name
            card_count = 0
            sub_card_list = []
            show_card = None

            for card in card_list: # multiple cards with same name, make a smaller list and choose one
                if action == card["card_name"]:
                    card_count += 1
                    if card_count == 1:
                        unique = True
                        show_card = card
                        sub_card_list.append(show_card)
                    elif card_count > 1:
                        unique = False
                        sub_card_list.append(card)

            if card_count == 1:
                action_view_info = self.view_card_info_screen(show_card, collection)
                if action_view_info == 'H' or action_view_info == 'h':
                    return action_view_info

            elif card_count > 1:
                action_view_info = self.sub_collection(sub_card_list, collection)
                if action_view_info == 'H' or action_view_info == 'h':
                    return action_view_info

            # if the user wants to return to the collection from viewing a card
            if action_view_info == 'C' or action_view_info == 'c':
                count = 0

            elif action_view_info is True:
                count = 0

            elif action == 'H' or action == 'h':
                is_valid = True
                return action

            elif action == 'C' or action == 'c':
                is_valid = True
                return # go back to collections

            else:
                print("Card not found!")
                count = 1



    def display_card_info(self, card):
        '''
        prints all of a card's info
        :param card:
        :return:
        '''

        print(f'\n[{card["card_name"]}]----------------------------------------------')

        print(f'\nCollection: {card["collection_name"]}')
        print(f'\nSet: {card["set_name"]}')
        print(f'Type: {card["card_type"]}')
        print(f'Rarity: {card["card_rarity"]}')
        print(f'Market Price: {card["market_price"]}')
        print(f'Path to Image: {card["image_path"]}')
        print(f'Additional Comments: {card["comments"]}')


    def view_card_info_screen(self, card, collection):
        '''
        allows the user to see the card's info, the [card info state]
        * will user COLLECTION microservice later *
        :param card:
        :return:
        '''

        self.display_card_info(card)

        # shows the user's options
        print('\n(options)')
        print("'I' to view the card IMAGE")
        print("'C' to return to the COLLECTION")
        print("'D' to DELETE the card")
        print("'E' to EDIT card info")
        print("'H' to return HOME")

        is_valid = False

        # loop until a valid input
        while is_valid is False:
            action = input('What would you like to do? ')

            # view the image
            if action == "I" or action == 'i':
                #is_valid = False
                # follow the path to show the image
                if card["image_path"] == '':
                    print("No image provided!")
                else:
                    try:
                        with Image.open(card["image_path"]) as img:
                            img.show()
                    except IOError:
                        print("Image not found!")


            # return to the collection
            elif action == 'C' or action == 'c':
                is_valid = True
                return action # this goes out of this function and back to the view collection function that calls it

            # delete the card
            elif action == 'D' or action == 'd':
                print('\nAre you sure you want to delete this card?')
                action_delete = input('\nThere is no undoing this (Y/N) ')
                if action_delete == 'Y' or action_delete == 'y':
                    # delete card from list in collection
                    collection["card_list"].remove(card)

                    # self._collections is updated, now update json file here
                    self.update_data_microservice(self._username, self._collections)

                    print('Card deleted')
                    go_back = True
                    return go_back # go back to view collection function
                else:
                    continue

            elif action == 'H' or action == 'h':
                return action # go back home

            # edit card info
            elif action == 'E' or action == 'e':
                self.edit_card(card)
                action = 'h'
                return action # go back home


# handles adding a new card ---------------------------
    def add_card_screen(self):
        '''
         Adds a new card to the collection
        * will use [COLLECTION] microservice
        '''

        print("\n[ADD CARD]---------------------------------------")
        added_card = self.new_card()
        collection_name = added_card["collection_name"]

        # find the matching collection in collections, if collection is found, add it to the list of cards
        for collection in self._collections:
            if collection["collection_name"] == collection_name:
                collection["card_list"].append(added_card)

                # need to actually find the collection based off the name
                print(f'\nCard added to {collection["collection_name"]}!')
                self.display_card_info(added_card)
                # add card to the json file with microservice
                update = self._collections
                self.update_data_microservice(self._username, update)

        print("\n(options)\n"
              "'E' to EDIT, '+' to ADD another card, 'H' to return HOME")

        is_valid = False
        while is_valid is False:
            action = input("What would you like to do? ")
            if action == 'h' or action == 'H':
                return
            elif action == 'E' or action == 'e':
                self.edit_card(added_card)
                return
            elif action == '+':
                self.add_card_screen()
                return


    def new_card(self):
        '''
        allows the user to add a new card to a collection
        '''

        card_name = input("Card Name: ")

        # make user input a valid collection
        collection_name = self.collection_validation(False)


        set_name = input("Set Name: ")
        card_type = input("Type: ")
        card_rarity = input("Rarity: ")

        # only float values are allowed
        market_price = self.market_price_validation(False)


        image_path = input("Path to Image: ")
        comments = input("\nAdditional Comments: ")

        new_card = {
            "card_name": card_name,
            "collection_name": collection_name,
            "set_name": set_name,
            "card_type": card_type,
            "card_rarity": card_rarity,
            "market_price": market_price,
            "image_path": image_path,
            "comments": comments
        }
        return new_card


    def edit_card(self, card):
        '''
        Allows the user to edit a card info
        :return:
        '''

        is_valid = False
        print("\n[EDIT CARD]-----------------------------------------\n")

        while is_valid is False:
            self.display_card_info(card)
            print("'H' to return HOME")
            parameter = input("Please enter a parameter to edit or A for all: ")
            parameter = parameter.lower()  # so  case doesn't matter

            # change the name
            if parameter == 'name':
                card["card_name"] = input('New name: ')


            if parameter == 'collection':
                # make user input a valid collection
                current_collection = card["collection_name"]
                collection_name = self.collection_validation(False)
                card["collection_name"] = collection_name

                # need to pass the objects to the function
                for collection in self._collections:
                    if current_collection == collection["collection_name"]:
                        current_collection = collection     # change it to object
                    elif collection_name == collection["collection_name"]:
                        collection_name = collection

                # move card to different collection
                if current_collection != collection_name:
                    self.move_collection(card, current_collection, collection_name)

            if parameter == 'set':
                card["set_name"] = input("New set name: ")

            if parameter == 'rarity':
                card["rarity"] = input("New rarity: ")

            if parameter == 'type':
                card["card_type"] = input("New type: ")

            if parameter == 'market price':
                # only string of float values are allowed
                market_price = self.market_price_validation(False)
                card["market_price"] = market_price

            if parameter == 'path to image':
                card["image_path"] = input("New image path: ")

            if parameter == 'additional comments':
                card["comments"] = input("Updated comments: ")

             # update all the info
            if parameter == 'a':
                card["card_name"] = input('New name: ')

                # make user input a valid collection
                collection_name = self.collection_validation(False)
                if current_collection != collection_name:
                    self.move_collection(card, current_collection, collection_name)

                card["set_name"] = input("New set name: ")
                card["rarity"] = input("New rarity: ")
                card["card_type"] = input("New type: ")
                card["market_price"] = input("New market price: ")
                card["image_path"] = input("New image path: ")
                card["comments"] = input("Updated comments: ")


            # need to update the json file
            self.update_data_microservice(self._username, self._collections)

            if parameter == 'h':
                return # return to the view card info state
                is_valid = True


    def filter_card_screen(self, username):
        """
        Takes a user input and returns a list of cards filtered by the parameters:
        :return: displays all the cards that match the parameter
        """
        print("[FILTER CARDS]-----------------------------------------------")

        filtered_list = self.find_card(username)

        # display each card
        print("\n[FILTERED LIST]------------------------------------------------------------------")
        for i in range(len(filtered_list)):
            print()
            print(f'[{i+1}] ------------ V V V V V V V V V V V --------------')
            self.display_card_info(filtered_list[i])

        print("-----------------------------------------------------------------------------------")
        return

    def find_card(self, username):
        print("Please enter...\n")
        name = input("Card Name: ")
        card_type = input("Type: ")
        rarity = input("Rarity: ")
        collection = input("Collection: ")
        set_name = input("Set: ")

        # for a valid order input
        print("\n[For increasing, press enter]\n[For decreasing, enter 'decreasing']")
        is_valid = False
        while is_valid is False:
            order = input("Order: ")
            order = order.lower()

            if order == '':  # if user presses enter
                is_valid = True
            elif order == 'decreasing':
                is_valid = True
            else:
                is_valid = False

        filter = {"card_name": name,
                  "collection_name": collection,
                  "set_name": set_name,
                  "card_type": card_type,
                  "card_rarity": rarity,
                  "order": order,
                  "json_path": f'/Users/ryan/PycharmProjects/CS361_Pokemon_Card_Tracker/{username}.json'
                  }

        # convert object to bytes with charset UTF-8 and send to microservice
        filter_string = json.dumps(filter)
        filter_bytes = filter_string.encode('utf-8')
        socket.send(filter_bytes)

        # receive the data a string from the microservice
        message = socket.recv()
        message = message.decode('utf-8')

        # convert the string into an actual dictionary list to use
        filtered_list = json.loads(message)

        return filtered_list

    # handles adding a new collection -------------------------------
    def add_new_collection(self):
        '''
        Allows the user to add a new collection
        :return:
        '''

        is_valid = False
        count = 0
        while is_valid is False:
            if count == 0:
                print('\n[ADD NEW COLLECTION]')
                print("\n'H' to return HOME\n")

            collection_name = input('Collection Name: ')
            # if the user doesn't input anything, try again or just quit
            if collection_name == 'H' or collection_name == 'h':
                return

            # invalid input
            elif len(collection_name) < 2:
                print("Please enter a name with 2 or more letters")
                count = 1
                continue

            # create and add a new collection object
            else:
                count = 1
                new_collection = {"collection_name": collection_name, "card_list": []}
                self._collections.append(new_collection)
                self.update_data_microservice(self._username, self._collections)
                print('Collection Added!')

                yes_or_no = False
                while yes_or_no is False:
                    # if user wants to add another collection
                    action = input('Make another collection? (Y/N) ')
                    if action == 'Y' or action == 'y':
                        yes_or_no = True    # go through loop again
                    elif action == 'N' or action == 'n':
                        return # go back home
                    else:
                        continue # reprompt y/n
                continue

    def sub_collection(self, sub_card_list, collection):
        """
        Prompts user to choose one of the cards with duplicate names
        :param sub_card_list: a list
        :return:
        """
        for i in range(len(sub_card_list)):
            print(f'({i+1}) {sub_card_list[i]["card_name"]}')

        is_valid = False
        while is_valid is False:
            action = input('\nWhich card? Please enter a number: ')
            if action.isnumeric() is False:
                print("Must be a number!")
                continue

            # assuming user chooses number i + 1
            action = int(action) - 1
            if action > len(sub_card_list) - 1:
                print("Invalid number!")
                continue
            else:
                action = self.view_card_info_screen(sub_card_list[action], collection)
                return action

    def move_collection(self, card, current_collection, new_collection):
        """
        moves a card from the current collection to a different collection
        :param current_collection:
        :param new_collection:
        :return:
        """
        # delete the card from the current collection
        if card in current_collection["card_list"]:
            current_collection["card_list"].remove(card)
            new_collection["card_list"].append(card)
            # self._collections is updated, now update json file here
            self.update_data_microservice(self._username, self._collections)


        # add the card to the new collection
    def micro_request(self, action):
        """
        Makes a request from a microservice. To be used in multiple functions
        :return: a decoded message from the microservice
        """
        socket.send_string(action)
        message = socket.recv()
        return message.decode()

    def market_price_validation(self, is_valid):
        """
        Takes the user input for the market price and validates it
        :return: string market price
        """
        while is_valid is False:
            market_price = input("Market Price: ")
            # check if the input can be a float
            is_valid = is_float(market_price)
        # if input can be a float, exit the while loop and convert to float
        market_price = float(market_price)
        # convert to string to work with microservice
        return str(market_price)

    def collection_validation(self, is_valid):
        """
        Takes the user input for the collection and validates it
        :return: string collection name
        """
        while is_valid is False:
            collection_name = input("Collection Name: ")
            for i in range(len(self._collections)):
                if collection_name == self._collections[i]["collection_name"]:
                    return collection_name
            if is_valid is False:
                print("Please input an existing collection!")


    def trade_card_screen(self):
        """
        Screen prompting user to trade cards
        :return: None
        """
        print("\n[TRADE CARD]------------------------------------------------------------------")
        print("*At any time, you may enter 'H' to return to Homepage*")

        # sends the current username for process in trading microservice
        socket_4.send_json((1, self._collections))
        socket_4.recv()

        while True:
            user_trade = input("\nWith who would you like to trade with? ")

            if user_trade == 'H' or user_trade == 'h':
                return                                                      # return to Homepage

            # so user does not switch cards with themselves
            if user_trade == self._username:
                print('Cannot trade with yourself!')

            else:
                # validate that user to trade with exists by connect with user microservice
                socket_3.send_json((1, user_trade))                             # 1 = id for searching for user
                message = socket_3.recv()
                message = message.decode()

                if message == 'User not found!':
                    print(message)
                    continue
                if message == 'Found':
                    print('User found!')

                    # get the user_trade data and to trading microservice
                    user_trade_data = self.get_data_microservice(user_trade)

                    # check if user has anything to trade
                    if user_trade_data == []:
                        print('User has no cards to trade!')
                        return

                    count = 0
                    for collection in user_trade_data:
                        if collection["card_list"] != []:
                            count += 1

                    if count == 0:
                        print('User has no cards to trade!')
                        return

                    socket_4.send_json((2, user_trade_data))
                    socket_4.recv()
                    self.trade_card(user_trade)
                    break
        return

    def find_card_to_trade(self, username):
        """
        Allows the user to trade a card with provided user
        :param username: The user of which finding a card to trade
        :return: card
        """

        # use filter fx to find the card to trade
        while True:
            print(f"\nPlease input the following info for the card from [{username}] you would like to trade.")
            filtered_list = self.find_card(username)
            if filtered_list == []:
                print('Card not found!')

            elif len(filtered_list) == 1:           # 1 card found with the parameters
                card = filtered_list[0]
                print(f'Trading [{card["card_name"]}]...')
                break

            # more than one card found with the parameters, let user choose
            elif len(filtered_list) > 1:
                print(f"\n{len(filtered_list)} cards found")
                for i in range(len(filtered_list)):
                    print(f"[{i+1}] {filtered_list[i]['card_name']}")
                action = -1
                while action not in range(1, len(filtered_list)+1):         # loop for valid input
                    try:
                        action = input("Please choose a card to trade: ")
                        action = int(action)
                    except ValueError:
                        print('Please input an integer')
                card = filtered_list[action-1]
                print(f'Trading [{card["card_name"]}]...')
                break
        return card

    def trade_card(self, user_trade):
        """
        Allows the user to trade with another user
        :param user_trade:
        :return:
        """
        # find cards to trade for both users
        card_1 = self.find_card_to_trade(self._username)
        card_2 = self.find_card_to_trade(user_trade)

        # send to trading microservice for processing
        socket_4.send_json((3, (card_1, card_2)))
        message = socket_4.recv_json()
        update_1, update_2 = message[0], message[1]

        # update the collections of both users
        self._collections = update_1
        self.update_data_microservice(self._username, self._collections)
        self.update_data_microservice(user_trade, update_2)
        print('Trade successful!')
        return
def is_float(num):
    """
    Converts the number into a float and returns the number if it is possible and False if not
    :param num:
    :return:
    """
    try:
        num = float(num)
        is_valid = True
        return True
    except ValueError:
        print('Please only enter numbers with/without a decimal. If unsure, enter 0')
        return False
    except SyntaxError:
        print('Please only enter numbers with/without a decimal. If unsure, enter 0')
        return False

def user_validation():
    """
    Validates a user by calling the user microservice
    :return: a string username, string path_json
    """
    is_valid = False
    while is_valid is False:
        username = input("Please enter your username or 'Q' to quit: ")

        # if user doesn't input anything, reprompt
        if len(username) < 1:
            continue

        # quit
        if username == 'q' or username == 'Q':
            return username

        else:
            # call microservice to see if valid
            socket_3.send_json((1, username))
            message = socket_3.recv()
            message = message.decode()

            if message == 'User not found!':
                # would you like to create a new user?
                print(message)
                while True:
                    action = input('Would you like to create a new user? (Y/N) ')
                    action = action.lower()
                    if action == 'n':
                        break
                    elif action == 'y':
                        new_username = make_username()
                        return new_username
                    else:
                        continue

            elif message == 'Found':
                is_valid = True
                return username

def make_username():
    """
    Walks through making a new username
    :return: string username, json_path of username
    """
    print("\n[CREATE NEW USER]------------------------------\n"
          "\nFor a new username, no spaces are not allowed\n"
          "Usernames are NOT case sensitive.\n")

    while True:
        new_username = input("Please enter a new username: ")
        if ' ' in new_username:
            print('No spaces allowed!')
            continue

        elif new_username is None:
            continue

        else:
            socket_3.send_json((2, new_username))
            message = socket_3.recv()               # new username created
            message = message.decode()
            if message == 'Name already taken.':
                continue
            else:
                print(message)
                return new_username

#-----------------------------------------




# Welcome page
print("Welcome to the pokemon card collection app! \nHere you can keep track and organize all the "
        "cards you've collected.\n\n")


username = user_validation()

# make a username validation function here
if username == 'Q' or username == 'q':
    print("See you next time!")

# enter the Home Page if user file found
else:
    with open(f'{username}.json', 'r') as infile:
        collections = json.load(infile)
    my_tracker = PokemonTracker(username, collections)
    my_tracker.homepage()


