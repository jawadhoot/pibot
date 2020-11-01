from bs4 import BeautifulSoup
from requests import get

url = 'https://m.cricbuzz.com'
response = get(url)
MATCHHEADER_SPLIT = '\xa0•&nbsp'
SCORE_SPLIT = ' '

def extractor():
	scores = []
	html_soup = BeautifulSoup(response.text, 'html.parser')
	match_list = html_soup.find('div',class_ = 'list-group')
	matches = match_list.find_all('a', class_ = 'cb-list-item')
	for match in matches:
		result = {}
		matchheader = match.find('div', class_ = 'matchheader').text.split(MATCHHEADER_SPLIT)
		team1 = match.find('span', class_ = 'bat-team-scores').text
		team2 = match.find('span', class_ = 'bat-team-scores-test').text
		summary = match.find('span', class_ = 'cbz-ui-home').text
		
		result['tournament'] = matchheader[1]
		result['tornament_match'] = matchheader[0]
		result['teams'] = [team1.split(SCORE_SPLIT)[0],team2.split(SCORE_SPLIT)[0]] 
		result['team1-score'] = team1
		result['team2-score'] = team2
		result['summary'] = summary

		scores.append(result)
	return scores

def filter():
	pass

def xmpp_transform():
	pass

if __name__ == "__main__":
	print(extractor())