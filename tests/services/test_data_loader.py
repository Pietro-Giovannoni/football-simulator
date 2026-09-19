from src.services.data_loader import load_teams
import pytest


def test_load_teams():

    teams = load_teams(file_path='./src/repos/teams.csv')
    codes = {team.code for team in teams}
    assert {"JUV", "MIL"} <= codes

def test_load_teams_wrong_path():
    with pytest.raises(TypeError):
        load_teams(file_path=100)
