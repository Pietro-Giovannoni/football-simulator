from collections.abc import Iterable
from dataclasses import dataclass

from src.domain.match import Match
from src.domain.team import Team


@dataclass(frozen=True)
class StandingRow:
    '''
    Immutable class representing a single row from a Standing object.
    '''
    team: Team
    points: int = 0
    scored_goals: int = 0
    conceded_goals: int = 0

    def __post_init__(self):

        if not isinstance(self.team, Team):
            raise TypeError(f'Expected team as Team, got {type(self.team).__name__} instead.')

        if not isinstance(self.points, int) or isinstance(self.points, bool):
            raise TypeError(f'Expected points as int, got {type(self.points).__name__} instead.')

        if not isinstance(self.scored_goals, int) or isinstance(self.scored_goals, bool):
            raise TypeError(f'Expected scored_goals as int, got {type(self.scored_goals).__name__} instead.')

        if not isinstance(self.conceded_goals, int) or isinstance(self.conceded_goals, bool):
            raise TypeError(f'Expected conceded_goals as int, got {type(self.conceded_goals).__name__} instead.')

        if self.points < 0:
            raise ValueError('Points cannot be negative.')

        if self.scored_goals < 0:
            raise ValueError('Scored goals cannot be negative.')

        if self.conceded_goals < 0:
            raise ValueError('Conceded goals cannot be negative.')

    @property
    def goal_difference(self):
        return self.scored_goals - self.conceded_goals





@dataclass(frozen=True)
class Standing:
    '''
    Immutable class representing a championship's standing.
    '''
    rows: tuple[StandingRow, ...]

    def __post_init__(self):
        if not isinstance(self.rows, tuple) or not all(isinstance(row, StandingRow) for row in self.rows):
            raise TypeError('rows must be a tuple of StandingRow objects.')


    @property
    def ranking(self) -> tuple[StandingRow, ...]:
        '''Returns the standing ranked by points, then goal difference, then scored goals.'''
        return tuple(sorted(
            self.rows,
            key = lambda row : (
                row.points,
                row.goal_difference,
                row.scored_goals
            ),
            reverse = True
        ))


    @classmethod
    def build(cls, teams: tuple[Team,...], matches: Iterable[Match]) -> "Standing":
        '''
        Builds the standing and initializes statistics for every team.
        Must be rebuilt after every played match.

        Args:
            teams:      the championship's participants.
            matches:    the championship's scheduled matches; only played matches add value to the standing.
        '''


        if not isinstance(teams, tuple) or not all(isinstance(t, Team) for t in teams):
            raise TypeError('teams must be a tuple of Team objects.')

        matches = tuple(matches)

        if not all(isinstance(m, Match) for m in matches):
            raise TypeError('matches must be a tuple of Match objects.')

        stats = {
            t.code : {
                'team' : t,
                'points' : 0,
                'scored_goals' : 0,
                'conceded_goals' : 0
            }
            for t in teams
        }
        for m in matches:
            if not m.played:
                continue

            home = stats[m.home.code]
            away = stats[m.away.code]

            home['scored_goals'] += m.home_score
            home['conceded_goals'] += m.away_score
            away['scored_goals'] += m.away_score
            away['conceded_goals'] += m.home_score

            if m.winner == m.home:
                home['points'] += 3
            elif m.winner == m.away:
                away['points'] += 3
            else:
                home['points'] += 1
                away['points'] += 1

        rows = [
            StandingRow(
                team = values['team'],
                points = values['points'],
                scored_goals = values['scored_goals'],
                conceded_goals = values['conceded_goals']
            )
            for values in stats.values()
        ]

        return cls(tuple(rows))
