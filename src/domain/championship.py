from collections.abc import Mapping
from dataclasses import dataclass, field
from random import Random
from types import MappingProxyType

from src.domain.match import Match
from src.domain.standing import Standing
from src.domain.team import Team
from src.services.scheduler import round_robin_builder


@dataclass
class Championship:
    """
    Class representing a championship.
    """
    teams: tuple[Team, ...]
    _calendar: dict[int, tuple[Match, ...]] | None = field(default=None, init=False, repr=False)


    def __post_init__(self):

        if len(self.teams) < 2:
            raise ValueError('A championship must have at least two teams.')

        if not all(isinstance(t, Team) for t in self.teams):
            raise TypeError('Every element in teams must be a Team object.')

        codes = [t.code for t in self.teams]
        if len(codes) != len(set(codes)):
            raise ValueError('Teams must be unique.')

        self.teams = tuple(self.teams) # to ensure immutability


    def start(self, seed: int|None=None):
        '''
        Creates a random calendar for this championship.
        '''
        if self._calendar is not None:
            raise ValueError('Championship already started.')

        if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
            raise TypeError(f'Expected seed as int or None, got {type(seed).__name__} instead.')

        matchdays = round_robin_builder(self.teams, Random(seed))

        self._calendar = {
            number : matchday
            for number, matchday in enumerate(matchdays, start=1)
        }


    @property
    def calendar(self) -> Mapping[int, tuple[Match,...]]:
        '''
        Returns the championship (read-only) calendar.
        '''
        if self._calendar is None:
            raise RuntimeError('Call start() before accessing the calendar.')

        return MappingProxyType(self._calendar)


    @property
    def standing(self):
        '''
        Returns the championship (read-only) standing.
        '''
        if self._calendar is None:
            raise RuntimeError('Call start() before accessing the calendar.')

        matches = [
            match
            for matchday in self._calendar.values()
            for match in matchday
            if match.played
        ]
        return Standing.build(teams=self.teams, matches=matches)
