import csv
from nba import NBAPlay
from nba import NBAGame
from nba import NBAPlayer
from nba import NBATeam

data_root_dir = 'data'
GAME_FILE_FORMAT = '%s/Raw Tracking Data/NBA_LG_FINAL_SEQUENCE_OPTICAL${0}_{1}.XML' % data_root_dir

# Returns two maps:
# 1) Maps from regular player id to NBAPlayer objects.
# 2) Maps from SportsVU player id to NBAPlayer objects.
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


# Returns two maps:
# 1) Maps from regular team id to NBATeam objects.
# 2) Maps from SportsVU team id to NBATeam objects.
def load_team_maps(filename):
  team_map = {}
  sv_team_map = {}

  with open(filename, 'rb') as csvfile:
    csv_reader = csv.reader(csvfile)
    csv_reader.next()

    for row in csv_reader:
      sv_team_id = int(row[0])
      team_id = int(row[1])
      conference = row[2]
      city = row[3]
      name = row[4]

      team = NBATeam(team_id, sv_team_id, name, city, conference)

      team_map[team_id] = team
      sv_team_map[sv_team_id] = team

  return team_map, sv_team_map

def load_plays(filename):
  plays = []
  with open(filename, 'rt') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
      plays.append(NBAPlay(row))
  return plays


if __name__ == '__main__':
	player_map, player_svu_map = load_player_maps('%s/Player_Map.csv' % data_root_dir)
	team_map, team_svu_map = load_team_maps('%s/Team_Map.csv' % data_root_dir)

	plays = load_plays('%s/Play_by_Play_New.csv' % data_root_dir)

	game_id = 2016102505
	game = NBAGame(GAME_FILE_FORMAT.format(game_id, 'Q1'), player_svu_map)

	for moment in game.moments[1]:
	  print moment
