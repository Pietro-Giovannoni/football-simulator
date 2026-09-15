import pytest

from src.championship import Championship
from src.team import Team


def test_championship(juventus: Team, milan: Team):

    seriea = Championship(
        teams = [juventus, milan],
        capacity = 2
    )
    assert juventus, milan in seriea.teams
    assert seriea.capacity == 2


def test_championship_wrong_teams():
    with pytest.raises(TypeError):
        Championship(teams=['abc'])

def test_championship_wrong_capacity(juventus: Team):
    with pytest.raises(TypeError):
        Championship(teams=[juventus], capacity='abc')

def test_championship_negative_capacity(juventus: Team):
    with pytest.raises(ValueError):
        Championship(teams=[juventus], capacity=-3)

def test_championship_exceeding_capacity(juventus: Team, milan: Team):
    with pytest.raises(ValueError):
        Championship(teams=[juventus, milan], capacity=1)


def test_championship_add_team(juventus: Team):
    seriea = Championship()
    assert seriea.teams == []

    seriea.add_team(juventus)
    assert juventus in seriea.teams


def test_championship_add_team_wrong_team():
    seriea = Championship()
    with pytest.raises(TypeError):
        seriea.add_team('abc')

def test_championship_add_team_double_team(juventus: Team):
    seriea = Championship(teams=[juventus])
    with pytest.raises(ValueError):
        seriea.add_team(juventus)

def test_championship_add_team_exceeding_capacity(juventus: Team, milan: Team):
    seriea = Championship(teams=[juventus], capacity=1)
    with pytest.raises(ValueError):
        seriea.add_team(milan)


def test_championship_schedule(juventus, milan):
    seriea = Championship(teams=[juventus, milan])
    calendar = seriea.schedule(seed=37)

    assert len(calendar) == 2


def test_championship_schedule_wrong_seed(juventus, milan):
    seriea = Championship(teams=[juventus, milan])
    with pytest.raises(TypeError):
        seriea.schedule(seed='abc')

def test_championship_schedule_few_teams(juventus):
    seriea = Championship(teams=[juventus])
    with pytest.raises(ValueError):
        seriea.schedule(seed=4)
