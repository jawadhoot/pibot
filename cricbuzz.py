from bs4 import BeautifulSoup
from requests import get
import re

url = 'https://m.cricbuzz.com'
response = get(url)
MATCHHEADER_SPLIT = '\xa0•&nbsp'
SCORE_SPLIT = ' '
r_score_pattern = re.compile(r'^(\w+(?: \w+)*)(?: (\d+)\/?(\d+)? \((\d+.?\d+?)\))?$')


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
		result['tornament_match'] = matchheader[0]
		result['teams'] = [team1['team'],team2['team']]
		result['scores'] = [team1,team2] 
		result['summary'] = summary

		scores.append(result)
	return scores

def filter():
	pass

def xmpp_transform():
	pass

def parse_score(string):
	print(string)
	score = {}
	grp = r_score_pattern.findall(string)[0]
	score['team'] = grp[0]
	if grp[1]:
		score['runs'] = grp[1]
		score['overs'] = grp[3]
		if grp[2]:
			score['wickets'] = grp[2]
		else:
			score['wickets'] = 10
	return score

if __name__ == "__main__":
	print(extractor())
	#print(parse_score("SRH 121/5 (14.1)"))
	#print(parse_score("Kings 11 Punjab"))