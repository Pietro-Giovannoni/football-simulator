from dataclasses import FrozenInstanceError

import pytest
from src.domain.championship import Championship
from src.domain.standing import Standing, StandingRow
from src.domain.team import Team
from src.domain.match import Match


def test_standingrow(juventus: Team):

    row = StandingRow(team=juventus)

    assert row.team == juventus
    assert row.points == row.scored_goals == row.conceded_goals == row.goal_difference == 0


def test_standingrow_wrong_team():
    with pytest.raises(TypeError):
        StandingRow(team='abc')


def test_standingrow_wrong_points(juventus):
    with pytest.raises(TypeError):
        StandingRow(team=juventus, points='abc')


def test_standingrow_wrong_scored(juventus):
    with pytest.raises(TypeError):
        StandingRow(team=juventus, scored_goals='abc')


def test_standingrow_wrong_conceded(juventus):
    with pytest.raises(TypeError):
        StandingRow(team=juventus, conceded_goals='abc')


def test_standingrow_negative_points(juventus):
    with pytest.raises(ValueError):
        StandingRow(team=juventus, points=-4)


def test_standingrow_negative_scored(juventus):
    with pytest.raises(ValueError):
        StandingRow(team=juventus, scored_goals=-3)


def test_standingrow_negative_conceded(juventus):
    with pytest.raises(ValueError):
        StandingRow(team=juventus, conceded_goals=-2)


def test_standing(juventus, milan, inter):

    juv_row = StandingRow(
        team=juventus,
        points=7,
        scored_goals=7,
        conceded_goals=4,
    )
    mil_row = StandingRow(
        team=milan,
        points=3,
        scored_goals=4,
        conceded_goals=5,
    )
    int_row = StandingRow(
        team=inter,
        points=7,
        scored_goals=6,
        conceded_goals=5,
    )
    standing = Standing(rows=(juv_row, mil_row, int_row))

    assert standing.rows == (juv_row, mil_row, int_row)
    assert standing.ranking == (juv_row, int_row, mil_row)


def test_standing_wrong_rows():
    with pytest.raises(TypeError):
        Standing(rows=('abc',))


def test_standing_build(juventus, milan, inter):

    matches: tuple[Match,...] = (
        Match(home=juventus, away=milan, home_score=3, away_score=1),
        Match(home=milan, away=inter, home_score=0, away_score=1),
        Match(home=inter, away=juventus, home_score=0, away_score=0)
    )
    standing = Standing.build(
        teams = (juventus, milan, inter),
        matches = matches
    )
    rows = {
        row.team.code : row
        for row in standing.rows
    }
    assert rows['JUV'].points == 4
    assert rows['JUV'].scored_goals == 3
    assert rows['JUV'].conceded_goals == 1
    assert rows['MIL'].points == 0
    assert rows['MIL'].scored_goals == 1
    assert rows['MIL'].conceded_goals == 4
    assert rows['INT'].points == 4
    assert rows['INT'].scored_goals == 1
    assert rows['INT'].conceded_goals == 0





def test_standing_build_wrong_teams(juventus, milan):
    with pytest.raises(TypeError):
        Standing.build(
            teams = ('abc',),
            matches = ()
        )


def test_standing_build_wrong_matches(juventus, milan):
    with pytest.raises(TypeError):
        Standing.build(
            teams = (juventus, milan),
            matches = ('abc',)
        )


def test_standing_rows_are_immutable(juventus: Team, milan: Team):

    st = Standing(
        rows = (StandingRow(juventus),)
    )
    with pytest.raises(FrozenInstanceError):
        st.rows += (StandingRow(milan),)
