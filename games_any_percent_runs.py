import time

import requests
import json
from webcrawler_database import create_connection, initialize_database, insert_users, insert_speedruns

def get_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def get_games_any_percent_runs(game_id_txt):
    # filter to only get games that have an any% full game run without any variables
    games_any_percent_runs = []
    with (open(game_id_txt, 'r') as file):
        for line in file:
            game = line.strip()
            title = game.split('-')[0].strip().replace(' ', '%20')
            game_url = get_api_data(f"https://www.speedrun.com/api/v1/games?name={title}&embed=categories")

            if not game_url or not game_url.get('data'):
                continue

            game_id = game_url['data'][0]['id']
            print(f"Processing game: {game_id}")
            game_categories = game_url['data'][0]['categories']

            try:
                for category in game_categories['data']:
                    if category['name'] == 'Any%':
                        # add to array
                        games_any_percent_runs.append(game_id)
                        with open('speedrun_data/games_with_any_percent.txt', 'a', encoding='utf-8') as f:
                            f.write(f"{game_id} - {category['id']}\n")
            except(KeyError, IndexError, TypeError):
                print("does not have categories")


# get all of the players from the leaderboard of celeste
# then run get_users_games to get all of the other games that they run and the times for it??
# mark down whether it was a per-game run or per-level = per game means it's a full game run

def celeste_game_runners():
    celeste_leaderboard = get_api_data(f"https://www.speedrun.com/api/v1/leaderboards/o1y9j9v6/category/7kjpl1gk")
    for each_run in celeste_leaderboard['data']['runs']:
        placement = each_run['place']

        run = each_run['run']
        player_id = run['players'][0]['id']

        # get the player info
        player_url = get_api_data(f"https://www.speedrun.com/api/v1/users/{player_id}")
        try:
            player_pronouns = player_url['data']['pronouns']
        except (KeyError, IndexError, TypeError):
            player_pronouns = None

        try:
            player_signup = player_url['data']['signup']
        except (KeyError, IndexError, TypeError):
            player_signup = None

        try:
            player_location = player_url['data']['location']['country']['names']['international']
        except(KeyError, IndexError, TypeError):
            player_location = None


def get_users_games(player_ids_txt, connection):
    with open(player_ids_txt, 'r') as file:
        for line in file:
            print(line+'\n')
            player_url = get_api_data(f"https://www.speedrun.com/api/v1/users/{line}")

            try:
                player_pronouns = player_url['data']['pronouns']
            except (KeyError, IndexError, TypeError):
                player_pronouns = None

            try:
                player_signup = player_url['data']['signup']
            except (KeyError, IndexError, TypeError):
                player_signup = None

            try:
                player_location = player_url['data']['location']['country']['names']['international']
            except(KeyError, IndexError, TypeError):
                player_location = None

            player_pb_url = get_api_data(f"https://www.speedrun.com/api/v1/users/{line}/personal-bests?embed=game.genres,category")

            if player_pb_url == None:
                print("ERROR: " + line)
                continue

            for entry in player_pb_url['data']:
                print(entry)
                game_id = entry['game']['data']['id']
                try:
                    game_name = entry['game']['data']['names']['international']
                except (KeyError, IndexError, TypeError):
                    game_name = None
                try:
                    game_genre = entry['game']['data']['genres']['data'][0]['name']
                except (KeyError, IndexError, TypeError):
                    game_genre = None
                run_id = entry['run']['id']
                run_time = entry['run']['times']['primary_t']
                isFull = entry['category']['data']['type']

                insert_users(connection, line, game_id, game_name, game_genre, run_id, run_time, player_location, player_pronouns, player_signup)
                connection.commit()

# def get_games_leaderboard():
    # for each game, go into the leaderboard for the any% category

#
# connection = create_connection('new_database.sqlite')
# initialize_database(connection)
#
# #get_all_users_from_game('speedrun_data/games.txt')
#
# get_users_games('player_ids.txt', connection)
#
# connection.close()

get_games_any_percent_runs('speedrun_data/games.txt')

# connection = create_connection('database.sqlite')
# initialize_database(connection)
#
#
# connection.commit()
# connection.close()
#
# test_run = get_api_data(f"https://www.speedrun.com/api/v1/leaderboards/xldev513/category/rklg3rdn?embed=players")
# with open('data_new_3.json', 'w', encoding='utf-8') as f:
#     json.dump(test_run, f, ensure_ascii=False, indent=4)
