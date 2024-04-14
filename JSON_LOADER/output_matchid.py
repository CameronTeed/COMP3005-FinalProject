import os
import json


def extract_match_id():
    """
    Extracts match IDs from JSON files in the 'valid_matches' directory and writes them to 'match_id.txt'.
    """
    json_directory = 'valid_matches\\'

    # Open file to write match_id
    with open('match_id.txt', 'w') as f:
        for file in os.listdir(json_directory):
            file_path = os.path.join(json_directory, file)
            data = load_json_file(file_path)

            for match in data:
                match_id = match['match_id']
                f.write(str(match_id) + '\n')


def load_json_file(file_path):
    with open(file_path, 'r', encoding="utf8") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    extract_match_id()