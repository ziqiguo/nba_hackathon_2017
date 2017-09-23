import csv, sys

def read_csv(filename):
  rows = []
  with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
      rows.append(row)
  return rows

def get_game_id(team1, team2, date):
  potential_games = []
  for row in read_csv('data/Game_Map.csv'):
    if row[2] == date:
      potential_games.append(row[0])
  boxscores = read_csv('data/Player_Boxscores.csv')
  boxscores = [score for score in boxscores if score[0] in potential_games]
  for row in boxscores:
    if row[10] == team1 or row[10] == team2:
      return row[0]

if len(sys.argv) != 4:
  print 'usage: python get_game_id.py <team-abbrev-1> <team-abbrev-2> <date>'
  sys.exit(1)
print get_game_id(sys.argv[1], sys.argv[2], sys.argv[3])
