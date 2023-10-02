import json

def main():
  orig_team_list = json.load(open('team_list_old.json'))
  preseason_polls = {
    'fbs_2018': json.load(open('./2018_fbs_polls/week_0.json')),
    'fbs_2019': json.load(open('./2019_fbs_polls/week_0.json')),
    'fbs_2021': json.load(open('./2021_fbs_polls/week_0.json')),
    'fbs_2022': json.load(open('./2022_fbs_polls/week_0.json')),
    'fcs_2018': json.load(open('./2018_fcs_polls/week_0.json')),
    'fcs_2019': json.load(open('./2019_fcs_polls/week_0.json')),
    'fcs_2021': json.load(open('./2021_fcs_polls/week_0.json')),
    'fcs_2022': json.load(open('./2022_fcs_polls/week_0.json')),
  }
  def fbs_to_pts(ap) -> float:
    return round(0.175438596491 * ap + 723.684210526,2)
  def fcs_to_pts(ap) -> float:
    return round(-6.25 * ap + 406.25,2)
  def get_normal_conf_name(full_conf):
    return {
      'Pacific-12 Conference': 'Pac-12',
      'American Athletic Conference': 'AAC',
      'Mountain West Conference': 'MW',
      'Atlantic Coast Conference': 'ACC',
      'Big Ten Conference': 'Big Ten',
      'Big 12 Conference': 'Big 12',
      'Southeastern Conference': 'SEC',
      'Western Athletic Conference': 'WAC',
      'Southwestern Athletic Conference': 'SWAC',
      'Sun Belt Conference': 'Sun Belt',
      'Ohio Valley Conference': 'Ohio Valley',
      'Mid-American Conference': 'MAC',
      'Independent': 'Independent',
      'Ivy League': 'Ivy League',
      'Northeast Conference': 'NEC',
      'Patriot League': 'Patriot League',
      'Big East Conference': 'Big East',
      'Big West Conference': 'BWC',
      'Big Sky Conference': 'BSC',
      'Big South Conference': 'Big South',
      'Atlantic 10 Conference': 'A-10',
      'Mid-Eastern Athletic Conference': 'MEAC',
      'Missouri Valley Conference': 'MVC',
      'Southern Conference': 'SoCon',
      'ASUN Conference': 'ASUN',
      'Colonial Athletic Association': 'CAA',
      'Conference USA': 'C-USA',
      'Southland Conference': 'Southland',
      'Metro Atlantic Athletic Conference': 'MAAC',
      'Northeast-10 Conference': 'NE-10',
      'The Summit League': 'The Summit',
      'Horizon League': 'Horizon',
      'America East Conference': 'America East',
      'West Coast Conference': 'WCC',
      'Mid-South': 'MSC',
      'Gulf South': 'GSC',
      'Southern Intercollegiate Athletic Conference': 'SIAC',
      'Central Intercollegiate Athletic Association': 'CIAA',
      'Great Lakes Valley Conference': 'GLVC',
      'Rocky Mountain Athletic Conference': 'RMAC',
      'Pioneer Football League': 'PFL',
      'Pennsylvania State Athletic Conference': 'PSAC',
      'Lone Star Conference': 'LSC',
      'South Atlantic Conference': 'SAC',
      'USA South Athletic Conference': 'USA South',
      'Appalachian Athletic Conference': 'App Ath Conf',
      'Chicagoland Collegiate Athletic Conference': 'CCAC',
      'Mid-America Intercollegiate Athletics Association': 'MIAA',
      'National Christian College Athletic Association': 'NCCAA',
      'Heartland Collegiate Athletic Conference': 'HCAC',
      'North Star Athletic Association': 'NSAA',
      'Crossroads League': 'Crossroads',
      'Red River Athletic Conference': 'RRAC',
      'Old Dominion Athletic Conference': 'ODAC',
      'Frontier Conference': 'Frontier',
      'Sooner Athletic Conference': 'Sooner',
      'Pacific West Conference': 'PacWest',
      'Mountain East Conference': 'MEC',
      'Eastern Collegiate Football Conference': 'ECFC',
      'Cascade Collegiate Conference': 'CCC',
      'Great Midwest Athletic Conference': 'G-MAC',
      'Ohio Valley Conference': 'OVC',
      'Great Northwest Athletic Conference': 'GNAC',
      'Mid-States Football Association': 'MSFA',
      'New England Women\'s and Men\'s Athletic Conference': 'NEWMAC',
      'Commonwealth Coast Football': 'CCF',
      'The Sun Conference': 'The Sun',
      'Great Lakes Intercollegiate Athletic Conference': 'GLIAC',
      'North Coast Athletic Conference': 'NCAC'
    }[full_conf]
  def get_default_point_value(team_id,conf,div):
    if conf in ('ACC','Big Ten','Big 12','SEC') or team_id in ('ND','BYU'):
      return 700
    elif conf in ('Pac-12'):
      return 650
    elif conf in ('AAC'):
      return 550
    elif conf in ('MW'):
      return 500
    elif div == 'FBS':
      return 400
    elif conf in ('BSC','MVC','CAA'):
      return 200
    elif div == 'FCS':
      return 150
    elif div == 'Div II':
      return 50
    return 0 #naia,div iii
  def get_preseason_value(team) -> dict:
    team_id = team['id']
    ap_points_2018 = -1
    ap_points_2019 = -1
    ap_points_2021 = -1
    ap_points_2022 = -1
    for place in preseason_polls['fbs_2018']: #find 2018 fbs value
      if place['id'] == team_id:
        ap_points_2018 = fbs_to_pts(place['raw_pts'])
        break
    for place in preseason_polls['fbs_2019']: #find 2019 fbs value
      if place['id'] == team_id:
        ap_points_2019 = fbs_to_pts(place['raw_pts'])
        break
    for place in preseason_polls['fbs_2021']: #find 2021 fbs value
      if place['id'] == team_id:
        ap_points_2021 = fbs_to_pts(place['raw_pts'])
        break
    for place in preseason_polls['fbs_2022']: #find 2022 fbs value
      if place['id'] == team_id:
        ap_points_2022 = fbs_to_pts(place['raw_pts'])
        break
    for place in preseason_polls['fcs_2018']: #find 2018 fcs value
      if place['id'] == team_id:
        ap_points_2018 = fcs_to_pts(place['rank'])
        break
    for place in preseason_polls['fcs_2019']: #find 2019 fcs value
      if place['id'] == team_id:
        ap_points_2019 = fcs_to_pts(place['rank'])
        break
    for place in preseason_polls['fcs_2021']: #find 2021 fcs value
      if place['id'] == team_id:
        ap_points_2021 = fcs_to_pts(place['rank'])
        break
    for place in preseason_polls['fcs_2022']: #find 2022 fcs value
      if place['id'] == team_id:
        ap_points_2022 = fcs_to_pts(place['rank'])
        break
    conf = team['conf']
    div = team['subdivision']
    default_point = get_default_point_value(team_id,conf,div)
    if ap_points_2018 == -1:
      ap_points_2018 = default_point
    if ap_points_2019 == -1:
      ap_points_2019 = default_point
    if ap_points_2021 == -1:
      ap_points_2021 = default_point
    if ap_points_2022 == -1:
      ap_points_2022 = default_point
    return {
      '2018': ap_points_2018,
      '2019': ap_points_2019,
      '2021': ap_points_2021,
      '2022': ap_points_2022
    }
  spliced_teams = []
  for team in orig_team_list:
    del team['starting_points']
    team['full_conf'] = team['conf']
    team['conf'] = get_normal_conf_name(team['conf'])
    point_values = get_preseason_value(team)
    team['starting_point_values'] = {
      '2018': point_values['2018'],
      '2019': point_values['2019'],
      '2021': point_values['2021'],
      '2022': point_values['2022'],
    }
    spliced_teams.append(team)
  json.dump(spliced_teams,open('team_list.json','w'))

main()