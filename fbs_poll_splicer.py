import requests
from bs4 import BeautifulSoup
import json

def convert_ap_to_pts(ap) -> float:
  return 0.0178571428571 * ap + 61.4285714286

bounds = {
  '2018': (1136,1151),
  '2019': (1152,1168),
  '2021': (1186,1201),
  '2022': (1202,1203)
}

def main():
  team_list = json.load(open('team_list_old.json'))
  def get_team_id(name) -> str:
    for team in team_list:
      if team['name'] == name or team['name'].replace('St.','State') == name:
        return team['id']
    if name == 'Florida Atlantic':
      return 'FAU'
    elif name == 'Miami (FL)':
      return 'MIAMI'
    elif name == 'Appalachian State':
      return 'APLST'
    elif name == 'California':
      return 'CAL'
    elif name == 'South Florida':
      return 'USF'
    elif name == 'Georgia Southern':
      return 'GAS'
    elif name == 'Mississippi':
      return 'MISS'
    elif name == 'North Dakota State':
      return 'NDST'
    elif name == 'Western Michigan':
      return 'WMICH'
    elif name == 'Northern Illinois':
      return 'NIL'
    print('no id for',name)
    return '__' + name.upper().replace(' ','')
  for year in (2018,2019,2021,2022):
    year_bounds = bounds[str(year)]
    week = 0
    for poll_id in range(year_bounds[0],year_bounds[1] + 1):
      polls_by_year = []
      poll_html = requests.get(f'https://collegepollarchive.com/football/ap/seasons.cfm?appollid={poll_id}')
      poll_soup = BeautifulSoup(poll_html.content,'html.parser')
      table = poll_soup.find('table').find('tbody')
      rows = table.find_all('tr')
      for row in rows:
        cells = row.find_all('td')
        rank = cells[0].get_text()
        if rank == 'NR': #team is not ranked
          continue
        name = cells[3].find('a').get_text()
        pts = int(cells[6].get_text())
        id = get_team_id(name)
        polls_by_year.append({
          'id': id,
          'name': name,
          'raw_pts': pts,
          'pts': convert_ap_to_pts(pts)
        })
      export_file = open(f'./{year}_fbs_polls/week_{week}.json','w')
      json.dump(polls_by_year,export_file)
      week += 1

main()