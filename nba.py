import xml.etree.ElementTree as ET
# Note: You can load a game from the file by passing in the game_id.
# 
# Fields:
#  - self.date : Calendar date of the game (e.g. 2017-25-12).
#  - self.stadium : Name of the stadium the game took place in (e.g. ORACLE Arena).
#  - self.home_sv_team_id / self.away_sv_team_id : SportsVU team ids for each team.
#  - self.home_team_scores / self.away_team_scores : Array of scores by quarter (including OT).
#  - self.moments : Map from quarter number (1-4 or 5/6 if game went into OT) to arrays of
#           NBAMoment objects for each moment in that period.
class NBAGame:
  def __init__(self, file_path, player_svu_map):
    root = ET.parse(file_path).getroot()
    
    boxscore = root.find('sports-boxscores/nba-boxscores/nba-boxscore')
    date_tag = boxscore.find('date').attrib
    self.date = "{0}-{1}-{2}".format(date_tag['year'],
                     date_tag['month'],
                     date_tag['date'])
    self.stadium = boxscore.find('stadium').attrib['name']

    home_team_tag = boxscore.find('home-team')
    away_team_tag = boxscore.find('visiting-team')
    self.home_sv_team_id = home_team_tag.find('team-code').attrib['id']
    self.away_sv_team_id = away_team_tag.find('team-code').attrib['id']

    self.home_scores = [int(q.attrib['score']) for q in home_team_tag.iter('quarter')]
    self.away_scores = [int(q.attrib['score']) for q in away_team_tag.iter('quarter')]

    self.moments = {}
    for quarter in range(1, len(self.home_scores) + 1):
      quarter_label = 'Q{0}'.format(quarter) if quarter <= 4 else 'OT{0}'.format(quarter-4)
      root = ET.parse(file_path.replace('Q1', quarter_label)).getroot()
      sequences = root.find('sports-boxscores/nba-boxscores/nba-boxscore/sequences')
      self.moments[quarter] = [NBAMoment(tag, self.home_sv_team_id, self.away_sv_team_id, player_svu_map) for tag in sequences.iter('moment')]

# Fields:
#  - self.team_id : Regular id for the team.
#  - self.sv_team_id : SportsVU id for the team.
#  - self.name : Team name (e.g. Cavaliers).
#  - self.city : Team city (e.g. Cleveland).
#  - self.conference : East or West.
#  - self.players : Map from SportsVU player ids to NBAPlayer objects.
class NBATeam:
  def __init__(self, team_id, sv_team_id, name, city, conference):
    self.team_id = team_id
    self.sv_team_id = sv_team_id
    self.name = name
    self.city = city
    self.conference = conference

  def __str__(self):
    return '{0} {1}'.format(self.city, self.name)

  def __repr__(self):
    return self.__str__()

# Fields:
#  - self.name : Name of the player (e.g. Lebron James).
#  - self.player_id : Regular id for the player.
#  - self.sv_player_id : SportsVU id for the player.
class NBAPlayer:
  def __init__(self, name, player_id, sv_player_id):
    self.name = name
    self.player_id = player_id
    self.sv_player_id = sv_player_id

  def __str__(self):
    return self.name

  def __repr__(self):
    return self.__str__()

# Fields:
#  - self.game_clock : Number of seconds left in the period (float value).
#  - self.shot_clock : Number of seconds left on the shot clock (float value).
#  - self.ball_location : (x, y, z) tuple for the ball location.
#  - self.home_team_locations : Map from sv_player_ids to (x, y, z) tuples for
#                 home team player locations.
#  - self.away_team_locations : Map from sv_player_ids to (x, y, z) tuples for
#                 away team player locations.
class NBAMoment:
  def __init__(self, tag, sv_home_team_id, sv_away_team_id, player_svu_map):
    self.game_clock = float(tag.attrib['game-clock'])
    self.shot_clock = None if tag.attrib['shot-clock'] == '' else float(tag.attrib['shot-clock'])

    location_strings = tag.attrib['locations'].split(';')
    split_string = location_strings[0].split(',')
    self.ball_location = (float(split_string[2]), float(split_string[3]), float(split_string[4]))
    self.home_team_locations = {}
    self.away_team_locations = {}
    for location_string in location_strings[1:]:
      split_string = location_string.split(',')
      team_id = split_string[0]
      sv_player_id = int(split_string[1])
      player = player_svu_map.get(sv_player_id)
      if player == None:
        player = sv_player_id
      location = (float(split_string[2]), float(split_string[3]), float(split_string[4]))

      if team_id == sv_home_team_id:
        self.home_team_locations[player] = location
      if team_id == sv_away_team_id:
        self.away_team_locations[player] = location

  def __str__(self):
    return str(vars(self))

  def __repr__(self):
    return self.__str__()

class NBAPlay:
  def __init__(self, attributes):
    self.game_id = attributes[0]
    self.season = attributes[1]
    self.season_type = attributes[2]
    self.game_no = attributes[3]
    self.playoff_rd = attributes[4]
    self.playoff_rd_game_no = attributes[5]
    self.date = attributes[6]
    self.home_team_id = attributes[7]
    self.visitor_team_id = attributes[9]
    self.period = attributes[11]
    self.event_num = attributes[12]
    self.wall_clock_time = attributes[13]
    self.play_clock_time = attributes[14]
    self.team_committing_action = attributes[15]
    self.people = attributes[16:18]
    self.home_pts = attributes[19]
    self.visitor_pts = attributes[20]
    self.x_location = attributes[21]
    self.y_location = attributes[22]
    self.description = attributes[23]
    self.rebound_designation = attributes[24]
    self.shot_value = attributes[25]
    self.shot_outcome = attributes[26]
    self.shot_side_of_ct = attributes[27]
    self.shot_distance = attributes[28]
    self.general_description = attributes[29]
    self.players = attributes[30:]

  def __str__(self):
    return str(vars(self))

  def __repr__(self):
    return self.__str__()
