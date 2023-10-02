import json

def main():
  import_file = open('teams_raw.txt','r')
  lines = import_file.readlines()
  team_list = []
  for line_index in range(int((len(lines) + 1) / 9)):
    team_name = lines[line_index * 9].replace('\n','')
    conference = lines[line_index * 9 + 4].replace('\n','')
    subdivision = lines[line_index * 9 + 5].replace('\n','')
    team_id = lines[line_index * 9 + 6].replace('\n','')
    try:
      points = int( lines[line_index * 9 + 7] )
    except:
      points = float( lines[line_index * 9 + 7] )
    team_list.append({
      'name': team_name,
      'id': team_id,
      'conf': conference,
      'subdivision': subdivision,
      'starting_points': points
    })
  export_file = open('team_list.json','w')
  json.dump(team_list,export_file)

main()