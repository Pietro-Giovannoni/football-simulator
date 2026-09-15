from dataclasses import dataclass


@dataclass
class Team:
    '''
    A class representing a team, along with its attributes.
    '''
    name: str
    code: str | None = None
    attack: int = 0
    defense: int = 0

    def __post_init__(self):

        if not isinstance(self.name, str):
            raise TypeError(f'Expected name as str, got {type(self.name).__name__} instead.')

        if not isinstance(self.code, str):
            if self.code is None:
                self.code = self.name[:3].upper()
            else:
                raise TypeError(f'Expected code as str, got {type(self.code).__name__} instead.')

        if not isinstance(self.attack, int):
            raise TypeError(f'Expected attack as int, got {type(self.attack).__name__} instead.')

        if not isinstance(self.defense, int):
            raise TypeError(f'Expected defense as int, got {type(self.attack).__name__} instead.')
