# This script gets the valid files from /data/events and /data/lineups by matching the file name with a match_id fromt match_id.txt
# The file is then moved to the valid folder

import os
import shutil
import json

def move_events():
    """
    Moves the JSON files in the 'data/events' directory to the 'valid_matches' directory
    if they have a match ID that is in 'match_id.txt'.
    """
    events_directory = 'data/lineups/'
    valid_directory = 'valid_linups/'
    match_id_file = 'match_id.txt'

    # Get match IDs from 'match_id.txt'
    with open(match_id_file, 'r') as f:
        match_ids = f.read().splitlines()

    # Iterate through JSON files in events directory
    for filename in os.listdir(events_directory):
        if filename.endswith('.json'):
            # Extract match ID from filename
            event_match_id = os.path.splitext(filename)[0]
            # Check if match ID is in match_ids list
            if event_match_id in match_ids:
                # Construct source and destination paths
                src_path = os.path.join(events_directory, filename)
                dest_path = os.path.join(valid_directory, filename)
                # Move the file
                shutil.move(src_path, dest_path)


def load_json_file(file_path):
    with open(file_path, 'r', encoding="utf8") as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    move_events()