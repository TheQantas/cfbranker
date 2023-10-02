import json
import rank_resources as rr

def main():
  for year in ('2018','2019','2021','2022'):
    for week in range(rr.get_week_limit(year) + 1):
      game_list = json.load(open(f'./{year}_games/week_{week}.json'))
      for game in game_list:
        if game['winning_score'] == game['losing_score']:
          print(game)

main()