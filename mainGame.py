import datetime
import json
import os
import time

_fieldGame = lambda: {'name', 'release', 'status', 'completed', 'rating', 'genres', 'comment', 'platform'}


class Game:
    _status = ('Plan to game', 'Dropped', 'On Hold', 'Completed', 'Currently gaming')

    def __init__(self, name='NoNe', release=datetime.date(1, 1, 1), status=_status[0],
                 date_of_completion=datetime.date(1, 1, 1),
                 rating=0, genres='', comment='', platform=''):
        self.name = name
        self.release = release
        self.status = status
        self.completed = date_of_completion
        self.genres = genres
        self.comment = comment
        self.rating = rating
        self.platform = platform

    def __str__(self):
        return (f'{self.name}, {self.genres}, {self.release}, '
                f'{self.status}, {self.completed}, {self.comment}, {self.rating}')



def test_game_Celeste():
    """Create test object game Celeste"""

    name = 'Celeste'
    release = datetime.date(2018, 2, 2)
    status = 'Completed'
    completed = datetime.date(2020, 1, 13)
    genres = 'platformer'
    rating = 8
    comment = 'Прекрасный платформер, о восхождении на гору. 1,5К смертей!'
    platform = 'switch'
    myGame = Game(name, release, status, completed, rating, genres, comment, platform)
    return myGame


def mistake_enter(s='Sorry you mistake. Repeat enter (Y/N)'):
    """
    Quick input check

    check input y or n on keyboard,
    and return bool
    """
    print(s)
    s = input()
    while True:
        if s.upper() == 'Y':
            return True
        elif s.upper() == 'N':
            return False
        s = input('Sorry you mistake. you must enter Y(y) or N(n) \n')


def create_new_game_manual():
    """Create new game in manual

    create new object game in consol
    """

    print('Input data of game')

    # Input name
    name = input('Name the game \n')
    if name == '':
        print('''You don't enter name. The name Temp will be used''')
        name = 'Temp'

    # Input date release
    while True:
        try:
            release = datetime.datetime.strptime(input('Input date release game in format YYYY-MM-DD \n'),
                                                 '%Y-%m-%d').date()
        except ValueError:
            if not mistake_enter():
                release = datetime.date(2010, 1, 1)
                print(f'Release was used {release}')
                break
        else:
            break

    # Input status
    status_dict = {'Plan to game': False, 'Dropped': True, 'On Hold': False, 'Completed': True, 'Now playing': False}
    print(f'Select status the game (first letter or full word): {", ".join(status_dict.keys())} ')
    status = input()
    check = False
    for i in status_dict.keys():
        if i.upper() == status.upper():
            check = True
            break
        elif i[0].upper() == status.upper() and len(status) == 1:
            check = True
            status = i
            break
    if not check:
        print('Status set "Plan to game"')

    # Input date complete
    while True:
        try:
            completed = datetime.datetime.strptime(input('Input date completed game in format YYYY-MM-DD \n'),
                                                   '%Y-%m-%d').date()
        except ValueError:
            if not mistake_enter('Sorry, you made a mistake in typing, repeat?(Y/N)'):
                completed = datetime.date(1, 1, 1)
                break
        else:
            break

    del status_dict

    # input gener
    genres = input('Gener \n')

    # input rating
    while True:
        try:
            rating = int(input('rating from 0/10 \n'))
        except ValueError:
            if not mistake_enter():
                rating = 0
                break
        else:
            if 0 <= rating <= 10:
                break
            elif not mistake_enter():
                rating = 0
                break

    # input comment
    comment = input('Your comment about game \n')

    # input platform
    platform_tuple = ('PC', 'Switch', 'PS4', 'XBOX')
    check = False
    while True:
        platform = input(f'Choose platform:{", ".join(platform_tuple)} \n')
        for i in platform_tuple:
            if platform.upper() == i.upper():
                check = True
                break
        if check:
            break
        elif not mistake_enter('You have not selected a platform, or selected the wrong platform. Repeat enter?(Y/N)'):
            break

    newGame = Game(name, release, status, completed, rating, genres, comment, platform)
    return newGame


def add_game_to_dict(newGame: Game, gameDict: dict()):
    """Add game to Dict"""
    if newGame.name in gameDict.keys():
        print(f'Game {newGame.name} was added earlier, change it?(y/n)')
        confirm = input().upper()
        while True:
            if confirm == 'Y':
                gameDict[newGame.name] = newGame
                print(f'Game {newGame.name} changed!')
                return gameDict
            elif confirm == 'N':
                print('The object has not been modified')
                return gameDict
        confirm = input('Sorry, enter y or n').upper()
    gameDict[newGame.name] = newGame
    print(f'New game {newGame.name} was added from list')
    return gameDict


def change_game(nameOfGame: str, gameDict: dict()):
    if (nameOfGame not in gameDict.keys()):
        return print(f'Sorry {nameOfGame} not found in list')
    changeGame = Game()
    changeGame = gameDict[nameOfGame]
    print('What you want change? \n' + ', '.join(_fieldGame()))
    changeField = {i for i in input().split(' ')}.intersection(_fieldGame())
    print(f'Field {", ".join(changeField)} will modifited')
    for field in changeField:
        print(field)
        changeGame.__setattr__(field, 'yes')
        print(changeGame)
    return

def add_gamedict_to_file(myGameList: dict, fileName='myGameList.json'):
    """Add dict to file .json

    convert datetime and object Game
    from write to file
    """
    jsonGameList = []
    gameField = {'name', 'release', 'status', 'completed', 'rating', 'genres', 'comment', 'platform'}
    for val in myGameList.values():
        print(val)
        jsonGameList.append({key: val.__getattribute__(key) for key in gameField})
    for elem in jsonGameList:
        elem['release'] = datetime.date.strftime(elem['release'], '%Y-%m-%d')
        elem['completed'] = datetime.date.strftime(elem['completed'], '%Y-%m-%d')
    with open(fileName, 'w') as writeFile:
        json.dump(jsonGameList, writeFile)
    return


def create_dict_from_file(fileName='myGameList.json'):
    """Create dict from .json file

    :param fileName:
    :return:
    """
    _myGameDict = {}
    with open(fileName) as file:
        _myGameList = json.load(file)
    for i in _myGameList:
        _myGameDict[i['name']] = Game(i['name'], datetime.datetime.strptime(i['release'], '%Y-%m-%d').date(),
                                           i['status'], datetime.datetime.strptime(i['completed'], '%Y-%m-%d').date(),
                                           i['rating'], i['genres'], i['comment'], i['platform'])
    return _myGameDict


def menu():
    print(
        """menu:
1: Print your game list
2: Add new game
3: Change game
0: Exit"""
    )


def action(myGameDict: dict):
    menu()
    while True:
        ac = input()
        if ac == '1':
            for i in sorted(myGameDict.keys()):
                print(myGameDict[i])
            return action(myGameDict)
        elif ac == '2':
            newGame = create_new_game_manual()
            myGameDict = add_game_to_dict(newGame, myGameDict)
            return action(myGameDict)
        elif ac == '3':
            print("Select game from changed:\n" + '\n'.join(sorted(myGameDict.keys())))
            change_game(input(), myGameDict)
            return action(myGameDict)
        elif ac == '0':
            print('Goodbye, game in your list:')
            return add_gamedict_to_file(myGameDict)
        else:
            if mistake_enter('Oooooppppsss... change again? (Y/N)'):
                menu()
            else:
                print('Goodbye, game in your list:')
                return add_gamedict_to_file(myGameDict)
    return add_gamedict_to_file(myGameDict)


myGameDict = create_dict_from_file()
action(myGameDict)
