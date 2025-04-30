# ICS 635 - Team we-are-speedrunners

## Acquire dataset
First run `get_games_with_most_runs.py` to get the first 6 pages of speedrun.com. This will get the games with the most runs on the site. 

Then run `users_pb.py`. This will go through each game, getting all users who are on the leaderboard for the game and then getting all of the other games they played. In our project, we were only able to do the first 6 games before cutting it off. 

After running `users_pb.py`, the table `users_final` in database `new_database.sqlite` will have all of the collected data.

## Dataset 
All 3 team members ran the users_pb.py script in parallel and the resulting csv files can be found in the dataset folder. 

## Trial Models
The TrialModels folder contains the team's iterations over different models that ended up being outperformed by the Final Model. 

## Final Model
The final model was selected from all the models the team trained because it demonstrated strong generalization performance and was robust enough to handle the combined data from the three CSV files.
