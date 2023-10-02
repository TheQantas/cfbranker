import csv
import json

def main():
  team_list = json.load(open('team_list_old.json'))
  csv_polls = {
    '2018': csv.reader(open('./fcs_csv/2018_polls.csv')),
    '2019': csv.reader(open('./fcs_csv/2019_polls.csv')),
    '2021': csv.reader(open('./fcs_csv/2021_polls.csv')),
    '2022': csv.reader(open('./fcs_csv/2022_polls.csv'))
  }
  def get_team_id(name) -> str:
    for team in team_list:
      if team['name'] == name or team['name'].replace('St.','State') == name:
        return team['id']
    if name == 'North Dakota State':
      return 'NDST'
    if name == 'Eastern Washington':
      return 'EWASH'
    if name == 'South Dakota State':
      return 'SDST'
    if name == 'Sam Houston State':
      return 'SAMST'
    if name == 'North Carolina A&T':
      return 'NCAT'
    if name == 'Nicholls':
      return 'NICHST'
    if name == 'Northern Iowa':
      return 'NOIOWA'
    if name == 'Central Arkansas':
      return 'CAR'
    if name == 'Southeast Missouri State':
      return 'SEMOST'
    if name == 'East Tennessee State':
      return 'ETSU'
    if name == 'Youngstown State':
      return 'YST'
    if name == 'Northern Arizona':
      return 'NAU'
    if name == 'Central Connecticut':
      return 'CCTST'
    if name == 'Southeastern Louisiana':
      return 'SELOU'
    if name == 'Southern Illinois':
      return 'SIL'
    if name == 'VMI':
      return 'VMI'
    if name == 'Stephen F. Austin':
      return 'SFA'
    if name == 'Eastern Kentucky':
      return 'EKY'
    if len(name) > 0:
      print('no id for',name)
    return '__' + name.upper().replace(' ','')
  polls = {}
  for year in ('2022','x'):
    poll = csv_polls[year]
    rank = 0
    for raw_rank_row in poll:
      rank_row = raw_rank_row[1:-1]
      for week in range(len(rank_row)):
        raw_team_name = rank_row[week]
        team_name = ''
        key = year + '_week_' + str(week)
        if key not in polls:
          polls[key] = []
        for char in raw_team_name:
          if char == '(':
            break
          if char not in ('0','1','2','3','4','5','6','7','8','9','?'):
            team_name += char
        team_name = team_name.strip()
        polls[key].append({
          'name': team_name,
          'id': get_team_id(team_name),
          'rank': rank + 1
        })
      rank += 1
    break
  for key in polls:
    key_list = key.split('_')
    file_path = f'./{key_list[0]}_fcs_polls/week_{key_list[2]}.json'
    json.dump(polls[key],open(file_path,'w'))


main()