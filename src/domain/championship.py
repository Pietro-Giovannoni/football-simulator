from dataclasses import dataclass, field
from random import Random

from src.match import Match
from src.standing import Standing
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
        '''Adds a team to the current championship.'''

        if not isinstance(team, Team):
            raise TypeError(f'Expected team as Team, got {type(self.teams).__name__} instead.')

        if team in self.teams:
            raise ValueError(f'{team} is already participating.')

        if len(self.teams) >= self.capacity:
            raise ValueError('This championship is already full.')

        self.teams.append(team)



    def schedule(self, seed: int|None = None) -> dict[int, list[Match]]:
        """
        Sorts a round-robin calendar for this championship.

        Args:
            seed (int|None): optional seed used to shuffle the calendar matchdays.

        Returns:
            calendar (dict[int, list[Match]]): a dictionary of numbered matchdays.
        """

        if not isinstance(seed, int) and seed is not None:
            raise TypeError(f"Expected seed as int or None, got {type(seed).__name__} instead.")

        n = len(self.teams)
        if n < 2:
            raise ValueError("Cannot schedule a calendar with less than two teams.")

        teams = self.teams.copy()
        slots = n if n%2==0 else n+1
        rounds = slots-1
        half = slots//2
        positions = list(range(slots))
        Random(seed).shuffle(positions)
        calendar: dict[int, list[Match]] = {}

        for round_number in range(rounds):     # for each matchday
            first_leg: list[Match] = []
            second_leg: list[Match] = []

            for i in range(half):   # games in a single matchday
                left_index = positions[i]
                right_index = positions[slots-1-i]

                if left_index >= n or right_index >= n:
                    continue        # skip this game (resting team)

                if i==0 and round_number % 2 == 0: # to prevent some team to always play home or away
                    home = teams[left_index]
                    away = teams[right_index]
                else:
                    away = teams[left_index]
                    home = teams[right_index]

                first_leg.append(Match(home=home, away=away))
                second_leg.append(Match(home=away, away=home))

            Random().shuffle(first_leg)
            Random().shuffle(second_leg)
            calendar[round_number+1] = first_leg
            calendar[round_number+20] = second_leg

            # rotation
            fixed = [positions[0]]
            rest = positions[1:]
            rest = [rest[-1]] + rest[:-1]
            positions = fixed + rest

        calendar = dict(sorted(calendar.items()))

        return calendar


    @property
    def standing(self):
        return Standing.from_teams(self.teams)
