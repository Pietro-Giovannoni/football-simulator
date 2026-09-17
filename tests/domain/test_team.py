from src.team import Team
import pytest

def test_team():

    juventus = Team(name = 'Juventus')

    assert juventus.name == 'Juventus'
    assert juventus.code == 'JUV'
    assert juventus.attack == 0
    assert juventus.defense == 0


def test_team_wrong_name():
    with pytest.raises(TypeError):
        Team(name=100)

def test_team_wrong_code():
    with pytest.raises(TypeError):
        Team(name='Juventus', code=100)

def test_team_wrong_attack():
    with pytest.raises(TypeError):
        Team(name='Juventus', attack='abc')

def test_team_wrong_defense():
    with pytest.raises(TypeError):
        Team(name='Juventus', defense='abc')
