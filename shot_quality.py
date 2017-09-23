from ShotParser import load_shots
from NBADataParser import load_player_maps, load_team_maps
import pandas as pd

data_root_dir = 'data'

defender_distance_range = 2
shot_distance_range = 3
player_map_file_name = '%s/Player_Map.csv' % data_root_dir
team_map_file_name = '%s/Team_Map.csv' % data_root_dir

class ShotQuality:
  def __init__(self):
    self.shots = load_shots()
    print('Shots loaded')
#    self.shots = {201939: ['a']}

  def shot_quality(self, player_id, defender_distance, shot_distance, shot_value):
    shots = self.shots[player_id]
    lb_def_dist = max(defender_distance - defender_distance_range, 0) # lower bound for defender distance
    ub_def_dist = defender_distance + defender_distance_range # upper bound for defender distance
    lb_shot_dist = max(shot_distance - shot_distance_range, 0)
    ub_shot_dist = shot_distance + shot_distance_range
    shot_count = 0
    made = 0
    dist_hist = dict()
    # print lb_def_dist
    # print ub_def_dist
    # print lb_shot_dist
    # print ub_shot_dist
    for shot in shots:
      if shot.defender_distance >= lb_def_dist and shot.defender_distance <= ub_def_dist:
        if shot.shot_distance >= lb_shot_dist and shot.shot_distance <= ub_shot_dist:
          shot_count += 1
          if shot.made:
            made += 1
    # print shot_count
    # print made
    # print float(made)/shot_count
    if shot_count == 0:
      return 0.5*shot_value
    ev = float(made)/shot_count * shot_value
    return ev

  def shot_quality_player(self):
    shot_quality_player_dict = {}
    for key, value in self.shots.items():
      for shot in value:
        quality = ShotQuality().shot_quality(key, shot.defender_distance, shot.shot_distance, shot.pts_type)
        if key in shot_quality_player_dict.keys():
          shot_quality_player_dict[key] += (quality)
        else:
          shot_quality_player_dict[key] = quality
      shot_quality_player_dict[key] /= len(value)

    player_map, player_svu_map = load_player_maps(player_map_file_name)
    player_map_new = {'PERSON_ID':[], 'PERSON_NAME':[], 'SHOT_QUALITY':[]}
    for key, value in team_map.items():
      player_map_new['PERSON_ID'].append(key)
      player_map_new['PERSON_NAME'].append(value.name)
      player_map_new['SHOT_QUALITY'].append(shot_quality_team_dict[key])
    shot_quality_player_df = pd.DataFrame.from_dict(player_map_new)
    shot_quality_player_df = shot_quality_player_df.sort_values(by='SHOT_QUALITY', ascending=False)
    return shot_quality_player_dict, shot_quality_player_df


  def shot_quality_team(self):
    shot_quality_team_dict = {}
    for key, value in self.shots.items():
      for shot in value:
        quality = self.shot_quality(shot.person_id, shot.defender_distance, shot.shot_distance, shot.pts_type)
        if shot.team_id in shot_quality_team_dict.keys():
          shot_quality_team_dict[shot.team_id][0] += quality
          shot_quality_team_dict[shot.team_id][1] += 1
        else:
          shot_quality_team_dict[shot.team_id] = [quality, 1]

    for key, value in shot_quality_team_dict.items():
      shot_quality_team_dict[key] = value[0] / value[1]

    print('Dictionary created')
    team_map, team_svu_map = load_team_maps(team_map_file_name)
    team_map_new = {'TEAM_ID':[], 'TEAM_NAME':[], 'SHOT_QUALITY':[]}
    for key, value in team_map.items():
      team_map_new['TEAM_ID'].append(key)
      team_map_new['TEAM_NAME'].append(value.name)
      team_map_new['SHOT_QUALITY'].append(shot_quality_team_dict[key])
    shot_quality_team_df = pd.DataFrame.from_dict(team_map_new)
    shot_quality_team_df = shot_quality_team_df.sort_values(by='SHOT_QUALITY', ascending=False)
    return shot_quality_team_dict, shot_quality_team_df

print(ShotQuality().shot_quality_team()[1])





#shotQuality = ShotQuality()
#print shotQuality.shot_quality(201939, 4, 23, 3)
