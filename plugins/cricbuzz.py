from bs4 import BeautifulSoup
from requests import get
import re
from logging import debug

from core import action

url = 'https://m.cricbuzz.com'
response = get(url)
MATCHHEADER_SPLIT = '\xa0•&nbsp'
SCORE_SPLIT = ' '
r_score_pattern = re.compile(r'^(\w+(?: \w+)*?)(?: (\d+)(?:\/(\d+))?(?: d)?(?: d?\((\d+.?\d?)\))?)?(?: & (\d+)(?:\/(\d+))?(?: d)? d?\((\d+.?\d?)\))?$')

@action("cricket-score")
def cricket_score(params, variables):
  res = extractor()
  debug(res)
  if "filters" in params:
	  filters = params["filters"]
  else:
	  filters={}
  variables["score"] = filter_matches(filters, res)
  variables["status"] = "ok"
  return "ok"
  
def extractor():
	scores = []
	html_soup = BeautifulSoup(response.text, 'html.parser')
	match_list = html_soup.find('div',class_ = 'list-group')
	matches = match_list.find_all('a', class_ = 'cb-list-item')
	for match in matches:
		result = {}
		matchheader = match.find('div', class_ = 'matchheader').text.split(MATCHHEADER_SPLIT)
		team1 = parse_score(match.find('span', class_ = 'bat-team-scores').text)
		team2 = parse_score(match.find('span', class_ = 'bat-team-scores-test').text)
		summary = match.find('span', class_ = 'cbz-ui-home').text
		
		result['tournament'] = matchheader[1]
		result['tournament_match'] = matchheader[0]
		result['teams'] = [team1['team'],team2['team']]
		result['scores'] = [team1,team2] 
		result['summary'] = summary

		scores.append(result)
	return scores

def filter_matches(filters_array, matches):
	for filter_str in filters_array:
		matches = apply_filter(filter_str, matches)
	return matches

def apply_filter(string, matches):
	tokens = string.split(';')
	debug(tokens)
	if tokens[0] == "tournament":
		return list(filter(lambda a: tokens[1] in a['tournament'], matches))
	if tokens[0] == "team":
		return list(filter(lambda a: tokens[1] in a['teams'], matches))
	if tokens[0] == "limit":
		return matches[:int(tokens[1])]

def get_string(match_dict):
	str_arr = []
	str_arr.append(match_dict["tournament"] + ', ' + match_dict["tournament_match"])
	for score in match_dict['scores']:
		if "runs" in score:
			str_arr.append(score['team'] + ' ' + score['runs'] + '/' + score['wickets'] + ' (' + score['overs'] + '), RR: ' + str(run_rate(score['runs'],score['overs'])))
		if "runs2" in score:
			str_arr.append(score['team'] + ' ' + score['runs2'] + '/' + score['wickets2'] + ' (' + score['overs2'] + '), RR: ' + str(run_rate(score['runs2'],score['overs2'])))
		else:
			str_arr.append(score['team'])
	str_arr.append(match_dict['summary'])
	return '\n'.join(str_arr)

def run_rate(runs, overs):
	if overs == "NA":
		return 0
	balls = overs.split('.')
	if len(balls) > 1:
		balls_delta =  float(balls[1])  / 6
	else:
		balls_delta = 0
	run_rate = float(runs)  / (float(balls[0]) + balls_delta)
	return round(run_rate, 2)

def parse_score(string):
	debug(string)
	score = {}
	grp = r_score_pattern.match(string).groups()
	debug(grp)
	score['team'] = grp[0]
	if grp[1]:
		score['runs'] = grp[1]
		if grp[3]:
			score['overs'] = grp[3]
		else:
			score['overs'] = "NA"
		if grp[2]:
			score['wickets'] = grp[2]
		else:
			score['wickets'] = "10"
	if grp[4]:
		score['runs2'] = grp[4]
		if grp[6]:
			score['overs2'] = grp[6]
		else:
			score['overs2'] = "NA"
		if grp[5]:
			score['wickets2'] = grp[5]
		else:
			score['wickets2'] = "10"
	return score

