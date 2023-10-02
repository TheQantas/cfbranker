import requests
from bs4 import BeautifulSoup
import json
import rank_resources as rr

def parse_table(table) -> list:
  def remove_rank(name) -> str:
    final_name = ''
    for char in name:
      if char not in ('0','1','2','3','4','5','6','7','8','9'):
        final_name += char
    return final_name.strip()
  matches = []
  rows = table.find('tbody').find_all('tr')
  def get_team_id(cell):
    try:
      link = cell.find('a')['href']
      return link.split('/')[3]
    except:
      return 'PLACEHOLDER'
  for row in rows:
    cells = row.find_all('td')
    away_id = get_team_id(cells[0])
    home_id = get_team_id(cells[1])
    
    away_team_name = remove_rank( cells[0].get_text().replace('\n','').replace('\t','').strip() )
    while '  ' in away_team_name:
      away_team_name = away_team_name.replace('  ',' ')
    home_team_name = remove_rank( cells[1].get_text().replace('\n','').replace('\t','').strip() )
    while '  ' in home_team_name:
      home_team_name = home_team_name.replace('  ',' ')
    status_text = cells[2].get_text().replace(',','').strip()
    if status_text == 'Postponed' or status_text == 'Cancelled':
      continue
    score_list = status_text.split(' ')
    if score_list[2] != '-':
      score_list = score_list[0:2] + ['-'] + score_list[2:]
    winning_id = score_list[0]
    losing_id = score_list[3]
    try:
      if ',' not in status_text:
        winning_score = int(score_list[1])
        losing_score = int(score_list[4])
    except:
      print(away_id,home_id,cells[2].get_text().strip(),status_text)
      raise Exception('WTF')
    matches.append({
      'away_name': away_team_name,
      'away_id': away_id,
      'home_name': home_team_name,
      'home_id': home_id,
      'winning_id': winning_id,
      'losing_id': losing_id,
      'winning_score': winning_score,
      'losing_score': losing_score,
      'uid': away_id + '@' + home_id
    })
  return matches

def get_week_of_year(year,week_number):
  week_matches = []
  week_uids = []
  schedule_fbs_html = requests.get(f'https://www.cbssports.com/college-football/schedule/FBS/{year}/regular/{week_number}/')
  schedule_fbs_soup = BeautifulSoup(schedule_fbs_html.content,'html.parser')
  fbs_tables = schedule_fbs_soup.find_all('table',{'class':'TableBase-table'})
  schedule_fcs_html = requests.get(f'https://www.cbssports.com/college-football/schedule/fcs/{year}/regular/{week_number}/')
  schedule_fcs_soup = BeautifulSoup(schedule_fcs_html.content,'html.parser')
  fcs_tables = schedule_fcs_soup.find_all('table',{'class':'TableBase-table'})
  for table in fbs_tables + fcs_tables:
    table_matches = parse_table(table)
    for match in table_matches:
      if match['uid'] not in week_uids: #unique game
        week_uids.append(match['uid'])
        week_matches.append(match)
  export_file = open(f'./{year}_games/week_{week_number}.json','w')
  json.dump(week_matches,export_file)

def main():
  # get_week_of_year(2019,9)
  for year in (2019,2021):
    for week_index in range(rr.get_week_limit(year)):
      get_week_of_year(year,week_index + 1)

main()