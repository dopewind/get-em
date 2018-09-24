from codecs import open
from datetime import date
import os.path
import requests

def main(user, file):
    print("Downloading %s's games to %s:" % (user, file))
    try:
        os.remove(file)
    except OSError:
        pass
    for archive in get('https://api.chess.com/pub/player/%s/games/archives' % user)['archives']:
        download_archive(archive, file)

def download_archive(url, file):
    games = get(url)['games']
    print('Starting work on %s...' % file)
    # XXX: If a file with this name already exists, we'll blow away the old
    # one. Possibly not ideal.
    with open(file, 'a', encoding='utf-8') as output:
        for game in games:
            print(game['pgn'], file=output)
            print('', file=output)

def get(url):
    return requests.get(url).json()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Download a user's games from chess.com")
    parser.add_argument('user', metavar='USER', help='The user whose games we want')
    parser.add_argument('file', metavar='PATH', help='which file (can include directory) to create the PGN files',
            default="./chessGames.pgn", nargs='?')
    args = parser.parse_args()
    main(args.user, args.file)
