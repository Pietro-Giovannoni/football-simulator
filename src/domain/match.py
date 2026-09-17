from dataclasses import dataclass

from src.domain.team import Team


@dataclass
class Match:
    '''
    Class representing a match, along with its attributes.
    '''
    home: Team
    away: Team
    home_score: int | None = None
    away_score: int | None = None

    def __post_init__(self):

        if not isinstance(self.home, Team):
            raise TypeError(f'Expected home as Team, got {type(self.home).__name__} instead.')

        if not isinstance(self.away, Team):
            raise TypeError(f'Expected away as Team, got {type(self.home).__name__} instead.')

        for score in (self.home_score, self.away_score):
            if score is not None:
                if isinstance(score, bool) or not isinstance(score, int):
                    raise TypeError('Scores must be integer numbers.')
                if score < 0:
                    raise ValueError('Cannot have negative scores.')


    @property
    def winner(self) -> Team | None:
        '''Returns the winning team or None, in case of a tie.'''

        if self.home_score is not None and self.away_score is not None:
            if self.home_score > self.away_score:
                return self.home
            if self.home_score < self.away_score:
                return self.away
        return None


    @property
    def score(self):
        '''Returns the match score.'''

        if self.home_score is not None and self.away_score is not None:
            return (self.home_score, self.away_score)
        return None


    def update_score(self, home_score: int|None = None, away_score: int|None = None):
        '''Updates the match score according to the given input.'''

        for score in (home_score, away_score):
            if score is not None:
                if isinstance(score, bool) or not isinstance(score, int):
                    raise TypeError('Scores must be integer numbers.')
                if score < 0:
                    raise ValueError('Cannot have negative scores.')

        if home_score is not None:
            self.home_score = home_score
        if away_score is not None:
            self.away_score = away_score
