import time

import requests
import json
from webcrawler_database import create_connection, initialize_database, insert_users, insert_category_type, insert_users_final, insert_celeste

def get_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        with open('errors_celeste.txt', 'a', encoding='utf-8') as f:
            f.write(f"Error making request: {e}\n")
        return None

def get_all_users_from_game(game_id_txt, game_output_txt):
    all_player_ids = set()  # Using set to avoid duplicates

    with open(game_id_txt, 'r') as file:
        for line in file:
            game = line.strip()
            title = game.split('-')[0].strip().replace(' ', '%20')
            game_url = get_api_data(f"https://www.speedrun.com/api/v1/games?name={title}&embed=categories")

            if not game_url or not game_url.get('data'):
                continue

            game_id = game_url['data'][0]['id']
            print(f"Processing game: {game_id}")

            if isinstance(game_url, dict):
                data = game_url.get('data')
                data_list = data if isinstance(data, list) else [data]

                for item in data_list:
                    if isinstance(item, dict) and 'categories' in item:
                        categories = item['categories']
                        if isinstance(categories, dict) and 'data' in categories:
                            for category in categories['data']:
                                if isinstance(category, dict) and 'id' in category and category.get(
                                        'type') == 'per-game':
                                    print(f"Processing category: {category['id']}")

                                    # Get only first page of leaderboard
                                    api_url = f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{category['id']}?embed=players"
                                    game_data = get_api_data(api_url)

                                    if game_data and isinstance(game_data, dict):
                                        players = game_data.get('data', {}).get('players', {}).get('data', [])
                                        for player in players:
                                            if isinstance(player, dict) and 'id' in player:
                                                all_player_ids.add(player['id'])

    # Write all unique player IDs to file once
    with open(game_output_txt, 'w', encoding='utf-8') as f:
        for player_id in all_player_ids:
            f.write(f"{player_id}\n")

    print(f"Found {len(all_player_ids)} unique player IDs (first page only)")

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
                time.sleep(60)
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
                category_type = entry['category']['data']['type']
                category = entry['category']['data']['name']

                #insert_users(connection, line, game_id, game_name, game_genre, run_id, run_time, player_location, player_pronouns, player_signup)
                insert_users_final(connection, line, game_id, game_name, game_genre, run_id, run_time, category_type, player_location, player_pronouns, player_signup)
                #insert_celeste(connection, line, game_id, game_name, game_genre, run_id, run_time, category, category_type, player_location, player_pronouns, player_signup)
                connection.commit()

connection = create_connection('new_database.sqlite')
initialize_database(connection)

get_all_users_from_game('speedrun_data/games.txt', 'speedrun_data/games_output.txt')
get_users_games('speedrun_data/games_output.txt', connection)

#get_all_users_from_game('speedrun_data/celeste.txt','celeste_players.txt')

#get_users_games('celeste_players.txt', connection)

#insert_extra_categories(connection)

connection.close()

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
