# This python script loads the json file to the database
# The tables are created with the 'createTables.sql' script

import json
import psycopg2
import sys
import uuid
import os

root_database_name = "project_database"
query_database_name = "query_database"
db_username = 'postgres'
db_password = '1234'
db_host = 'localhost'
db_port = '5432'

validPermier = "Premier League"
validPermierSeason = "2003/2004"

validCompetitionName = "La Liga"
validSeasonsName = ["2020/2021", "2019/2020", "2018/2019"]

def load_json_file(file_path):
    with open(file_path, 'r', encoding="utf8") as f:
        data = json.load(f)
    return data

def load_competitions(conn):
    # /data/competitions.json
    data = load_json_file('data/competitions.json')

    cur = conn.cursor()

    # Iterate over each object and insert into the database
    for item in data:
        competition_name = item['competition_name']
        season_name = item['season_name']

        if (competition_name == validCompetitionName and season_name in validSeasonsName) or (competition_name == validPermier and season_name == validPermierSeason):
            
            competition_id = item['competition_id']
            season_id = item['season_id']
            country_name = item['country_name']

            competition_gender = item['competition_gender']
            competition_youth = item['competition_youth']
            competition_international = item['competition_international']
            match_updated = item['match_updated']
            match_updated_360 = item['match_updated_360']
            match_available_360 = item['match_available_360']
            match_available = item['match_available']

            # SQL query to insert data into the table
            insert_query = """INSERT INTO Competitions (
                CompetitionID, SeasonID, CountryName, CompetitionName, CompetitionGender,
                CompetitionYouth, CompetitionInternational, SeasonName, MatchUpdated,
                MatchUpdated360, MatchAvailable360, MatchAvailable
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (CompetitionID, SeasonID) DO NOTHING"""

            # Execute the SQL query
            cur.execute(insert_query, (
                competition_id, season_id, country_name, competition_name, competition_gender,
                competition_youth, competition_international, season_name, match_updated,
                match_updated_360, match_available_360, match_available
            ))

    # Commit the changes
    conn.commit()


# Not needed maybe
def load_360(conn):
    # All the 360 files are in the /data/360 folder
    # Iterate over each file and load the data into the database
    for file in os.listdir('data/360'):
        data = load_json_file('data/360/' + file)
        cur = conn.cursor()

        for item in data:
            event_uuid = item['event_uuid']
            visible_area = item['visible_area']

            # SQL query to insert data into the table
            insert_query = """INSERT INTO ThreeSixty (
                EventUUID, VisibleArea ) VALUES (%s, %s)"""
            
            # iterate through the freeze_frame array
            for freeze in item['freeze_frame']:
                teammate = freeze['teammate']
                actor = freeze['actor']
                keeper = freeze['keeper']
                location = freeze['location']

                # extract the x y z from location
                x = location[0]
                y = location[1]
                z = location[2]

                # SQL query to insert data into the table
                insert_query = """INSERT INTO FreezeFrame (
                    EventUUID, Teammate, Actor, Keeper, X, Y, Z ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cur.execute(insert_query, (
                    event_uuid, teammate, actor, keeper, x, y, z ))

            # Execute the SQL query
            cur.execute(insert_query, (
                event_uuid, visible_area ))

# ON CONFLICT (id) DO NOTHING
def load_matches(conn):
    # Every match is in a separate file in the /data/matches folder
    # Iterate over each file and load the data into the database

    cur = conn.cursor()

    for file in os.listdir('valid_matches\\'):
        data = load_json_file(os.path.join('valid_matches\\', file))

        for item in data:
            # Extract values
            match_id = item['match_id']
            match_date = item['match_date']
            kick_off = item['kick_off']

            competition_id = item['competition']['competition_id']
            # comp_country_name = item['competition']['country_name']
            # comp_name = item['competition']['competition_name']

            season_id = item['season']['season_id']
            # season_name = item['season']['season_name']

            home_country_id = item['home_team']['country']['id']
            home_country_name = item['home_team']['country']['name']
            home_team_id = item['home_team']['home_team_id']
            home_team_name = item['home_team']['home_team_name']
            home_team_gender = item['home_team']['home_team_gender']
            home_team_group = item['home_team']['home_team_group']

            away_country_id = item['away_team']['country']['id']
            away_country_name = item['away_team']['country']['name']
            away_team_id = item['away_team']['away_team_id']
            away_team_name = item['away_team']['away_team_name']
            away_team_gender = item['away_team']['away_team_gender']
            away_team_group = item['away_team']['away_team_group']
            
            if 'managers' in item['home_team']:
                for manager in item['home_team']['managers']:
                    manager_home_id = manager['id']
                    manager_home_name = manager['name']
                    manager_home_nickname = manager['nickname']
                    manager_home_dob = manager['dob']
                    manager_home_country_id = manager['country']['id']
                    manager_home_country_name = manager['country']['name']

                    cur.execute("INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s) ON CONFLICT (CountryID, CountryName) DO NOTHING", (manager_home_country_id, manager_home_country_name))
                    cur.execute("INSERT INTO Managers (ManagerID, ManagerName, Nickname, DateOfBirth, CountryID) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (ManagerID, ManagerName) DO NOTHING", (manager_home_id, manager_home_name, manager_home_nickname, manager_home_dob, manager_home_country_id))

            if 'managers' in item['away_team']:
                for manager in item['away_team']['managers']:
                    manager_away_id = manager['id']
                    manager_away_name = manager['name']
                    manager_away_nickname = manager['nickname']
                    manager_away_dob = manager['dob']
                    manager_away_country_id = manager['country']['id']
                    manager_away_country_name = manager['country']['name']
                    cur.execute("INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s) ON CONFLICT (CountryID, CountryName) DO NOTHING", (manager_away_country_id, manager_away_country_name))
                    cur.execute("INSERT INTO Managers (ManagerID, ManagerName, Nickname, DateOfBirth, CountryID) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (ManagerID, ManagerName) DO NOTHING", (manager_away_id, manager_away_name, manager_away_nickname, manager_away_dob, manager_away_country_id))
                    

            home_score = item['home_score']
            away_score = item['away_score']
            match_status = item['match_status']
            match_status_360 = item['match_status_360']
            last_updated = item['last_updated']
            last_updated_360 = item['last_updated_360']

            metadeta_data_version = item['metadata']['data_version']
            metadeta_shot_fidelity_version = item['metadata']['shot_fidelity_version']
            if 'xy_fidelity_version' in item['metadata']:
                metadeta_xy_fidelity_version = item['metadata']['xy_fidelity_version']

            match_week = item['match_week']
            competition_stage_id = item['competition_stage']['id']
            # competition_stage_name = item['competition_stage']['name']

            if 'stadium' in item:
                stadium_id = item['stadium']['id']
                stadium_name = item['stadium']['name']
                stadium_country_id = item['stadium']['country']['id']
                stadium_country_name = item['stadium']['country']['name']

            if 'referee' in item:
                referee_id = item['referee']['id']
                referee_name = item['referee']['name']
                referee_country_id = item['referee']['country']['id']
                referee_country_name = item['referee']['country']['name']

            cur.execute("INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s) ON CONFLICT (CountryID, CountryName) DO NOTHING", (home_country_id, home_country_name))
            cur.execute("INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s) ON CONFLICT (CountryID, CountryName) DO NOTHING", (away_country_id, away_country_name))
            cur.execute("INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s) ON CONFLICT (CountryID, CountryName) DO NOTHING", (stadium_country_id, stadium_country_name))
            cur.execute("INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s) ON CONFLICT (CountryID, CountryName) DO NOTHING", (referee_country_id, referee_country_name))
            cur.execute("INSERT INTO Referees (RefereeID, RefereeName, CountryID) VALUES (%s, %s, %s) ON CONFLICT (RefereeID, RefereeName) DO NOTHING", (referee_id, referee_name, referee_country_id))
            cur.execute("INSERT INTO Stadiums (StadiumID, StadiumName, CountryID) VALUES (%s, %s, %s) ON CONFLICT (StadiumID, StadiumName) DO NOTHING", (stadium_id, stadium_name, stadium_country_id))
            cur.execute("INSERT INTO Teams (TeamID, TeamName, TeamGender, TeamGroup, CountryID) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (TeamID, TeamName) DO NOTHING", (home_team_id, home_team_name, home_team_gender, home_team_group, home_country_id))
            cur.execute("INSERT INTO Teams (TeamID, TeamName, TeamGender, TeamGroup, CountryID) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (TeamID, TeamName) DO NOTHING", (away_team_id, away_team_name, away_team_gender, away_team_group, away_country_id))    
            cur.execute("""
                INSERT INTO Matches (MatchID, MatchDate, KickOff, CompetitionID, SeasonID, HomeTeam, AwayTeam, HomeScore, AwayScore, MatchStatus, MatchStatus360, LastUpdated, LastUpdated360, MatchWeek, CompetitionStage, Stadium, Referee)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (MatchID) DO NOTHING
            """, (match_id, match_date, kick_off, competition_id, season_id, home_team_id, away_team_id, home_score, away_score, match_status, match_status_360, last_updated, last_updated_360, match_week, competition_stage_id, stadium_id, referee_id))
            cur.execute("INSERT INTO MetaData (MatchID, DataVersion, ShotFidelityVersion, XYFidelityVersion) VALUES (%s, %s, %s, %s) ON CONFLICT (MatchID, DataVersion, ShotFidelityVersion, XYFidelityVersion) DO NOTHING", (match_id, metadeta_data_version, metadeta_shot_fidelity_version, metadeta_xy_fidelity_version))        

            # Extract values
        conn.commit()

def load_lineups(conn):
    # All the lineup files are in the /data/lineups folder
    # Iterate over each file and load the data into the database

    for file in os.listdir('valid_linups\\'):
        data = load_json_file('valid_linups\\' + file)
        cur = conn.cursor()

        for item in data:
            # No need to load team information again
            team_id = item['team_id']
            # team_name = item['team_name']
           
            # match id should be the file number
            match_id = file.split('.')[0]

            for player in item['lineup']:
                player_id = player['player_id']
                player_name = player['player_name']
                player_nickname = player['player_nickname']
                jersey_number = player['jersey_number']

                country_id = player['country']['id']
                country_name = player['country']['name']

                cur.execute("INSERT INTO Lineups (MatchID, TeamID) VALUES (%s, %s) ON CONFLICT (MatchID, TeamID) DO NOTHING", (match_id, team_id))
                cur.execute("INSERT INTO Country (CountryID, CountryName) VALUES (%s, %s) ON CONFLICT (CountryID, CountryName) DO NOTHING", (country_id, country_name))
                cur.execute("INSERT INTO Players (PlayerID, MatchID, TeamID, JerseyNumber, CountryID, PlayerName, Nickname) VALUES (%s, %s, %s, %s, %s, %s, %s)  ON CONFLICT (PlayerID) DO NOTHING", (player_id, match_id, team_id, jersey_number, country_id, player_name, player_nickname))


                for position in player['positions']:
                    position_id = position['position_id']
                    # position_name = position['position']
                    from_time = position['from']
                    to_time = position['to']
                    from_period = position['from_period']
                    to_period = position['to_period']
                    start_reason = position['start_reason']
                    end_reason = position['end_reason']

                    # cur.execute("INSERT INTO Positions (PositionID, Name) VALUES (%s, %s) ON CONFLICT (PositionID, Name) DO NOTHING", (position_id, position_name))
                    cur.execute("INSERT INTO PlayerPositions (PlayerPositionID, MatchID, PlayerID, PositionID, SwitchedFrom, SwitchedTo, FromPeriod, ToPeriod, StartReason, EndReason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  ON CONFLICT (PlayerPositionID, MatchID, PlayerID) DO NOTHING", (player_id, match_id, player_id, position_id, from_time, to_time, from_period, to_period, start_reason, end_reason))
                

        conn.commit()


# CREATE TABLE Events (
#   EventID UUID PRIMARY KEY,
#   Index INT,
#   Period INT,
#   Timestamp TIME,
#   Minute INT,
#   Second INT,
#   EventType INT,
#   EventTypeName VARCHAR(255),
#   Possession INT,
#   PossessionTeamID INT,
#   PossessionTeamName VARCHAR(255),
#   PlayPatternID INT,
#   PlayPatternName VARCHAR(255),
#   TeamID INT,
#   TeamName VARCHAR(255),
#   PlayerID INT,
#   PlayerName VARCHAR(255),
#   PositionID INT,
#   PositionName VARCHAR(255),
#   LocationX DOUBLE PRECISION,
#   LocationY DOUBLE PRECISION,
#   Duration DECIMAL,
#   UnderPressure BOOLEAN,
#   OffCamera BOOLEAN,
#   Out BOOLEAN,
#   RelatedEvents UUID[],

#   FOREIGN KEY (PossessionTeamID) REFERENCES Teams(TeamID),
#   FOREIGN KEY (TeamID) REFERENCES Teams(TeamID),
#   FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
# )
def load_events(conn):
    # All the events files are in the /data/events folder
    # Iterate over each file and load the data into the database
    json_directory = 'valid_event\\'
    for file in os.listdir(json_directory):
        data = load_json_file(os.path.join(json_directory, file))
        cur = conn.cursor()
        event_match_id = file.split('.')[0]

        for item in data:
            event_id = item['id']
            index = item['index']
            period = item['period']
            timestamp = item['timestamp']
            minute = item['minute']
            second = item['second']
            event_type = item['type']['id']
            event_type_name = item['type']['name']
            possession = item['possession']
            possession_team_id = item['possession_team']['id']
            possession_team_name = item['possession_team']['name']
            play_pattern_id = item['play_pattern']['id']
            play_pattern_name = item['play_pattern']['name']
            team_id = item['team']['id']
            team_name = item['team']['name']
            if 'tactics' in item:
                player_id = item['tactics']['lineup'][0]['player']['id']
                player_name = item['tactics']['lineup'][0]['player']['name']
                position_id = item['tactics']['lineup'][0]['position']['id']
                position_name = item['tactics']['lineup'][0]['position']['name']
            if 'location' in item and len(item['location']) >= 2:
                location_x = item['location'][0]
                location_y = item['location'][1]
            else:
                location_x = None
                location_y = None
            duration = item.get('duration')
            under_pressure = item.get('under_pressure')
            off_camera = item.get('off_camera')
            out = item.get('out')
            # Covert to uuid array
            related_events = []
            if 'related_events' in item:
                # Convert UUID strings to UUID objects and then cast to uuid[]
                related_events = [f"'{uuid_str}'::uuid" for uuid_str in related_events]

                # Join the casted UUID strings into a PostgreSQL array format
                related_events = f"{{{','.join(related_events)}}}"


            cur.execute("""
                INSERT INTO Events (EventID, MatchID, Index, Period, Timestamp, Minute, Second, EventType, EventTypeName, Possession, PossessionTeamID, PossessionTeamName, PlayPatternID, PlayPatternName, TeamID, TeamName, PlayerID, PlayerName, PositionID, PositionName, LocationX, LocationY, Duration, UnderPressure, OffCamera, Out, RelatedEvents)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (EventID) DO NOTHING
            """, (event_id, event_match_id, index, period, timestamp, minute, second, event_type, event_type_name, possession, possession_team_id, possession_team_name, play_pattern_id, play_pattern_name, team_id, team_name, player_id, player_name, position_id, position_name, location_x, location_y, duration, under_pressure, off_camera, out, related_events))
            
            
            if (item.get('pass') is not None):
                load_pass(conn, item.get('pass'), event_id)
            if (item.get('carry') is not None):
                load_carry(conn, item.get('carry') , event_id)
            if (item.get('duel') is not None):
                load_duel(conn, item['duel'], event_id)
            if (item.get('foul_committed') is not None):
                load_foul_committed(conn, item['foul_committed'], event_id)
            if (item.get('foul_won') is not None):
                load_foul_won(conn, item['foul_won'], event_id)
            if (item.get('goalkeeper') is not None):
                load_goalkeeper(conn, item['goalkeeper'], event_id)
            if (item.get('interception') is not None):
                load_interception(conn, item['interception'], event_id)
            if (item.get('miscontrol') is not None):
                load_miscontrol(conn, item['miscontrol'], event_id)
            if (item.get('block') is not None):
                load_block(conn, item['block'], event_id)
            if (item.get('clearance') is not None):
                load_clearance(conn, item['clearance'], event_id)
            if (item.get('dribble') is not None):
                load_dribble(conn, item['dribble'], event_id)
            if (item.get('dribbled_past') is not None):
                load_dribbled_past(conn, item['dribbled_past'], event_id)
            if (item.get('ball_recovery') is not None):
                load_ball_recovery(conn, item['ball_recovery'], event_id)
            if (item.get('ball_receipt') is not None):
                load_ball_receipt(conn, item['ball_receipt'], event_id)
            if (item.get('injury_stoppage') is not None):
                load_injury_stoppage(conn, item['injury_stoppage'], event_id)
            if (item.get('half_start') is not None):
                load_half_start(conn, item['half_start'], event_id)
            if (item.get('half_end') is not None):
                load_half_end(conn, item['half_end'], event_id)
            if (item.get('shot') is not None):
                load_shot(conn, item['shot'], event_id)
            
    conn.commit()
            # Then we need to check for the special events



# CREATE TABLE Tactics (
#   EventID UUID PRIMARY KEY,
#   Formation INT,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
# CREATE TABLE TacticLineupPlayer (
#   TacticID UUID PRIMARY KEY,
#   PlayerID INT,
#   PositionID INT,

#   FOREIGN KEY (TacticID) REFERENCES Tactics(EventID),
#   FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
  
# );
def load_tactics(conn, item, event_id):
    cur = conn.cursor()

    formation = item['tactics']['formation']

    cur.execute("INSERT INTO Tactics (EventID, Formation) VALUES (%s, %s)", (event_id, formation))

    for player in item['tactics']['lineup']:
        player_id = player['player']['id']
        position_id = player['position']['id']

        cur.execute("INSERT INTO TacticLineupPlayer (TacticID, PlayerID, PositionID) VALUES (%s, %s, %s)", (event_id, player_id, position_id))
# CREATE TABLE FiftyFifty (
#   EventID UUID,
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),
#   Counterpress BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_5050(conn,data, event_id):
    cur = conn.cursor()
    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')
    counterpress = data.get('counterpress')

    cur.execute("INSERT INTO FiftyFifty (EventID, OutcomeID, OutcomeName, Counterpress) VALUES (%s, %s, %s, %s)", (event_id, outcome_id, outcome_name, counterpress))

# CREATE TABLE BadBehaviour (
#   EventID UUID,
#   CardID INT,
#   CardName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );

def load_bad_behaviour(conn,data,event_id):
    cur = conn.cursor()

    card_id = data.get('card', {}).get('id')
    card_name = data.get('card', {}).get('name')

    cur.execute("INSERT INTO BadBehaviour (EventID, CardID, CardName) VALUES (%s, %s, %s)", (event_id, card_id, card_name))

# CREATE TABLE BallReceipt (
#   EventID UUID,
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_ball_receipt(conn,data,event_id):
    cur = conn.cursor()

    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')

    cur.execute("INSERT INTO BallReceipt (EventID, OutcomeID, OutcomeName) VALUES (%s, %s, %s)", (event_id, outcome_id, outcome_name))

# CREATE TABLE BallRecovery (
#   EventID UUID,
#   Offensive BOOLEAN,
#   RecoveryFailure BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_ball_recovery(conn,data, event_id):
    cur = conn.cursor()

    offensive = data.get('offensive')
    recovery_failure = data.get('recovery_failure')

    cur.execute("INSERT INTO BallRecovery (EventID, Offensive, RecoveryFailure) VALUES (%s, %s, %s)", (event_id, offensive, recovery_failure))
  
# CREATE TABLE Block (
#   EventID UUID,
#   Deflection BOOLEAN,
#   Offensive BOOLEAN,
#   SaveBlock BOOLEAN,
#   Counterpress BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_block(conn,data, event_id):
    cur = conn.cursor()

    deflection = data.get('deflection')
    offensive = data.get('offensive')
    save_block = data.get('save_block')
    counterpress = data.get('counterpress')

    cur.execute("INSERT INTO Block (EventID, Deflection, Offensive, SaveBlock, Counterpress) VALUES (%s, %s, %s, %s, %s)", (event_id, deflection, offensive, save_block, counterpress))

# CREATE TABLE Carry (
#   EventID UUID,
#   EndLocationX DOUBLE PRECISION,
#   EndLocationY DOUBLE PRECISION,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_carry(conn,data, event_id):
    cur = conn.cursor()

    end_location_x = data.get('end_location', [])[0]
    end_location_y = data.get('end_location', [])[1]

    cur.execute("INSERT INTO Carry (EventID, EndLocationX, EndLocationY) VALUES (%s, %s, %s)", (event_id, end_location_x, end_location_y))

# CREATE TABLE Clearance (
#   EventID UUID,
#   AerialWon BOOLEAN,
#   BodyPartID INT,
#   BodyPartName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );

def load_clearance(conn,data, event_id):
    cur = conn.cursor()

    aerial_won = data.get('aerial_won')
    body_part_id = data.get('body_part', {}).get('id')
    body_part_name = data.get('body_part', {}).get('name')

    cur.execute("INSERT INTO Clearance (EventID, AerialWon, BodyPartID, BodyPartName) VALUES (%s, %s, %s, %s)", (event_id, aerial_won, body_part_id, body_part_name))

# CREATE TABLE Dribble (
#   EventID UUID,
#   Overrun BOOLEAN,
#   Nutmeg BOOLEAN,
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),
#   NoTouch BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_dribble(conn,data, event_id):
    cur = conn.cursor()

    overrun = data.get('overrun')
    nutmeg = data.get('nutmeg')
    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')
    no_touch = data.get('no_touch')
    cur.execute("INSERT INTO Dribble (EventID, Overrun, Nutmeg, OutcomeID, OutcomeName, NoTouch) VALUES (%s, %s, %s, %s, %s, %s)", (event_id, overrun, nutmeg, outcome_id, outcome_name, no_touch))

# CREATE TABLE DribbledPast (
#   EventID UUID,
#   Counterpress BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_dribbled_past(conn,data, event_id):
    cur = conn.cursor()

    counterpress = data.get('counterpress')

    cur.execute("INSERT INTO DribbledPast (EventID, Counterpress) VALUES (%s, %s)", (event_id, counterpress))

# CREATE TABLE Duel (
#   EventID UUID,
#   Counterpress BOOLEAN,
#   TypeID INT,
#   TypeName VARCHAR(255),
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_duel(conn,data, event_id):
    cur = conn.cursor()


    counterpress = data.get('counterpress')
    type_id = data.get('type', {}).get('id')
    type_name = data.get('type', {}).get('name')
    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')
    cur.execute("INSERT INTO Duel (EventID, Counterpress, TypeID, TypeName, OutcomeID, OutcomeName) VALUES (%s, %s, %s, %s, %s, %s)", (event_id, counterpress, type_id, type_name, outcome_id, outcome_name))

# CREATE TABLE FoulCommitted (
#   EventID UUID,
#   Counterpress BOOLEAN,
#   Offensive BOOLEAN,
#   TypeID INT,
#   TypeName VARCHAR(255),
#   Advantage BOOLEAN,
#   Penalty BOOLEAN,
#   CardID INT,
#   CardName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );

def load_foul_committed(conn,data, event_id):
    cur = conn.cursor()

    counterpress = data.get('counterpress')
    offensive = data.get('offensive')
    type_id = data.get('type', {}).get('id')
    type_name = data.get('type', {}).get('name')
    advantage = data.get('advantage')
    penalty = data.get('penalty')
    card_id = data.get('card', {}).get('id')
    card_name = data.get('card', {}).get('name')

    cur.execute("INSERT INTO FoulCommitted (EventID, Counterpress, Offensive, TypeID, TypeName, Advantage, Penalty, CardID, CardName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (event_id, counterpress, offensive, type_id, type_name, advantage, penalty, card_id, card_name))

# CREATE TABLE FoulWon (
#   EventID UUID,
#   Defensive BOOLEAN,
#   Advantage BOOLEAN,
#   Penalty BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_foul_won(conn,data, event_id):
    cur = conn.cursor()

    defensive = data.get('defensive')
    advantage = data.get('advantage')
    penalty = data.get('penalty')
    cur.execute("INSERT INTO FoulWon (EventID, Defensive, Advantage, Penalty) VALUES (%s, %s, %s, %s)", (event_id, defensive, advantage, penalty))

# CREATE TABLE Goalkeeper (
#   EventID UUID,
#   PositionID INT,
#   PositionName VARCHAR(255),
#   TechniqueID INT,
#   TechniqueName VARCHAR(255),
#   BodyPartID INT,
#   TypeID INT,
#   TypeName VARCHAR(255),
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),
#   BodyPartName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_goalkeeper(conn,data, event_id):
    cur = conn.cursor()

    position_id = data.get('position', {}).get('id')
    position_name = data.get('position', {}).get('name')
    technique_id = data.get('technique', {}).get('id')
    technique_name = data.get('technique', {}).get('name')
    body_part_id = data.get('body_part', {}).get('id')
    type_id = data.get('type', {}).get('id')
    type_name = data.get('type', {}).get('name')
    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')
    body_part_name = data.get('body_part', {}).get('name')

    cur.execute("INSERT INTO Goalkeeper (EventID, PositionID, PositionName, TechniqueID, TechniqueName, BodyPartID, TypeID, TypeName, OutcomeID, OutcomeName, BodyPartName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (event_id, position_id, position_name, technique_id, technique_name, body_part_id, type_id, type_name, outcome_id, outcome_name, body_part_name))

# CREATE TABLE HalfEnd (
#   EventID UUID,
#   EarlyVideoEnd BOOLEAN,
#   MatchSuspended BOOLEAN,
  
#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_half_end(conn,data, event_id):
    cur = conn.cursor()

    early_video_end = data.get('early_video_end')
    match_suspended = data.get('match_suspended')

    cur.execute("INSERT INTO HalfEnd (EventID, EarlyVideoEnd, MatchSuspended) VALUES (%s, %s, %s)", (event_id, early_video_end, match_suspended))

# CREATE TABLE HalfStart (
#   EventID UUID,
#   LateVideoStart BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_half_start(conn,data, event_id):
    cur = conn.cursor()

    late_video_start = data.get('late_video_start')

    cur.execute("INSERT INTO HalfStart (EventID, LateVideoStart) VALUES (%s, %s)", (event_id, late_video_start))

# CREATE TABLE InjuryStoppage (
#   EventID UUID,
#   InChain BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_injury_stoppage(conn,data, event_id):
    cur = conn.cursor()

    in_chain = data.get('in_chain')

    cur.execute("INSERT INTO InjuryStoppage (EventID, InChain) VALUES (%s, %s)", (event_id, in_chain))


# CREATE TABLE Interception (
#   EventID UUID,
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_interception(conn,data, event_id):
    cur = conn.cursor()

    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')

    cur.execute("INSERT INTO Interception (EventID, OutcomeID, OutcomeName) VALUES (%s, %s, %s)", (event_id, outcome_id, outcome_name))

# CREATE TABLE Miscontrol (
#   EventID UUID,
#   AerialWon BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_miscontrol(conn,data, event_id):
    cur = conn.cursor()

    aerial_won = data.get('aerial_won')

    cur.execute("INSERT INTO Miscontrol (EventID, AerialWon) VALUES (%s, %s)", (event_id, aerial_won))


# CREATE TABLE Pass (
#   EventID UUID,
#   Recipient INT,
#   Length DECIMAL,
#   Angle DECIMAL,
#   HeightID INT,
#   HeightName VARCHAR(255),
#   EndLocationX DOUBLE PRECISION,
#   EndLocationY DOUBLE PRECISION,
#   AssisstedShot UUID,
#   Backheel BOOLEAN,
#   Deflected BOOLEAN,
#   Miscommunication BOOLEAN,
#   IsCross BOOLEAN,
#   CutBack BOOLEAN,
#   Switch BOOLEAN,
#   ShotAssist BOOLEAN,
#   GoalAssist BOOLEAN,
#   BodyPartID INT,
#   BodyPartName VARCHAR(255),
#   TypeID INT,
#   TypeName VARCHAR(255),
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),
#   TechniqueID INT,
#   TechniqueName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID),
#   FOREIGN KEY (Recipient) REFERENCES Players(PlayerID)
# );
def load_pass(conn, data, event_id):
    cur = conn.cursor()

    recipient = data.get('recipient', {}).get('id')
    length = data.get('length')
    angle = data.get('angle')
    height_id = data.get('height', {}).get('id')
    height_name = data.get('height', {}).get('name')
    end_location_x = data.get('end_location', [])[0]
    end_location_y = data.get('end_location', [])[1]
    assissted_shot = data.get('assissted_shot')
    backheel = data.get('backheel')
    deflected = data.get('deflected')
    miscommunication = data.get('miscommunication')
    is_cross = data.get('is_cross')
    cut_back = data.get('cut_back')
    switch = data.get('switch')

    cur.execute("""
    INSERT INTO Pass 
    (EventID, Recipient, Length, Angle, HeightID, HeightName, EndLocationX, EndLocationY, AssisstedShot, Backheel, Deflected, Miscommunication, IsCross, CutBack, Switch) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    event_id, recipient, length, angle, height_id, height_name, end_location_x, end_location_y, 
    assissted_shot, backheel, deflected, miscommunication, is_cross, cut_back, switch
))
    conn.commit()
# CREATE TABLE PlayerOff (
#   EventID UUID,
#   Permanent BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_player_off(conn,data, event_id):
    cur = conn.cursor()

    permanent = data.get('permanent')

    cur.execute("INSERT INTO PlayerOff (EventID, Permanent) VALUES (%s, %s)", (event_id, permanent))

# CREATE TABLE Pressure (
#   EventID UUID,
#   Counterpress BOOLEAN,

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );

def load_pressure(conn,data, event_id):
    cur = conn.cursor()

    counterpress = data.get('counterpress')

    cur.execute("INSERT INTO Pressure (EventID, Counterpress) VALUES (%s, %s)", (event_id, counterpress))

# CREATE TABLE Shot (
#   EventID UUID,
#   KeyPassID UUID UNIQUE,
#   EndLocationX DOUBLE PRECISION,
#   EndLocationY DOUBLE PRECISION, 
#   EndLocationZ DOUBLE PRECISION,
#   AerialWon BOOLEAN,
#   FollowsDribble BOOLEAN,
#   FirstTime BOOLEAN,
#   OpenGoal BOOLEAN,
#   StatsbombXG DECIMAL,
#   Deflected BOOLEAN,
#   TechniqueID INT,
#   TechniqueName VARCHAR(255),
#   BodyPartID INT,
#   BodyPartName VARCHAR(255),
#   TypeID INT,
#   TypeName VARCHAR(255),
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID)
# );
def load_shot(conn,data, event_id):
    cur = conn.cursor()
    key_pass_id = data.get('key_pass_id')
    end_location_x = data.get('end_location', [])[0]
    end_location_y = data.get('end_location', [])[1]
    end_location_list = data.get('end_location', [])
    end_location_z = end_location_list[2] if len(end_location_list) >= 3 else None
    aerial_won = data.get('aerial_won')
    follows_dribble = data.get('follows_dribble')
    first_time = data.get('first_time')
    open_goal = data.get('open_goal')
    statsbomb_xg = data.get('statsbomb_xg')
    deflected = data.get('deflected')
    technique_id = data.get('technique', {}).get('id')
    technique_name = data.get('technique', {}).get('name')
    body_part_id = data.get('body_part', {}).get('id')
    body_part_name = data.get('body_part', {}).get('name')
    type_id = data.get('type', {}).get('id')
    type_name = data.get('type', {}).get('name')
    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')
    
    cur.execute("""
    INSERT INTO Shot 
    (EventID, KeyPassID, EndLocationX, EndLocationY, EndLocationZ, AerialWon, FollowsDribble, FirstTime, OpenGoal, StatsbombXG, Deflected, TechniqueID, TechniqueName, BodyPartID, BodyPartName, TypeID, TypeName, OutcomeID, OutcomeName) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    event_id, key_pass_id, end_location_x, end_location_y, end_location_z, aerial_won, follows_dribble, first_time, open_goal, statsbomb_xg, deflected, technique_id, technique_name, body_part_id, body_part_name, type_id, type_name, outcome_id, outcome_name
))
    
# CREATE TABLE FreezeFrame (
#   EventID UUID,
#   LocationX DOUBLE PRECISION,
#   LocationY DOUBLE PRECISION,
#   LocationZ DOUBLE PRECISION,
#   Player INT,
#   PositionID INT,
#   Teammate BOOLEAN,
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID),
#   FOREIGN KEY (Player) REFERENCES Players(PlayerID)
# );
def load_freeze_frame(conn,data, event_id):
    cur = conn.cursor()

    location_x = data.get('location', [])[0]
    location_y = data.get('location', [])[1]
    location_z = data.get('location', [])[2]
    player = data.get('player', {}).get('id')
    position_id = data.get('position', {}).get('id')
    teammate = data.get('teammate')
    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')

    cur.execute("INSERT INTO FreezeFrame (EventID, LocationX, LocationY, LocationZ, Player, PositionID, Teammate, OutcomeID, OutcomeName) VALUES"
                "(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (event_id, location_x, location_y, location_z, player, position_id, teammate, outcome_id, outcome_name))

# CREATE TABLE Substitution (
#   EventID UUID,
#   Replacement INT,
#   OutcomeID INT,
#   OutcomeName VARCHAR(255),

#   FOREIGN KEY (EventID) REFERENCES Events(EventID),
#   FOREIGN KEY (Replacement) REFERENCES Players(PlayerID)
# );

def load_substitution(conn,data, event_id):
    cur = conn.cursor()

    replacement = data.get('replacement', {}).get('id')
    outcome_id = data.get('outcome', {}).get('id')
    outcome_name = data.get('outcome', {}).get('name')

    cur.execute("INSERT INTO Substitution (EventID, Replacement, OutcomeID, OutcomeName) VALUES (%s, %s, %s, %s)", (event_id, replacement, outcome_id, outcome_name))


# ON CONFLICT (id) DO NOTHING ????

if __name__ == "__main__":
    # Connect to the database

    # We only need La Liga 2020/2021, 2019/2020, 2018/2019, and 2003/2004 seasons
    conn = psycopg2.connect(database=root_database_name, user=db_username, password=db_password, host=db_host, port=db_port)
    load_competitions(conn)
    load_matches(conn)
    load_lineups(conn)
    load_events(conn)