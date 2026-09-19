import pytest
from src.domain.championship import Championship
from src.domain.team import Team

def test_championship_even(juventus: Team, milan: Team, inter: Team, roma: Team):

    seriea = Championship(teams=[juventus, milan, inter, roma])
    assert isinstance(seriea.teams, tuple)

    seriea.start(seed=47)
    assert seriea._calendar is not None
    assert len(seriea.calendar) == 6
    assert all(len(matchday)==2 for matchday in seriea.calendar.values())
    assert all(match.home != match.away for matchday in seriea.calendar.values() for match in matchday)
    pairs = [
        (match.home.code, match.away.code)
        for matchday in seriea.calendar.values()
        for match in matchday
    ]

    assert len(pairs) == len(set(pairs)) # no duplicate matches


def test_championship_odd(juventus: Team, milan: Team, inter: Team):

    seriea = Championship(teams=[juventus, milan, inter])
    assert isinstance(seriea.teams, tuple)

    seriea.start(seed=47)
    assert seriea._calendar is not None
    assert len(seriea.calendar) == 6
    assert all(len(matchday)==1 for matchday in seriea.calendar.values())
    assert all(match.home != match.away for matchday in seriea.calendar.values() for match in matchday)
    pairs = [
        (match.home.code, match.away.code)
        for matchday in seriea.calendar.values()
        for match in matchday
    ]

    assert len(pairs) == len(set(pairs)) # no duplicate matches


def test_championship_zero_teams():
    with pytest.raises(ValueError):
        Championship(teams=())


def test_championship_wrong_teams(juventus: Team, milan: Team):
    with pytest.raises(TypeError):
        Championship(teams=(juventus, milan, 'abc'))


def test_championship_duplicate_teams(juventus: Team, milan: Team):
    with pytest.raises(ValueError):
        Championship(teams=(juventus, milan, juventus))


def test_championship_wrong_seed(juventus: Team, milan: Team):
    seriea = Championship(teams=(juventus, milan))
    with pytest.raises(TypeError):
        seriea.start(seed='abc')


def test_championship_start_with_calendar(juventus: Team, milan: Team):
    seriea = Championship(teams=(juventus, milan))
    seriea.start(seed=99)
    assert seriea.calendar is not None

    with pytest.raises(ValueError):
        seriea.start(seed=47)


def test_championship_calendar_before_start(juventus: Team, milan: Team):
    seriea = Championship(teams=(juventus, milan))
    with pytest.raises(RuntimeError):
        seriea.calendar


def test_championship_standing_before_start(juventus: Team, milan: Team):
    seriea = Championship(teams=(juventus, milan))
    with pytest.raises(RuntimeError):
        seriea.standing


def test_standing_is_rebuilt_from_played_matches(juventus, milan):
    championship = Championship((juventus, milan))
    championship.start(seed=1)

    match = championship.calendar[1][0]
    match.update_score(home_score=2, away_score=1)

    ranking = championship.standing.ranking

    assert ranking[0].team == match.home
    assert ranking[0].points == 3
    assert ranking[0].scored_goals == 2
    assert ranking[0].conceded_goals == 1
    assert ranking[1].team == match.away
    assert ranking[1].points == 0
    assert ranking[1].scored_goals == 1
    assert ranking[1].conceded_goals == 2
