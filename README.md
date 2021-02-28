
# get-em

## THIS IS STILL A WORK-IN-PROGRESS
  

Pulls games from [chess.com](chess.com) and [lichess.org](lichess.org) given usernames and a lichess api token to a pgn file using respective API's

  

## Usage

```

python get-em.py [--lichess_api_key API_KEY] [CHESS.COM_USERNAME] [LICHESS_USERNAME] [PATH_TO_SAVE]

```

For help type `python get-em.py -h`

  

## Example 

`python get-em.py xyz` saves all of "xyz"'s chess.com games to a file

`python get-em.py xyz xyzed`saves all of "xyz"'s chess.com games and "xyzed"'s games from lichess.org to a file

`python get-em.py "" xyzed` saves all of "xyzed"'s lichess.org games to a file

*lichess_api_key* should be provided, either with the program execution as an argument or as an env variable

Get it from [here](https://lichess.org/account/oauth/token)