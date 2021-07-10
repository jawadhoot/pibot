import pytest
from plugins import cricbuzz

matches = [
  {'tournament': 'Pakistan tour of England, 2021', 'tournament_match': '2nd ODI', 'teams': ['ENG', 'PAK'], 'scores': [{'team': 'ENG', 'runs': '63', 'overs': '9', 'wickets': '2'}, {'team': 'PAK'}], 'summary': 'Match reduced to 47 overs per side due to rain'},
  {'tournament': 'Bangladesh tour of Zimbabwe, 2021', 'tournament_match': 'Only Test', 'teams': ['ZIM', 'BAN'], 'scores': [{'team': 'ZIM', 'runs': '276', 'overs': 'NA', 'wickets': '10', 'runs2': '25', 'overs2': '9', 'wickets2': '1'}, {'team': 'BAN', 'runs': '468', 'overs': 'NA', 'wickets': '10', 'runs2': '284', 'overs2': '67.4', 'wickets2': '1'}], 'summary': 'Day 4: Tea Break - Zimbabwe need 452 runs'},
  {'tournament': 'Australia tour of West Indies, 2021', 'tournament_match': '1st T20I', 'teams': ['WI', 'AUS'], 'scores': [{'team': 'WI', 'runs': '145', 'overs': '20', 'wickets': '6'}, {'team': 'AUS', 'runs': '127', 'overs': '16', 'wickets': '10'}], 'summary': 'West Indies won by 18 runs'},
  {'tournament': 'Australia tour of West Indies, 2021', 'tournament_match': '2st T20I', 'teams': ['WI', 'AUS'], 'scores': [{'team': 'WI', 'runs': '145', 'overs': '20', 'wickets': '6'}, {'team': 'AUS', 'runs': '127', 'overs': '16', 'wickets': '10'}], 'summary': 'West Indies won by 18 runs'}
]

match_string = """Bangladesh tour of Zimbabwe, 2021, Only Test
ZIM 276/10 (NA), RR: 0
ZIM 25/1 (9), RR: 2.78
BAN 468/10 (NA), RR: 0
BAN 284/1 (67.4), RR: 4.2
Day 4: Tea Break - Zimbabwe need 452 runs"""

def test_extractor():
  res = cricbuzz.extractor()
  print(res)
  assert res

def test_filters_tournament():
  filter_array = ["tournament;Pakistan tour of England"]
  c = cricbuzz.filter_matches(filter_array, matches)
  assert  1 == len(c)
  assert "Pakistan tour of England, 2021" == c[0]["tournament"]

def test_filters_tournament_none():
  filter_array = ["tournament;India"]
  c = cricbuzz.filter_matches(filter_array, matches)
  assert  0 == len(c)

def test_filters_team():
  filter_array = ["team;AUS"]
  c = cricbuzz.filter_matches(filter_array, matches)
  assert  2 == len(c)
  assert "AUS" in c[0]["teams"]

def test_filters_limit():
  filter_array = ["limit;2"]
  c = cricbuzz.filter_matches(filter_array, matches)
  assert  2 == len(c)

def test_filters_limit_greaterthan():
  filter_array = ["limit;6"]
  c = cricbuzz.filter_matches(filter_array, matches)
  assert  4 == len(c)

def test_filters_team_limit():
  filter_array = ["team;AUS","limit;1"]
  c = cricbuzz.filter_matches(filter_array, matches)
  assert  1 == len(c)
  assert "AUS" in c[0]["teams"]

def test_filters_team_team():
  filter_array = ["team;AUS","team;WI"]
  c = cricbuzz.filter_matches(filter_array, matches)
  assert  2 == len(c)
  assert "AUS" in c[0]["teams"]
  assert "WI" in c[0]["teams"]

def test_cricbuzz_get_string():
  str = cricbuzz.get_string(matches[1])
  assert match_string == str


