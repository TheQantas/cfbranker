import time
import json

def get_week_limit(year) -> int:
  if type(year) is str:
    year = int(year)
  if year == 2019:
    return 16
  elif year == 2021 or year == 2018:
    return 15
  return 1 #2022

def get_week() -> int:
  raw_week = int(time.strftime('%U'))
  if raw_week < 20:
    raise Exception('Check rank_resources.get_week')
  raw_day = int(time.strftime('%w'))
  week_offset = 0 if raw_day < 3 else 1
  return (raw_week + week_offset) - 35

def get_all_team_schedules(year) -> dict:
  schedules_by_team_id = {}
  week_limit = get_week_limit(year)
  for week_index in range(week_limit):
    game_list = json.load(open(f'./games/{year}_week_{week_index + 1}.json'))
    for game in game_list:
      if game['away_id'] not in schedules_by_team_id:
        schedules_by_team_id[game['away_id']] = []
      if game['home_id'] not in schedules_by_team_id:
        schedules_by_team_id[game['home_id']] = []
      schedules_by_team_id[game['away_id']].append(game)
      schedules_by_team_id[game['home_id']].append(game)
  return schedules_by_team_id