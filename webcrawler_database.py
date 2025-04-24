import sqlite3
import pandas as pd

# from webcrawler import connection

def create_connection(db_path):
    return sqlite3.connect(db_path)

def initialize_database(connection):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS speedruns (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    GameID TEXT NOT NULL,
                    GameName TEXT NOT NULL,
                    CategoryID TEXT NOT NULL,
                    FullGameCategory TEXT NOT NULL,
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

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    PlayerID TEXT NOT NULL,
                    GameID TEXT NOT NULL,
                    GameName TEXT NOT NULL,
                    GameGenre TEXT,
                    RunID TEXT NOT NULL,
                    RunTime FLOAT NOT NULL,
                    PlayerCountry TEXT,
                    PlayerPronouns TEXT,
                    PlayerSignupDate TEXT
                    )
    ''')

    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users_final (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        PlayerID TEXT NOT NULL,
                        GameID TEXT NOT NULL,
                        GameName TEXT NOT NULL,
                        GameGenre TEXT,
                        RunID TEXT NOT NULL,
                        RunTime FLOAT NOT NULL,
                        CategoryType TEXT NOT NULL,
                        PlayerCountry TEXT,
                        PlayerPronouns TEXT,
                        PlayerSignupDate TEXT
                        )
        ''')

def insert_speedruns(connection, player_id, game_id, game_name, category_id, full_game_category, category_name, category_var, run_id, player_ids, run_date_submitted, run_date_verified, run_time, game_region, game_platform, is_emulated, player_country, player_account_signup_date, player_pronouns):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO speedruns(PlayerID, GameID, GameName, CategoryID, FullGameCategory, CategoryName, CategoryVariables, RunID, PlayerIDs, RunDateSubmitted, RunDateVerified, RunTime, GameRegion, GamePlatform, isEmulated, PlayerCountry, PlayerAccountSignupDate, PlayerPronouns) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (player_id, game_id, game_name, category_id, full_game_category, category_name, category_var, run_id, player_ids, run_date_submitted, run_date_verified, run_time, game_region, game_platform, is_emulated, player_country, player_account_signup_date, player_pronouns))
    connection.commit()
    return cursor.lastrowid

def insert_users(connection, player_id, game_id, game_name, game_genre, run_id, run_time, player_country, player_pronouns, player_signup_date):
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO users(PlayerID, GameID, GameName, GameGenre, RunID, RunTime, PlayerCountry, PlayerPronouns, PlayerSignupDate) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (player_id, game_id, game_name, game_genre, run_id, run_time, player_country, player_pronouns, player_signup_date))
    connection.commit()
    return cursor.lastrowid

def insert_users_final(connection, player_id, game_id, game_name, game_genre, run_id, run_time, category_type, player_country, player_pronouns, player_signup_date):
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO users_final(PlayerID, GameID, GameName, GameGenre, RunID, RunTime, CategoryType, PlayerCountry, PlayerPronouns, PlayerSignupDate) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (player_id, game_id, game_name, game_genre, run_id, run_time, category_type, player_country, player_pronouns, player_signup_date))
    connection.commit()
    return cursor.lastrowid

def insert_category_type(connection, player_id, run_id, category_type):
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO category_type(PlayerID, RunID, CategoryType) '
        'VALUES (?, ?, ?)',
        (player_id, run_id, category_type)
    )
    connection.commit()
    return cursor.lastrowid