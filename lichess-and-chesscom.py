import shutil
import requests
from codecs import open
from datetime import date
import os.path
from os import environ

lichess_api_key = environ['lichess_api_key']


def main(user, luser, file, lichess_api_key, ccom, lorg):
    try:
        os.remove(file)
    except OSError:
        pass
    if ccom == 1:
        for archive in requests.get('https://api.chess.com/pub/player/%s/games/archives' % user).json()['archives']:
            download_archive(archive, file)
    else:
        print("Skipping chess.com")
    if lorg == 1:
        print("about to make lichess request")
        if lichess_api_key is not None:
            print(lichess_api_key)
            r = requests.get('https://lichess.org/api/games/user/%s' % luser,
                             headers={'Authorization': 'Bearer ' + lichess_api_key[0]}, stream=True)
        elif lichess_api_key is None:
            print(lichess_api_key)
            r = requests.get('https://lichess.org/api/games/user/%s' %
                             luser, stream=True)
        print(r.text)
        with open(file, 'a', encoding='utf-8') as output:
            print(r.text, file=output)
            print('', file=output)

    else:
        print("Skipping lichess.org")


def download_archive(url, file):
    games = get(url)['games']
    print('Starting work on %s...' % file)
    # XXX: If a file with this name already exists, we'll blow away the old
    # one. Possibly not ideal.
    with open(file, 'a', encoding='utf-8') as output:
        for game in games:
            print(game['pgn'], file=output)
            print('', file=output)


def get(url, headers=None):
    return requests.get(url, headers=headers).json()


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(
        description="Download a user's games from chess.com")
    parser.add_argument('user', metavar='USER',
                        help='The user whose games we want', default=None, nargs='?')
    parser.add_argument('luser', metavar='LUSER',
                        help='The user whose games we want', default=None, nargs='?')
    parser.add_argument('file', metavar='PATH', help='which file (can include directory) to create the PGN files',
                        default="./chessGames.pgn", nargs='?')
    parser.add_argument('--lichess_api_key', metavar='API_KEY',
                        help='the api key for lichess', default=None, nargs=1)
    try:
        args = parser.parse_args()
        print("No errors passing arguments")
        if args.user != None and args.user != "":
            ccom = 1
        else:
            ccom = 0
        if args.luser != None:
            lorg = 1
        else:
            lorg = 0
    except:
        print("idk, some error")
    print(args.user, args.luser, args.file, args.lichess_api_key, ccom, lorg)
    main(args.user, args.luser, args.file, args.lichess_api_key, ccom, lorg)
