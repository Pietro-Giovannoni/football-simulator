import pytest

from src.match import Match

def test_match(juventus, milan):

    match = Match(home=juventus, away=milan)

    assert match.home == juventus
    assert match.away == milan
    assert match.score is None
    assert match.winner is None

    match.update_score(home_score=2, away_score=1)
    assert match.score == (2,1)
    assert match.winner == juventus


def test_match_wrong_home(juventus: Team):
    with pytest.raises(TypeError):
        Match(home='abc', away=juventus)

def test_match_wrong_away(juventus: Team):
    with pytest.raises(TypeError):
        Match(home=juventus, away='abc')

def test_match_wrong_home_score(juventus, milan):
    with pytest.raises(TypeError):
        Match(home=juventus, away=milan, home_score=False)

def test_match_wrong_away_score(juventus, milan):
    with pytest.raises(TypeError):
        Match(home=juventus, away=milan, away_score='abc')

def test_match_negative_home_score(juventus, milan):
    with pytest.raises(ValueError):
        Match(home=juventus, away=milan, home_score=-3)

def test_match_negative_away_score(juventus, milan):
    with pytest.raises(ValueError):
        Match(home=juventus, away=milan, away_score=-4)

def test_match_update_score_wrong(juventus, milan):
    match = Match(home=juventus, away=milan)
    with pytest.raises(TypeError):
        match.update_score(home_score='abc')

def test_match_update_score_negative(juventus, milan):
    match = Match(home=juventus, away=milan)
    with pytest.raises(ValueError):
        match.update_score(away_score=-5)
