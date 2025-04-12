import sqlite3
import pandas as pd

def create_connection(db_path):
    return sqlite3.connect(db_path)

def initialize_database(connection):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS speedruns (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    GameID TEXT NOT NULL,
                    GameName TEXT NOT NULL,
                    CategoryID TEXT NOT NULL,
                    CategoryName TEXT NOT NULL,
                    CategoryVariables TEXT,
                    RunID TEXT NOT NULL,
                    PlayerIDs TEXT,
                    RunDateSubmitted TEXT,
                    RunDateVerified TEXT,
                    RunTime FLOAT NOT NULL,
                    GameRegion TEXT,
                    GamePlatform TEXT,
                    isEmulated BOOLEAN,
                    PlayerCountry TEXT,
                    PlayerAccountSignupDate TEXT,
                    PlayerPronouns TEXT
                )
            ''')

def insert_speedruns(connection, game_id, game_name, category_id, category_name, category_var, run_id, player_ids, run_date_submitted, run_date_verified, run_time, game_region, game_platform, is_emulated, player_country, player_account_signup_date, player_pronouns):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO speedruns(GameID, GameName, CategoryID, CategoryName, CategoryVariables, RunID, PlayerIDs, RunDateSubmitted, RunDateVerified, RunTime, GameRegion, GamePlatform, isEmulated, PlayerCountry, PlayerAccountSignupDate, PlayerPronouns) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (game_id, game_name, category_id, category_name, category_var, run_id, player_ids, run_date_submitted, run_date_verified, run_time, game_region, game_platform, is_emulated, player_country, player_account_signup_date, player_pronouns))
    connection.commit()
    return cursor.lastrowid