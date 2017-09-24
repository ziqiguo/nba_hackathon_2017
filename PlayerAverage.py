import pandas as pd

shot_log_filename = 'data/Player_Boxscores.csv'
shot_log = pd.read_csv(shot_log_filename)[['Game_id','Person_id','Player_Name','Team_id','Points','Field_Goals_Attempted']]
shot_log = shot_log[shot_log.Game_id.astype(str).str[1:3]=='16']
shot_log['points_per_shot'] = shot_log['Points'] / shot_log['Field_Goals_Attempted']

shot_log['past_mean'] = [None] * shot_log.shape[0]
shot_log['past_std'] = [None] * shot_log.shape[0]
shot_log['rating'] = [None] * shot_log.shape[0]

for row in shot_log.iterrows():
	previous = shot_log[(shot_log.Game_id < row[1].Game_id) & (shot_log.Person_id == row[1].Person_id)]
	print(row[0], previous.shape[0])
	if previous.shape[0] > 0:
		shot_log.loc[row[0], 'past_mean'] = previous.Points.sum() / previous.Field_Goals_Attempted.sum()
		shot_log.loc[row[0], 'past_std'] = previous.points_per_shot.std()
		if shot_log.loc[row[0], 'points_per_shot'] < shot_log.loc[row[0], 'past_mean'] - shot_log.loc[row[0], 'past_std']:
			shot_log.loc[row[0], 'rating'] = -1
		elif shot_log.loc[row[0], 'points_per_shot'] > shot_log.loc[row[0], 'past_mean'] + shot_log.loc[row[0], 'past_std']:
			shot_log.loc[row[0], 'rating'] = 1
		else:
			shot_log.loc[row[0], 'rating'] = 0
	else:
		shot_log.loc[row[0], 'rating'] = 0

print(shot_log.head())
shot_log.to_csv('player_average.csv')

# shot_log = pd.read_csv('player_average.csv')
# import matplotlib.pyplot as plt
# ex = shot_log.Person_id.unique()[0]
# shot_log[shot_log.Person_id == ex].rating.plot()
# plt.show()
