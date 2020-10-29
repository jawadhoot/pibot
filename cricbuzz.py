from bs4 import BeautifulSoup
from requests import get

url = 'https://m.cricbuzz.com'
response = get(url)

def extractor():
	responses = []
	html_soup = BeautifulSoup(response.text, 'html.parser')
	matches = html_soup.find_all('a', class_ = 'cb-list-item')
	for match in matches[:2]:
		result = []
		result.append(match.find('span', class_ = 'bat-team-scores').text)
		result.append(match.find('span', class_ = 'bat-team-scores-test').text)
		result.append(match.find('span', class_ = 'cbz-ui-home').text)
		responses.append(';'.join(result))
	return '\n'.join(responses)	

