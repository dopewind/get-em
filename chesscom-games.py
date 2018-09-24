from codecs import open
from datetime import date
import os.path
import requests
import shutil

def main(user, file, lichess_api_key):
    print("Downloading %s's games to %s:" % (user, file))
    try:
        os.remove(file)
    except OSError:
        pass
    for archive in requests.get('https://api.chess.com/pub/player/%s/games/archives' % user).json()['archives']:
        download_archive(archive, file)
    print("about to make lichess request")
    if lichess_api_key is not None:
        print(lichess_api_key)
        r = requests.get('https://lichess.org/api/games/user/%s' % user, headers={'Authorization': 'Bearer ' + lichess_api_key[0]}, stream=True)
    elif lichess_api_key is None:
        print(lichess_api_key)
        r = requests.get('https://lichess.org/api/games/user/%s' % user, stream=True)
    print(r.text)
    with open(file, 'a', encoding = 'utf-8') as output:
        print(r.text, file=output)
        print('', file=output)

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
    return requests.get(url, headers = headers).json()



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Download a user's games from chess.com")
    parser.add_argument('user', metavar='USER', help='The user whose games we want')
    parser.add_argument('file', metavar='PATH', help='which file (can include directory) to create the PGN files', default="./chessGames.pgn", nargs='?')
    parser.add_argument('--lichess_api_key', metavar='API_KEY', help =  'the api key for lichess', default=None, nargs = 1)
    args = parser.parse_args()
    main(args.user, args.file, args.lichess_api_key)
