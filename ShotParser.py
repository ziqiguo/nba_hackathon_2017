import csv, pickle
from nba import NBAPlayer
import pandas as pd
data_root_dir = 'data'
player_map_file_name = '%s/Player_Map.csv' % data_root_dir
shot_log_path = '%s/NBAPlayerTrackingData_2014-17/' % data_root_dir
pklFile = 'shot-quality.pkl'

def load_player_maps(filename):
  player_map = {}
  sv_player_map = {}

  with open(filename, 'rU') as csvfile:
    csv_reader = csv.reader(csvfile)
    csv_reader.next()

    for row in csv_reader:
      player_id = int(row[0])
      sv_player_id = int(row[1]) if row[1] != 'n/a' else None
      name = row[2]

      player = NBAPlayer(name, player_id, sv_player_id)

      player_map[player_id] = player
      if sv_player_id:
        sv_player_map[sv_player_id] = player

  return player_map, sv_player_map


class NBAShot:
  def __init__(self, game_id, team_id, person_id, person_name, shot_result, shot_dist, close_def_dist, pts_type):
    self.game_id = game_id
    self.team_id = team_id
    self.person_id = person_id
    self.person_name = person_name
    self.made = shot_result == 'made'
    self.shot_distance = shot_dist
    self.defender_distance = close_def_dist
    self.pts_type = pts_type
  def __str__(self):
    return str(vars(self))
  def __repr__(self):
    return self.__str__()

# Returns one dictionary:
# Key: player ID
# Value: shot information
def load_shots():
  try:
    return pickle.load(open(pklFile, "rb"))
  except:
    print 'creating pickle file'
    return read_file()

def read_file():
  player_map, player_svu_map = load_player_maps(player_map_file_name)
  player_map_new = {'PERSON_ID':[], 'PERSON_NAME':[]}
  for key, value in player_map.items():
      player_map_new['PERSON_ID'].append(key)
      player_map_new['PERSON_NAME'].append(value.name)
  player_map_df = pd.DataFrame.from_dict(player_map_new)
  player_map_df.head()

  filenames = ['2014-15_nba_shot_log.txt', '2015-16_nba_shot_log.txt', '2016-17_nba_shot_log.txt']
  shot_pds = []
  for filename in filenames:
    filename = shot_log_path + filename
    shot_arr = pd.read_csv(filename, sep='\t')
    shot_arr  = pd.merge(shot_arr, player_map_df, on='PERSON_ID')
    shot_arr = shot_arr[['TEAM_ID', 'GAME_ID','PERSON_ID','PERSON_NAME','SHOT_RESULT','SHOT_DIST','CLOSE_DEF_DIST','PTS_TYPE']]
    shot_pds.append(shot_arr)

  shot_df = pd.concat(shot_pds, axis=0)
  shot_dict = {}
  for row in shot_df.iterrows():
      temp = row[1]
      shot = NBAShot(temp['GAME_ID'], temp['TEAM_ID'], temp['PERSON_ID'], temp['PERSON_NAME'], temp['SHOT_RESULT'], temp['SHOT_DIST'], temp['CLOSE_DEF_DIST'], temp['PTS_TYPE'])
      if shot.person_id in shot_dict.keys():
          shot_dict[shot.person_id].append(shot)
      else:
          shot_dict[shot.person_id] = [shot]

  pickle.dump(shot_dict, open(pklFile, "wb"))
  return shot_dict
