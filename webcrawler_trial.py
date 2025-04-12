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
#
# # vvv this gets the id of a game after searching it up
# api_url = "https://www.speedrun.com/api/v1/games?name=Breath%20of%20the%20wild"
# response = get_api_data(api_url)
# game_id = response['data'][0]['id']
#
# # vvv this gets the categories of a game
# categories_url =  f"https://www.speedrun.com/api/v1/games/{game_id}/categories"
# categories_response = get_api_data(categories_url)
# #for key in categories_response['data']:
# #    print(key['id']) # get all of the ids of each category
#
# # vvv this lets you embed the categories so you don't have to do the two above ^^^ in two different requests
# categories_url =  f"https://www.speedrun.com/api/v1/games/{game_id}?embed=categories"
# second_response = get_api_data(categories_url)
# #print(second_response)
#
# # vvv this gets all of the runs of a game and lets you embed the category that it was run in
# print(f"https://www.speedrun.com/api/v1/runs?game={game_id}?embed=category")
# third_response = get_api_data(f"https://www.speedrun.com/api/v1/runs?game={game_id}?embed=category")
# print(third_response)
#
# # vvv this gets 200 runs at once.
# # if cycling through, check if size < max = that means you are on the last page and got all the runs
# fourth_response = get_api_data(f"https://www.speedrun.com/api/v1/runs?max=200?game={game_id}?embed=category")
# print(fourth_response)
#
# # embed variables to get the mini variables in each category too
# # ?embed=categories.variables,regions
#
# # create a database
#
# ## Testing with Cannon Fodder (3DO)

#api_url = "https://www.speedrun.com/api/v1/games?name=Breath%20of%20the%20wild"
#api_url = "https://www.speedrun.com/api/v1/games?name=Cannon%20Fodder%20(3DO)"
#api_url = "https://www.speedrun.com/api/v1/games?name=super%20mario%2064"
api_url = "https://www.speedrun.com/api/v1/games?name=ultrakill"
response = get_api_data(api_url)
game_id = response['data'][0]['id']
# if we get the game ids by going like top 100 games, can skip this above step ^^^

# categories_url =  f"https://www.speedrun.com/api/v1/games/{game_id}/categories"
# categories_response = get_api_data(categories_url) # gets All Missions, Disc 2, Disc 3
# for key in categories_response['data']:
#    print(key['id']) # get all of the ids of each category

# # vvv get all of the runs of a game
# third_response = get_api_data(f"https://www.speedrun.com/api/v1/runs?game={game_id}")
# print(third_response)
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(third_response, f, ensure_ascii=False, indent=4)
#
# fourth_response = get_api_data(f"https://www.speedrun.com/api/v1/runs?game={game_id}&embed=category")
# print(fourth_response)
# with open('data2.json', 'w', encoding='utf-8') as f:
#     json.dump(fourth_response, f, ensure_ascii=False, indent=4)

# fifth_response = get_api_data(f"https://www.speedrun.com/api/v1/runs?game={game_id}&embed=category.variables,levels.variables,players,region")
# print(fifth_response)
# with open('data3.json', 'w', encoding='utf-8') as f:
#     json.dump(fifth_response, f, ensure_ascii=False, indent=4)

# will only get verified runs vvv
#test_run = get_api_data(f"https://www.speedrun.com/api/v1/runs?max=2&game={game_id}&status=verified&embed=game,platform,category.variables,levels.variables,players,region")
test_run = get_api_data(f"https://www.speedrun.com/api/v1/runs?max=2&level=29vl6lqw&game={game_id}&status=verified&embed=game,platform,category.variables,levels.variables,players,region")
with open('data_new_2.json', 'w', encoding='utf-8') as f:
     json.dump(test_run, f, ensure_ascii=False, indent=4)

connection = create_connection('database.sqlite')
initialize_database(connection)

#insert_runs(connection, game_id, category_id, run_id, player_id, place_on_leaderboard, run_date_submitted, run_date_verified, run_category, run_time, game_region, game_platform, players_country, players_account_signup_date, players_pronouns)
for run in test_run['data']:
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
    #level_variables =
    #game_levels = run['levels']['data']

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

    # print(run_id)
    # print(category_id)
    # print(category_name)
    # print(player_ids)
    # print(run_date_submitted)
    # print(run_date_verified)
    # print(run_category)
    # print(run_time)
    # print(game_region)
    # print(game_platform)
    # print(player_country)
    # print(player_pronouns)
    # print(player_account_signup_date)

#
# with open('data1.json', 'w', encoding='utf-8') as f:
#     json.dump(sixth_response, f, ensure_ascii=False, indent=4)

connection.commit()
connection.close()
# fourth_response = get_api_data(f"https://www.speedrun.com/api/v1/runs?max=200?game={game_id}?embed=category.variables,regions")
# print(fourth_response)

# primary = time in seconds


### Leaderboards
# # unsure if we should do that because this is just purely to get the placement
# # and we'd have to make a new api request for each separate leaderboard
# categories_url =  f"https://www.speedrun.com/api/v1/games/{game_id}/categories"
# categories_response = get_api_data(categories_url) # gets All Missions, Disc 2, Disc 3
# for key in categories_response['data']:
#     print(key['id'])
#     leaderboard_url = f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{key['id']}?embed=players"
#     with open(f'{key["id"]}_data_leaderboards.json', 'w', encoding='utf-8') as f:
#         json.dump(get_api_data(leaderboard_url), f, ensure_ascii=False, indent=4)