from dataclasses import dataclass

from src.team import Team


@dataclass
class StandingRow:
    '''
    Class representing a single row from a Standing object.
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

        if self.scored_goals < 0:
            raise ValueError('Scored goals cannot be negative.')

        if self.conceded_goals < 0:
            raise ValueError('Conceded goals cannot be negative.')

    @property
    def goal_difference(self):
        return self.scored_goals - self.conceded_goals





class Standing:
    '''
    Class representing a championship's standing.
    '''
    def __init__(self, rows: list[StandingRow]):

        if not isinstance(rows, list) or not all(isinstance(row, StandingRow) for row in rows):
            raise TypeError('rows must be a list of StandingRow objects.')

        self.rows = rows
        self.teams = [row.team for row in rows]


    @classmethod
    def from_teams(cls, teams: list[Team]):

        if not isinstance(teams, list) or not all(isinstance(team, Team) for team in teams):
            raise TypeError('teams must be a list of Team objects.')

        cls.rows = [StandingRow(team=team) for team in teams]
        cls.teams = teams
        return cls


    @property
    def ranking(self) -> list[StandingRow]:
        '''Returns the standing ranked by points, then goal difference, then scored goals.'''
        return sorted(
            self.rows,
            key = lambda row : (
                row.points,
                row.goal_difference,
                row.scored_goals
            ),
            reverse = True
        )
