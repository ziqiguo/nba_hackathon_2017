data_root_dir = 'data'

def load_player_maps(filename):
  player_map = {}
  sv_player_map = {}

  with open(filename, 'rb') as csvfile:
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
  def __init__(self, game_id, person_id, person_name, shot_result, shot_dist, close_def_dist, pts_type):
    self.game_id = game_id
    self.person_id = person_id
    self.person_name = person_name
    self.shot_result = shot_result
    self.shot_dist = shot_dist
    self.close_def_dist = close_def_dist
    self.pts_type = pts_type
  def __str__(self):
    return self.person_name
  def __repr__(self):
    return self.__str__()
        
player_map, player_svu_map = load_player_maps('%s/Player_Map.csv' % data_root_dir)
player_map_new = {'PERSON_ID':[], 'PERSON_NAME':[]}
for key, value in player_map.items():
    player_map_new['PERSON_ID'].append(key)
    player_map_new['PERSON_NAME'].append(value.name)
player_map_df = pd.DataFrame.from_dict(player_map_new)
player_map_df.head()

filename1 = 'data/Player Tracking Data/2015-16_nba_shot_log.txt'
filename2 = 'data/Player Tracking Data/2016-17_nba_shot_log.txt'
shot_1516 = pd.read_csv(filename1, sep='\t')
shot_1516 = pd.merge(shot_1516, player_map_df, on='PERSON_ID')
shot_1516 = shot_1516[['GAME_ID','PERSON_ID','PERSON_NAME','SHOT_RESULT','SHOT_DIST','CLOSE_DEF_DIST','PTS_TYPE']]

shot_1617 = pd.read_csv(filename2, sep='\t')
shot_1617 = pd.merge(shot_1617, player_map_df, on='PERSON_ID')
shot_1617 = shot_1617[['GAME_ID','PERSON_ID','PERSON_NAME','SHOT_RESULT','SHOT_DIST','CLOSE_DEF_DIST','PTS_TYPE']]

shot_df = pd.concat([shot_1516, shot_1617], axis=0)

shot_dict = {}
for row in shot_df.iterrows():
    temp = row[1]
    shot = NBAShot(temp['GAME_ID'], temp['PERSON_ID'], temp['PERSON_NAME'], temp['SHOT_RESULT'], temp['SHOT_DIST'], temp['CLOSE_DEF_DIST'], temp['PTS_TYPE'])
    if shot.person_id in shot_dict.keys():
        shot_dict[shot.person_id].append(shot)
    else:
        shot_dict[shot.person_id] = [shot]

print(len(shot_dict))