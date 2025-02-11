from PIL import Image
import json
import timeit
class PokemonTracker:

    # the default [] just for now
    def __init__(self, username, collections=[]):
        self._username = username
        self._collections = collections     # this will be nothing for now

    def homepage(self):
        '''
        The homepage for the pokemon tracker object
        :return:.
        '''

        # need to code this so it only shows options the first time

        # loop input until valid input
        is_valid = False
        count = 0 # so options only show upon entering the home state

        # handles all the actions
        while is_valid is False:
            if count == 0:
                print()
                print("[HOMEPAGE]\n")
                print("Options:\n"
                    "'V' to VIEW Collections\n"
                    "'+' to ADD a card \n"
                    #"'E' to EDIT a card's info\n"
                    "'++' to ADD a new collection (Group your cards to organize them!\n"
                    "'Q' to QUIT\n")
                count = 1

            # view collections
            action = input("What would you like to do? ")
            if action == 'V' or action == 'v':
                print('view collections')
                self.view_collections()
                count = 0
                #is_valid = True

            # add a card
            elif action == '+':
                print('add card')
                self.add_card_screen()
                count = 0
                #is_valid = True

            # elif action == 'E' or action == 'e':
            #     print('edit card')
            #     # go into edit card function
            #     self.edit_card(card,
            #     #is_valid = True
            #     count = 0

            elif action == '++':
                print('add a new collection')
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
        * WILL CALL MICROSERVICE FOR [COLLECTIONS] HERE *
        :return:
        '''

        is_valid = False
        count = 0
        while is_valid is False:
            if count == 0:

                print()
                # call [COLLECTION] microservice here to retrieve collection info
                print('[COLLECTIONS]\n')
                # for i in range(len(collections)):
                #     name = collections[i]['name']
                #     print(f'({i+1}) {name}')
                for i in range(len(self._collections)):
                    name = self._collections[i].get_name()
                    print(f'({i+1}] {name}')
                print('\n(other options)')
                print("'H' to return HOME")
                print("'D' to delete a collection\n")
                count = 1

        # loop until a valid input

            action = input("Please select a collection: ")
            if action == 'H' or action == 'h':
                is_valid = True
                return  # goes back to the homepage

            # call [COLLECTION] microservice here to actually delete the collection
            elif action == 'D' or action == 'd':
                action_delete = input("Which would you like to delete? ")
                for collection in collections:
                    if action_delete == collection.get_name():
                        action_check = input('Are you sure you want to delete this collection"\n'
                                             'There is no undoing this (Y/N) ')
                        if action_check == 'Y' or action_check == 'y':
                            collections.remove(collection)
                            print('Collection deleted')
                            count = 0
                        else:
                            print('Collection not removed')
                            count = 1

            # go into the collection to view # call [COLLECTION] microservice to return info to view the selection
            else:
                # for collection in collections:
                #     if action == collection["name"]:
                #         action_view = self.view_single_collection(collection)
                #         if action_view == 'h' or action_view == 'H':
                #             return # go back home from viewing
                #         count = 0
                for collection in self._collections:
                    if action == collection.get_name():
                            action_view = self.view_single_collection(collection)
                            if action_view == 'h' or action_view == 'H':
                                return # go back home from viewing
                            count = 0

                continue    # keep looping until valid input



    def view_single_collection(self, collection):  # will call microservice for this
        '''
        allows a user to view the cards in a single selection
        :param collection: an object with the collection name, and a list of card objects
        :return: action is H, to return home
        '''

        count = 0
        is_valid = False

        while is_valid is False:
            if count == 0:
                # print(f'\n[{collection["name"]}]\n')
                # card_list = collection["cards"]
                # # iterate through and print all the card names
                # for i in range(len(card_list)):
                #     print(f'({i+1}) {card_list[i]["name"]}')

                print(f'\n[{collection.get_name()}]')
                card_list = collection.get_cards()
                # iterate through and print all the card names
                for i in range(len(card_list)):
                    print(f'({i+1}) {card_list[i].card_name}')



                print('\n(options)')
                print("'H' to return HOME\n"
                      "'C' to return to COLLECTIONS\n")


            action = input("\nPlease select a card: ")
            action_view_info = None
            for card in card_list:
                if action == card.card_name:
                    action_view_info = self.view_card_info_screen(card, collection)
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



    def display_card_info(self, card, collection):
        '''
        prints all of a card's info
        :param card:
        :return:
        '''
        start = timeit.timeit()
        print(f'\n[{card.card_name}]')

        print(f'\nCollection: {card.collection_name}')
        print(f'\nSet: {card.set_name}')
        print(f'Type: {card.card_type}')
        print(f'Rarity: {card.card_rarity}')
        print(f'Market Price: {card.market_price}')
        print(f'Path to Image: {card.image_path}')
        print(f'\nAdditional Comments: {card.comments}')
        end = timeit.timeit()
        print(end-start)


    def view_card_info_screen(self, card, collection):
        '''
        allows the user to see the card's info, the [card info state]
        * will user COLLECTION microservice later *
        :param card:
        :return:
        '''



        # displays the card info
        # print(f'\n[{card["name"]}]')
        #
        # print(f'\nSet: {card["set"]}')
        # print(f'Type: {card["type"]}')
        # print(f'Rarity: {card["rarity"]}')
        # print(f'Market Price: {card["market price"]}')
        # print(f'Path to Image: {card["path to image"]}')
        # print(f'\nAdditional Comments: {card["additional comments"]}')
        self.display_card_info(card, collection)

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
                if card.image_path == '':
                    print("Image not found!")
                else:
                    try:
                        with Image.open(card.image_path) as img:
                            img.show()
                    except IOError:
                        print("Image not found!")

                # allow user to stay on this page so is_valid stays false to continue loop

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
                    #collection["cards"].remove(card)
                    collection.get_cards().remove(card)
                    print('Card deleted')
                    go_back = True
                    #is_valid = True
                    return go_back # go back to view collection function
                else:
                    continue

            elif action == 'H' or action == 'h':
                #is_valid = True
                return action # go back home

            # edit card info
            elif action == 'E' or action == 'e':
                self.edit_card(card, collection)
                action = 'h'
                return action # go back home


# handles adding a new card ---------------------------
    def add_card_screen(self):
        '''
         Adds a new card to the collection
        * will use [COLLECTION] microservice
        '''

        print("\n[ADD CARD]")
        added_card = self.new_card()
        collection_name = added_card.get_collection()

        # find the matching collection in collections, if collection is found, add it to the list of cards
        for collection in self._collections:
            if collection.get_name() == collection_name:
                collection.add_card(added_card)

                # need to actually find the collection based off the name
                print(f'\nCard added to {collection.get_name()}!')
                self.display_card_info(added_card, collection)

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
        is_valid = False
        while is_valid is False:
            collection_name = input("Collection Name: ")
            for i in range(len(self._collections)):
                if collection_name in self._collections[i].get_name():
                    is_valid = True
            if is_valid is False:
                print("Please input an existing collection!")

        set_name = input("Set Name: ")
        card_type = input("Type: ")
        card_rarity = input("Rarity: ")
        market_price = input("Market Price: ")
        image_path = input("Path to Image: ")
        comments = input("\nAdditional Comments: ")

        new_card = Card(card_name, collection_name, set_name, card_type, card_rarity,
                        market_price, image_path, comments)

        return new_card

# handles the edit card

    def edit_card(self, card, collection):
        '''
        Allows the user to edit a card info
        :return:
        '''

        is_valid = False

        while is_valid is False:
            self.display_card_info(card, collection)
            print("'H' to return HOME")
            parameter = input("Please enter a parameter to edit or A for all: ")
            parameter = parameter.lower()  # so  case doesn't matter

            # change the name
            if parameter == 'name':
                card.card_name = input('New name: ')

            #!!!! need to physically change this later
            if parameter == 'collection':
                card.card_collection = input('New collection: ')

            if parameter == 'set':
                card.set_name = input("New set name: ")

            if parameter == 'rarity':
                card.set_name = input("New rarity: ")

            if parameter == 'type':
                card.card_type = input("New type: ")

            if parameter == 'market price':
                card.market_price = input("New market price: ")

            if parameter == 'path to image':
                card.image_path = input("New image path: ")

            if parameter == 'additional comments':
                card.comments = input("Updated comments: ")

             # update all the info
            if parameter == 'a':
                card.card_name = input('New name: ')
                # !!!! need to physically change this later
                card.card_collection = input('New collection: ')
                card.set_name = input("New set name: ")
                card.set_name = input("New rarity: ")
                card.card_type = input("New type: ")
                card.market_price = input("New market price: ")
                card.image_path = input("New image path: ")
                card.comments = input("Updated comments: ")

            if parameter == 'h':
                return # return to the view card info state
                is_valid = True



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
                new_collection = Collection(collection_name)
                collections.append(new_collection)
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


class Card:
    '''
    Creates a card object
    :return:
    '''
    def __init__(self, card_name='', collection_name='', set_name='', card_type='', card_rarity='',
                 market_price='', image_path='', comments=''):
        # * WILL CHANGE THIS TO BE HANDLED BY A MICROSERVICE LATER *
        self.card_name = card_name
        self.collection_name = collection_name
        self.set_name = set_name
        self.card_type = card_type
        self.card_rarity = card_rarity
        self.market_price = market_price
        self.image_path = image_path
        self.comments = comments



    def get_collection(self):
        return self.collection_name

    #def edit_card(self):




# will change to be handled by microservice later
class Collection:
    '''
    Makes a collection object with a name and list of card objects
    '''

    # have card_list parameter for now
    def __init__(self, collection_name, card_list=[]):
        self._name = collection_name
        self._cards = card_list

    def get_name(self):
        return self._name

    def add_card(self, card):
        '''
        Adds a card to the collection
        :param card:
        :return:
        '''
        self._cards.append(card)

    def get_cards(self):
        '''
        Returns the list of card objects
        :return:
        '''
        return self._cards


#-----------------------------------------





# data for sprint1
# card_1 = {'name': 'Umbreon VMAX',
#           'collection': 'My Collection',
#           'set': 'Evolving Skies',
#           'type': 'dark',
#           'rarity': 'Ultra Rare',
#           'market price': '$1640',
#           'path to image': 'URL',
#           'additional comments': 'Love this card!'
#           }

card_1 = Card("Umbreon VMAX", 'My Collection', 'Evolving Skies', 'dark',
              'Ultra Rare', '$1640',
              '/users/ryan/documents/Pokemon_Tracker/Umbreon_vmax.jpg',
              'Love this Card')

# my_collection = {'name': 'My Collection', 'cards': [card_1]}
# my_watchlist = {'name': 'My WatchList'}
# the_rarest_cards = {'name': 'The Rarest Cards'}
# little_brothers_cards = {'name': "Little Brother's Cards"}
my_collection = Collection('My Collection', [card_1])
my_watchlist = Collection('My WatchList')
the_rarest_cards = Collection('The Rarest Cards')
little_brothers_cards = Collection("Little Brother's Cards")



collections = [my_collection, my_watchlist, the_rarest_cards, little_brothers_cards]

# Welcome page
print("Welcome to the pokemon card collection app! \nHere you can keep track and organize all the "
        "cards you've collected.\n\n")
username = input("Please enter your username or 'Q' to quit: ")
if username == 'Q' or username == 'q':
    print("See you next time!")

# enter the Home Page
else:
    my_tracker = PokemonTracker(username, collections)
    my_tracker.homepage()


