from src.data_loader import load_teams
import pytest


def test_load_teams(juventus, milan):

    teams = load_teams(file_path='./data/teams.csv')
    assert juventus, milan in teams

def test_load_teams_wrong_path():
    with pytest.raises(TypeError):
        load_teams(file_path=100)
