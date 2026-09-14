from dataclasses import dataclass, field

from src.team import Team


@dataclass
class Championship:
    '''
    A class representing a championship, along with its attributes.
    '''
    teams: list[Team] = field(default_factory=list)
    capacity: int = 20

    def __post_init__(self):

        if not isinstance(self.teams, list):
            raise TypeError(f'Expected teams as list, got {type(self.teams).__name__} instead.')

        if not all(isinstance(team, Team) for team in self.teams):
            raise TypeError('All elements in teams must be Team objects.')

        if not isinstance(self.capacity, int):
            raise TypeError(f'Expected capacity as int, got {type(self.capacity).__name__} instead.')

        if self.capacity <= 0:
            raise ValueError('Must have a positive capacity.')

        if len(self.teams) > self.capacity:
            raise ValueError('This championship exceeds its own capacity.')



    def add_team(self, team: Team) -> None:

        if not isinstance(team, Team):
            raise TypeError(f'Expected team as Team, got {type(self.teams).__name__} instead.')

        if team in self.teams:
            raise ValueError(f'{team} is already participating.')

        if len(self.teams) >= self.capacity:
            raise ValueError('This championship is already full.')

        self.teams.append(team)
