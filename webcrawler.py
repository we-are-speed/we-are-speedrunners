import requests
import json
from webcrawler_database import create_connection, initialize_database, insert_speedruns

def get_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

connection = create_connection('database.sqlite')
initialize_database(connection)

### Get top 100 games with most runs
with open('speedrun_data/test_games.txt', 'r') as file:
    for line in file:
        game = line.strip()
        title = game.split('-')[0].strip().replace(' ','%20')
        game_url = get_api_data(f"https://www.speedrun.com/api/v1/games?name={title}")
        game_id = game_url['data'][0]['id']

        # have to cycle through each page too
        # vvv this will only get the first 200 runs, so have to put in for loop
        # and check. pagination
        game_data = get_api_data(
            f"https://www.speedrun.com/api/v1/runs?max=200&game={game_id}&status=verified&embed=game,platform,category.variables,levels.variables,players,region")

        for run in game_data['data']:
            run_id = run['id']
            game_name = run['game']['data']['names']['international']
            category_id = run['category']['data']['id']
            category_name = run['category']['data']['name']
            player_ids = json.dumps([
                player['id']  # Using direct access since IDs should be mandatory
                for player in run.get('players', {}).get('data', [])
                if isinstance(player, dict) and 'id' in player
            ])
            run_date_submitted = run['submitted'] # have to clean this to get rid of time stamp at end
            run_date_verified = run['status']['verify-date']
            run_category = run['category']['data']['id']

            run_time = run['times']['primary_t'] # in seconds
            game_region = run['region']['data'][0]['name'] if run['region']['data'] else None
            game_platform = run['platform']['data']['name']
            is_emulated = run['system']['emulated']

            category_variables = json.dumps([
                var.get('name', None)
                for var in run.get('category', {}).get('data', {}).get('variables', {}).get('data', [])
                if isinstance(var, dict)
            ])

            player_country = json.dumps([
                player.get('location', {}).get('country', {}).get('names', {}).get('international', 'Unknown')
                for player in run.get('players', {}).get('data', [])
                if isinstance(player, dict)
            ])
            player_account_signup_date = json.dumps([
                player.get('signup')  # Removed explicit None default since .get() returns None by default
                for player in run.get('players', {}).get('data', [])
                if isinstance(player, dict)
            ])
            player_pronouns = json.dumps([
                player.get('pronouns')
                for player in run.get('players', {}).get('data', [])
                if isinstance(player, dict)
            ])

            # TODO: add list for variables for category
            # TODO: for loop for going through all pages of a game + cycle through all of the levels

            insert_speedruns(connection,
                        game_id,
                        game_name,
                        category_id,
                        category_name,
                        category_variables,
                        run_id,
                        player_ids,
                        run_date_submitted,
                        run_date_verified,
                        run_time,
                        game_region,
                        game_platform,
                        is_emulated,
                        player_country,
                        player_account_signup_date,
                        player_pronouns)

connection.commit()
connection.close()


# with open('most_runs_games2.json', 'w', encoding='utf-8') as f:
#      json.dump(test_run, f, ensure_ascii=False, indent=4)

#
# api_url = "https://www.speedrun.com/api/v1/games?name=ultrakill"
# response = get_api_data(api_url)
# game_id = response['data'][0]['id']
#
# test_run = get_api_data(f"https://www.speedrun.com/api/v1/runs?max=2&level=29vl6lqw&game={game_id}&status=verified&embed=game,platform,category.variables,levels.variables,players,region")
# with open('data_new_2.json', 'w', encoding='utf-8') as f:
#      json.dump(test_run, f, ensure_ascii=False, indent=4)
#
# connection = create_connection('database.sqlite')
# initialize_database(connection)
#
# for run in test_run['data']:
#     run_id = run['id']
#     game_name = run['game']['data']['names']['international']
#     category_id = run['category']['data']['id']
#     category_name = run['category']['data']['name']
#     player_ids = json.dumps([
#         player['id']  # Using direct access since IDs should be mandatory
#         for player in run.get('players', {}).get('data', [])
#         if isinstance(player, dict) and 'id' in player
#     ])
#     run_date_submitted = run['submitted'] # have to clean this to get rid of time stamp at end
#     run_date_verified = run['status']['verify-date']
#     run_category = run['category']['data']['id']
#
#     run_time = run['times']['primary_t'] # in seconds
#     game_region = run['region']['data'][0]['name'] if run['region']['data'] else None
#     game_platform = run['platform']['data']['name']
#     is_emulated = run['system']['emulated']
#
#     category_variables = json.dumps([
#         var.get('name', None)
#         for var in run.get('category', {}).get('data', {}).get('variables', {}).get('data', [])
#         if isinstance(var, dict)
#     ])
#     #level_variables =
#     #game_levels = run['levels']['data']
#
#     player_country = json.dumps([
#         player.get('location', {}).get('country', {}).get('names', {}).get('international', 'Unknown')
#         for player in run.get('players', {}).get('data', [])
#         if isinstance(player, dict)
#     ])
#     player_account_signup_date = json.dumps([
#         player.get('signup')  # Removed explicit None default since .get() returns None by default
#         for player in run.get('players', {}).get('data', [])
#         if isinstance(player, dict)
#     ])
#     player_pronouns = json.dumps([
#         player.get('pronouns')
#         for player in run.get('players', {}).get('data', [])
#         if isinstance(player, dict)
#     ])
#
#     # TODO: add list for variables for category
#     # TODO: for loop for going through all pages of a game + cycle through all of the levels
#
#     insert_speedruns(connection,
#                 game_id,
#                 game_name,
#                 category_id,
#                 category_name,
#                 category_variables,
#                 run_id,
#                 player_ids,
#                 run_date_submitted,
#                 run_date_verified,
#                 run_time,
#                 game_region,
#                 game_platform,
#                 is_emulated,
#                 player_country,
#                 player_account_signup_date,
#                 player_pronouns)
#
# connection.commit()
# connection.close()