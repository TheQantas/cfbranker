from cmath import inf
from math import sqrt
import json
import random
import rank_resources as rr
import time

class Game:
  def __init__(self,game_dict,week) -> None:
    self.dict = game_dict
    self.away_name = game_dict['away_name']
    self.away_id = game_dict['away_id']
    self.home_name = game_dict['home_name']
    self.home_id = game_dict['home_id']
    self.winning_id = game_dict['winning_id']
    self.losing_id = game_dict['losing_id']
    self.winning_score = game_dict['winning_score']
    self.losing_score = game_dict['losing_score']
    self.week_index = week
    self.uid = game_dict['uid']
  def get_team_pt_contribution(self,team_id,coeff_set,year,oppo) -> int:
    did_win_contr = coeff_set.did_win_scalar * ( int(self.did_team_win(team_id)) + coeff_set.did_win_offset )
    diff_contr = coeff_set.pt_diff_scalar * self.get_point_differential(team_id)
    oppo_contr = coeff_set.oppo_pt_scalar * oppo.get_point_value(year,coeff_set)
    record_contr = coeff_set.oppo_record_scalar * oppo.get_record(year)
    return did_win_contr + diff_contr + oppo_contr + record_contr
  #resources
  def did_team_win(self,team_id) -> bool:
    return team_id == self.winning_id
  def get_team_score(self,team_id) -> int:
    return self.winning_score if self.did_team_win(team_id) else self.losing_score
  def get_opponent_id(self,team_id) -> str: #CHECK IF NEEDED
    return self.away_id if self.home_id == team_id else self.home_id
  def get_point_differential(self,team_id) -> int:
    if team_id == self.winning_id:
      return self.winning_score - self.losing_score
    return self.losing_score - self.winning_score
  #class methods
  def copy(self) -> None:
    return Game(self.dict.copy(),self.week)
  def __str__(self) -> str:
    if self.did_team_win(self.away_id):
      return f'{self.winning_score} {self.away_id} @ {self.home_id} {self.losing_score} | wk {self.week_index}'
    return f'{self.losing_score} {self.away_id} @ {self.home_id} {self.winning_score} | wk {self.week_index}'

class Team:
  def __init__(self,team_id,sub,starting_point_values,is_clone) -> None:
    self.team_id = team_id
    self.sub = sub
    self.starting_point_values = starting_point_values
    self.wins = {'2018':0,'2019':0,'2021':0,'2022':0}
    self.losses = {'2018':0,'2019':0,'2021':0,'2022':0}
    self.point_game_contr = {
      '2018': [starting_point_values['2018']],
      '2019': [starting_point_values['2019']],
      '2021': [starting_point_values['2021']],
      '2022': [starting_point_values['2022']]
    }
    self.is_clone = is_clone
  def get_point_value(self,year,coeff_set) -> float:
    point_avg = sum(self.point_game_contr[year]) / len(self.point_game_contr[year])
    return coeff_set.avg_scalar * point_avg - coeff_set.loss_scalar * self.losses[year]
  def add_point_value(self,year,val) -> None:
    if self.is_clone:
      self.point_game_contr[year].append(val)
    else:
      raise Exception('Team is not clone')
  def get_record(self,year) -> float:
    games_played = self.wins[year] + self.losses[year]
    if games_played == 0:
      return 0.5
    return self.wins[year] / games_played
  def add_win(self,year):
    self.wins[year] += 1
  def add_loss(self,year):
    self.losses[year] += 1
  #class methods
  def print_record(self,year) -> str:
    if self.ties[year] != 0:
      return f'({self.wins[year]}-{self.losses[year]}-{self.ties[year]})'
    return f'({self.wins[year]}-{self.losses[year]})'
  def copy(self) -> None:
    return Team(self.team_id,self.sub,self.starting_point_values.copy(),True)
  def __str__(self) -> str:
    return f'Team({self.team_id})'

MINV = 0
MAXV = 3

class CoeffSet:
  def __init__(self,init=False,dict=None) -> None:
    if init:
      self.avg_scalar = random.uniform(MINV,MAXV)
      self.loss_scalar = random.uniform(MINV,MAXV*2)
      self.did_win_scalar = random.uniform(MINV,MAXV)
      self.did_win_offset = random.uniform(MINV,MAXV)
      self.pt_diff_scalar = random.uniform(MINV,MAXV)
      self.oppo_pt_scalar = random.uniform(MINV,MAXV)
      self.oppo_record_scalar = random.uniform(MINV,MAXV)
    else:
      self.avg_scalar = dict['avg_scalar']
      self.loss_scalar = dict['loss_scalar']
      self.did_win_scalar = dict['did_win_scalar']
      self.did_win_offset = dict['did_win_offset']
      self.pt_diff_scalar = dict['pt_diff_scalar']
      self.oppo_pt_scalar = dict['oppo_pt_scalar']
      self.oppo_record_scalar = dict['oppo_record_scalar']
  def get_values_as_dict(self) -> dict:
    return {
      'avg_scalar': self.avg_scalar,
      'loss_scalar': self.loss_scalar,
      'did_win_scalar': self.did_win_scalar,
      'did_win_offset': self.did_win_offset,
      'pt_diff_scalar': self.pt_diff_scalar,
      'oppo_pt_scalar': self.oppo_pt_scalar,
      'oppo_record_scalar': self.oppo_record_scalar
    }

class Model:
  def __init__(self,coeff_set,team_dict,schedule_dict,polls_dict) -> None:
    self.coeff_set = coeff_set
    self.team_dict = team_dict
    self.schedule_dict = schedule_dict
    self.polls_dict = polls_dict
    self.delta_r = 0
  def calc_delta_value(self) -> int:
    for year in ('2018','2019','2021'):
      self.simulate_year(year)
    return self.delta_r
  def simulate_year(self,year,export=False):
    week_number = 1
    for week in self.schedule_dict[year]:
      for game in week:
        self.team_dict[game.winning_id].add_win(year)
        self.team_dict[game.losing_id].add_win(year)
        away_team = self.team_dict[game.away_id]
        home_team = self.team_dict[game.home_id]
        away_pt = game.get_team_pt_contribution(game.away_id,self.coeff_set,year,home_team)
        home_pt = game.get_team_pt_contribution(game.home_id,self.coeff_set,year,away_team)
        away_team.add_point_value(year,away_pt)
        home_team.add_point_value(year,home_pt)
      fbs = []
      fcs = []
      for team_id in self.team_dict: #build fbs and fcs arrays
        team = self.team_dict[team_id]
        if team.sub == 'FBS':
          fbs.append(team)
        elif team.sub == 'FCS':
          fcs.append(team)
      def sorter(team):
        return -team.get_point_value(year,self.coeff_set)
      if week_number <= rr.get_week_limit(year): #can check fbs ranks
        fbs_sorted = sorted(fbs,key=sorter)
        fbs_poll = json.load(open(f'./{year}_fbs_polls/week_{week_number}.json'))
        poll_rank = 1
        for poll_team in fbs_poll: #loop through ranked teams
          model_rank = 1
          delta_team = 30
          for model_team in fbs_sorted: #find rank in model
            if model_team.team_id == poll_team['id']:
              delta_team = abs(poll_rank - model_rank)
              break
            model_rank += 1
          self.delta_r += delta_team ** 2
          poll_rank += 1
        if week_number == 13 and export: #export fbs top 25
          fbs_top_25 = ''
          for i in range(25):
            # fbs_top_25.append({
            #   'rank': i + 1,
            #   'id': fbs_sorted[i].team_id,
            #   'actual': fbs_poll[i]['id']
            # })
            fbs_top_25 += f'{str(i + 1).rjust(2," ")}. {fbs_sorted[i].team_id.ljust(7," ")} (actual {fbs_poll[i]["id"]})\n'
          open(f'./built_rankings/fbs_rankings_{year}.txt','w').write(fbs_top_25)

      if week_number <= 13: #can check fcs ranks
        fcs_sorted = sorted(fcs,key=sorter)
        fcs_poll = json.load(open(f'./{year}_fcs_polls/week_{week_number}.json'))
        poll_rank = 1
        for poll_team in fcs_poll: #loop through ranked teams
          model_rank = 1
          delta_team = 30
          for model_team in fcs_sorted: #find rank in model
            if model_team.team_id == poll_team['id']:
              delta_team = abs(poll_rank - model_rank)
              break
            model_rank += 1
          self.delta_r += delta_team ** 2
          poll_rank += 1
        if week_number == 13 and export: #export fcs top 25
          fcs_top_25 = ''
          for i in range(25):
            # fcs_top_25.append({
            #   'rank': i + 1,
            #   'id': fcs_sorted[i].team_id,
            #   'actual': fcs_poll[i]['id']
            # })
            fcs_top_25 += f'{str(i + 1).rjust(2," ")}. {fcs_sorted[i].team_id.ljust(7," ")} (actual {fcs_poll[i]["id"]})\n'
          open(f'./built_rankings/fcs_rankings_{year}.txt','w').write(fcs_top_25)
      week_number += 1

def main():
  schedules_by_year_and_week = {
    '2018': [],
    '2019': [],
    '2021': [],
    '2022': [],
  }
  polls_by_year_and_week = {
    'fbs_2018': [],
    'fbs_2019': [],
    'fbs_2021': [],
    'fbs_2022': [],
    'fcs_2018': [],
    'fcs_2019': [],
    'fcs_2021': [],
    'fcs_2022': [],
  }
  for year in ('2018','2019','2021','2022'): #build schedules_by_team with Game class objects and polls
    for week in range(rr.get_week_limit(int(year)) + 1):
      week_schedule = json.load(open(f'./{year}_games/week_{week}.json'))
      schedules_by_year_and_week[year].append(list(Game(game,week) for game in week_schedule))
      fbs_poll = json.load(open(f'./{year}_fbs_polls/week_{week}.json'))
      polls_by_year_and_week['fbs_' + year].append(fbs_poll)
      if week <= 13:
        fcs_poll = json.load(open(f'./{year}_fcs_polls/week_{week}.json'))
        polls_by_year_and_week['fcs_' + year].append(fcs_poll)
  team_list = json.load(open('team_list.json','r'))
  master_team_dict = {}
  for team in team_list: #build team dict
    master_team_dict[team['id']] = Team(team['id'],team['subdivision'],team['starting_point_values'],False)
  
  time_taken = []
  last_time = time.time()
  start_time = last_time

  generation_count = 100
  species_count = 100

  best_r_by_gen = []
  advance_gen = 0
  best_model = None
  best_delta_r = inf
  best_three_delta_rs = [inf,inf,inf]
  best_three_models = [None,None,None]
  def get_index_of_nth_best_model(index):
    if len(best_three_delta_rs) != 3:
      raise Exception('WTF')
    max_index = best_three_delta_rs.index(max(best_three_delta_rs))
    min_index = best_three_delta_rs.index(min(best_three_delta_rs))
    if index == 0:
      return min_index
    elif index == 2:
      return max_index
    return 3 - max_index - min_index

  for gen in range(generation_count):
    if gen > 0:
      avg_time_per_gen = sum(time_taken) / len(time_taken)
      time_left = avg_time_per_gen * (generation_count - gen - 1)
      print('starting gen',gen,'advance gen',advance_gen,'-',round(time_left),'secs')
    best_delta_r_of_gen = inf
    best_model_of_gen = None
    for species in range(species_count): #build each individual model
      master_team_dict_copy = {}
      for team_id in master_team_dict:
        master_team_dict_copy[team_id] = master_team_dict[team_id].copy()
      coeff_set = CoeffSet(init=True)
      if gen > 0: #use values based on best 3 overall
        ordered_coeff_set_dicts = [
          best_three_models[ get_index_of_nth_best_model(0) ].coeff_set.get_values_as_dict(),
          best_three_models[ get_index_of_nth_best_model(1) ].coeff_set.get_values_as_dict(),
          best_three_models[ get_index_of_nth_best_model(2) ].coeff_set.get_values_as_dict()
        ]
        max_variance = 0.8 * advance_gen / -8 + 0.9
        if max_variance < 0.1:
          max_variance = 0.1
        def vary():
          return random.random() * max_variance * 2 - max_variance + 1
        test_values_dict = {}
        for val_id in ordered_coeff_set_dicts[0]:
          best_val = ordered_coeff_set_dicts[0][val_id]
          next_val = ordered_coeff_set_dicts[1][val_id]
          worst_val = ordered_coeff_set_dicts[2][val_id]
          new_val = (best_val * 0.6 + next_val * 0.3 + worst_val * 0.1) * vary()
          if new_val > MAXV:
            new_val = MAXV
          elif new_val < -MINV:
            new_val = -MINV
          test_values_dict[val_id] = new_val
        coeff_set = CoeffSet(dict=test_values_dict)
      model = Model(coeff_set,master_team_dict_copy,schedules_by_year_and_week,polls_by_year_and_week)
      model_delta_r = model.calc_delta_value()
      if model_delta_r < best_delta_r_of_gen: #found new best delta of generation
        best_delta_r_of_gen = model_delta_r
        best_model_of_gen = model
      if model_delta_r < max(best_three_delta_rs): #in top 3 overall
        replace_index = get_index_of_nth_best_model(2)
        best_three_delta_rs[replace_index] = model_delta_r
        best_three_models[replace_index] = model
      
    best_r_by_gen.append(best_delta_r_of_gen)
    if best_delta_r_of_gen < best_delta_r: #found new best r overall
      print('new best delta r found on gen',gen)
      advance_gen += 1
      best_delta_r = best_delta_r_of_gen
      best_model = best_model_of_gen
    
    current_time = time.time()
    time_taken.append(current_time - last_time)
    last_time = current_time
  # print('taken',time_taken)
  # print('best overall delta r',best_delta_r)
  exec_time = round(time.time() - start_time)
  ranks_off = round( sqrt(best_delta_r / (29 * 50 * 3)),2 )
  final_coeffs = {
    'model_version': '2.0',
    'delta_r': best_delta_r,
    'delta_r_by_gen': best_r_by_gen,
    'exec_time': exec_time,
    'total_sims': generation_count * species_count,
    'time_per_model': exec_time / (generation_count * species_count),
    'ranks_off': ranks_off,
    'avg_scalar': best_model.coeff_set.avg_scalar,
    'did_win_offset': best_model.coeff_set.did_win_offset,
    'did_win_scalar': best_model.coeff_set.did_win_scalar,
    'loss_scalar': best_model.coeff_set.loss_scalar,
    'oppo_pt_scalar': best_model.coeff_set.oppo_pt_scalar,
    'oppo_record_scalar': best_model.coeff_set.oppo_record_scalar,
    'pt_diff_scalar': best_model.coeff_set.pt_diff_scalar
  }
  json.dump(final_coeffs,open(f'./coeffs/{round(time.time())}.json','w'))
  best_model.simulate_year('2018',True)
  best_model.simulate_year('2019',True)
  best_model.simulate_year('2021',True)

main()