# Go through pass log and determine number of points that could have been created
# via assist (based on shot quality)
import pickle
import math
from NBADataParser import *
from shot_quality import ShotQuality

shot_filenames = ['data/NBAPlayerTrackingData_2014-17/2015-16_nba_shot_log.txt',
                  'data/NBAPlayerTrackingData_2014-17/2016-17_nba_shot_log.txt']
pass_filenames = ['data/NBAPlayerTrackingData_2014-17/2015-16_nba_pass_log.txt',
                  'data/NBAPlayerTrackingData_2014-17/2016-17_nba_pass_log.txt']

class NBAShot:
  def __init__(self, line):
    self.player_id = int(line[1])
    self.period = int(line[8])
    self.game_clock = float(line[9]) / 10
    self.dribbles = int(line[11])
    self.shot_distance = float(line[12])
    self.touch_time = float(line[13])
    self.closest_defender_distance = float(line[16])
    self.possible_points = int(line[17])
    self.actual_points = int(line[20])

  def __str__(self):
    return 'Player: {0} (Period: {1} Clock: {2})'.format(self.player_id, self.period, self.game_clock)

  def __repr__(self):
    return self.__str__()


class NBAPass:
  def __init__(self, from_player_id, to_player_id, period, game_clock):
    self.from_player_id = from_player_id
    self.to_player_id = to_player_id
    self.period = period
    self.game_clock = game_clock

  def __str__(self):
    return 'From: {0} To {1} (Period: {2} Clock: {3})'.format(self.from_player_id, self.to_player_id, self.period, self.game_clock)

  def __repr__(self):
    return self.__str__()


class NBAAssist:
  def __init__(self, nba_pass, shot):
    self.passer_id = nba_pass.from_player_id
    self.shooter_id = nba_pass.to_player_id

    self.touch_time = shot.touch_time
    self.dribbles = shot.dribbles
    self.defender_distance = shot.closest_defender_distance
    self.shot_distance = shot.shot_distance
    self.shot_value = shot.possible_points
    self.made_shot = shot.actual_points > 0

  def __str__(self):
    return 'From: {0} To {1}'.format(self.passer_id, self.shooter_id)

  def __repr__(self):
    return self.__str__()


def load_shots(filenames):
  games_to_shots = {}
  
  for filename in filenames:
    with open(filename, 'rb') as file:
      file.readline()
      for row in file:
        line = row.strip().replace('"','').split('\t')
        game_id = int(line[0])
        games_to_shots.setdefault(game_id, []).append(NBAShot(line))

      for game_id in games_to_shots:
        sorted_shots = sorted(games_to_shots[game_id], key = lambda x: x.game_clock, reverse=True)
        sorted_shots = sorted(sorted_shots, key = lambda x: x.period)
        games_to_shots[game_id] = sorted_shots
  
  return games_to_shots


def load_passes(filenames):
  passes = {}
  
  for filename in filenames:
    with open(filename, 'rb') as file:
      file.readline()
      for row in file:
        row_list = row.strip().replace('"','').split('\t')
        
        game_id = int(row_list[0])
        player_id = int(row_list[1])
        period = int(row_list[5])
        game_clock = float(row_list[7])
        player_type = int(row_list[-1])

        key = (game_id, period, game_clock)
        value = (player_type, player_id)
        
        if player_type == 1 or player_type == 2:
          passes.setdefault(key, []).append(value)

      games_to_passes = {}
      for key in passes:
        if len(passes[key]) != 2: continue
        passer, receiver = sorted(passes[key])
        game_id = key[0]
        games_to_passes.setdefault(game_id, []).append(NBAPass(passer[1], receiver[1], key[1], key[2]))

      for game_id in games_to_passes:
        sorted_passes = sorted(games_to_passes[game_id], key = lambda x: x.game_clock, reverse=True)
        sorted_passes = sorted(sorted_passes, key = lambda x: x.period)
        games_to_passes[game_id] = sorted_passes

  return games_to_passes


def is_assist(nba_pass, shot):
  if nba_pass.period != shot.period: return False
  if nba_pass.to_player_id != shot.player_id: return False
  if nba_pass.game_clock > shot.game_clock + shot.touch_time + 2: return False
  
  #score = -0.2093040*shot.dribbles + -0.5831289*shot.touch_time + 1.9638416
  score = -0.40857009*shot.dribbles + -0.64162386*shot.touch_time + 0.03679159*shot.dribbles*shot.touch_time + 2.15275177
  probability = 1 / (1 + math.exp(-score))

  return probability > 0.5


def load_assists():
  games_to_assists = {}
  games_to_shots = load_shots(shot_filenames)
  games_to_passes = load_passes(pass_filenames)

  game_ids = set(games_to_shots.keys())
  game_ids.intersection_update(games_to_passes.keys()) 
  for game_id in game_ids:
    assists = []
    period = 1
    shots = games_to_shots[game_id]
    passes = games_to_passes[game_id]

    passes_index = 0
    for shot in shots:
      if shot.period != period:
        period = shot.period

      if passes_index == len(passes): break

      while passes[passes_index].period < period:
        passes_index += 1
        if passes_index == len(passes): break

      if passes_index == len(passes): break

      while passes[passes_index].game_clock > shot.game_clock:
        passes_index += 1
        if passes_index == len(passes): break
        if passes[passes_index].period != shot.period: break

      #print shot, '|', passes[passes_index-1], shot.touch_time
      if is_assist(passes[passes_index-1], shot):
        assists.append(NBAAssist(passes[passes_index-1], shot))

    games_to_assists[game_id] = assists

  return games_to_assists

# Maps from game_id to a list of NBAAssist objects.
#pickle.dump(load_assists(), open('assist_data.pkl', 'wb'))


def add_dicts(dict1, dict2):
  if dict1 == None:
    return dict2
  return {key : dict1[key] + dict2[key] for key in dict1}

def average_dicts(dicts):
  size = float(len(dicts))
  avg_dict = { key : 0 for key in dicts[0]}
  for d in dicts:
    for key in d:
      avg_dict[key] += d[key] / size
  return avg_dict

def get_true_assists(sq, assists):
  true_assists = {}
  for assist in assists:
    shot_quality = sq.shot_quality(assist.shooter_id, assist.defender_distance, assist.shot_distance, assist.shot_value)
    stats = {
      'expected_assisted_points' : shot_quality,
      'expected_assists' : shot_quality / assist.shot_value,
      'actual_assisted_points' : assist.shot_value if assist.made_shot else 0,
      'actual_assists' : 1 if assist.made_shot else 0,
    }

    true_assists[assist.passer_id] = add_dicts(true_assists.get(assist.passer_id), stats)
  return true_assists

  


#game_id = 21500001 # Hawks Vs Pistons (October 27th 2015)
#game_id = 21600299
#game_id = 21600122 # John Wall is underrated
#assists = games_to_assists[game_id]


print 'Loading Assist Data...'
games_to_assists = pickle.load(open('assist_data.pkl', 'rb'))
print 'Loading Shot Data...'
sq = ShotQuality()
print 'Loading Player Map...'
player_map, _ = load_player_maps('data/Player_Map.csv')

'''
true_assists = {}
for game_id, assists in games_to_assists.items():
  if not str(game_id).startswith('216'): continue

  print game_id
  for player_id, stat in get_true_assists(sq, assists).items():
    true_assists.setdefault(player_id, []).append(stat)

for player_id in true_assists:
  true_assists[player_id] = average_dicts(true_assists[player_id])

#true_assists = get_true_assists(sq, games_to_assists[21600122])

for player_id, stat in sorted(true_assists.items(), key = lambda x: x[1]['expected_assisted_points']):
  print player_map[player_id], stat

'''

with open('assists.csv', 'wb') as csvfile:
  csv_writer = csv.writer(csvfile)
  csv_writer.writerow(['GAME_ID', 'PLAYER_ID', 'Actual Assists', 'Expected Assists', 'Actual Points from Assists', 'Expected Points from Assists'])
  for game_id, assists in games_to_assists.items():
    print game_id
    for player_id, stats in get_true_assists(sq, assists).items():
      csv_writer.writerow([game_id,
                        player_id,
                        stats['actual_assists'],
                        stats['expected_assists'],
                        stats['actual_assisted_points'],
                        stats['expected_assisted_points']])



