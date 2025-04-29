# we-are-speedrunners

First run get_games_with_most_runs.py to get the first 6 pages of speedrun.com. This will get the games with the most runs on the site. 

Then run users_pb.py. This will go through each game, getting all users who are on the leaderboard for the game and then getting all of the other games they played. In our project, we were only able to do the first 6 games before cutting it off. 

After running users_pb.py, the database `new_database.sqlite` will have all of the collected data.
