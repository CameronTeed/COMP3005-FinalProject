import os
import shutil
import json

validPermier = "Premier League"
validPermierSeason = "2003/2004"

validCompetitionName = "La Liga"
validSeasonsName = ["2020/2021", "2019/2020", "2018/2019"]

def find_matches():
    # All the matches are in /data/matches
    json_file = 'data/matches'
    
    for folder in os.listdir(json_file):
        for file in os.listdir(os.path.join(json_file, folder)):
            file_path = os.path.join(json_file, folder, file)
            data = load_json_file(file_path)

            for match in data:
                competition_name = match['competition']['competition_name']
                season_name = match['season']['season_name']

                if (competition_name == validCompetitionName and season_name in validSeasonsName) or (competition_name == validPermier and season_name == validPermierSeason):
                    source = file_path
                    destination = os.path.join('valid_matches', file)

                    if not os.path.exists(destination):  # Check if file already exists in destination
                        shutil.move(source, destination) 

def load_json_file(file_path):
    with open(file_path, 'r', encoding="utf8") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    find_matches()