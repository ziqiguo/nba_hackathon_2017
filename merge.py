import csv

data = {}

with open('assists.csv', 'rU') as csvfile:
	csv_reader = csv.reader(csvfile)
	csv_reader.next()

	for row in csv_reader:
		key = (int(row[0]), int(row[2]))
		data[key] = [row[1]] + row[3:]

with open('shot_quality_season.csv', 'rU') as csvfile:
	csv_reader = csv.reader(csvfile)
	csv_reader.next()

	for row in csv_reader:
		key = (int(row[0]), int(row[1]))
		if key in data:
			data[key].extend([row[4], row[3]])

with open('shot_and_assist_data.csv', 'wb') as csvfile:
	csv_writer = csv.writer(csvfile)
	csv_writer.writerow(['GAME_ID', 'PLAYER_ID', 'TEAM_ID', 'Actual Assists', 'Expected Assists', 'Actual Points from Assists', 'Expected Points from Assists', 'Actual Points', 'Expected Points'])

	for key, value in data.items():
		csv_writer.writerow(list(key) + value)

