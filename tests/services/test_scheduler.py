import pytest
from src.services.scheduler import round_robin_builder
from random import Random


def test_round_robin_builder(juventus, milan, inter, roma):

    seriea = round_robin_builder(
        teams = (juventus, milan, inter, roma),
        rng = Random()
    )
    assert len(seriea) == 6
    assert all(len(matchday) == 2 for matchday in seriea)
    assert all(m.home != m.away for matchday in seriea for m in matchday)


def test_round_robin_builder_wrong_teams(juventus):
    with pytest.raises(TypeError):
        seriea = round_robin_builder(
            teams = (juventus, 'abc'),
            rng = Random()
        )


def test_round_robin_builder_wrong_rng(juventus, milan, inter, roma):
    with pytest.raises(TypeError):
        seriea = round_robin_builder(
            teams = (juventus, milan, inter, roma),
            rng = 'abc'
        )
