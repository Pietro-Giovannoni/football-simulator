from random import Random

from src.domain.match import Match
from src.domain.team import Team


def round_robin_builder(teams: tuple[Team, ...], rng: Random) -> tuple[tuple[Match,...], ...]:
    '''
    Builds a double round-robin from a collection of teams, also shuffling matches.
    An optional seed can be provided for reproducibility.

    Returns:
        a tuple of matchdays, which are tuples of Match onjects
    '''
    teams = tuple(teams)
    if not all(isinstance(t, Team) for t in teams):
        raise TypeError('All elements in teams must be Team objects.')

    if not isinstance(rng, Random):
        raise TypeError(f'Expected rng as Random, got {type(rng).__name__} instead.')

    rotation: list[Team | None] = list(teams)
    if len(rotation) % 2 == 1:
        rotation.append(None)   # resting turn for odd number of teams

    rng.shuffle(rotation)

    first_leg: list[tuple[Match, ...]] = []
    rounds = len(rotation) - 1
    matches_per_round = len(rotation) // 2

    for round_number in range(rounds):
        matchday: list[Match] = []

        for index in range(matches_per_round):
            left = rotation[index]
            right = rotation[-1-index]

            if left is None or right is None:   # ignore the resting team
                continue

            home, away = left, right
            if index == 0 and round_number % 2 == 0: # to avoid rotation[0] to always play at home
                home, away = away, home

            matchday.append(Match(home=home, away=away))

        rng.shuffle(matchday)
        first_leg.append(tuple(matchday))

        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1] # circle method: the last element becomes the second

    second_leg: list[tuple[Match,...]] = [
        tuple(Match(home=match.away, away=match.home) for match in matchday)
        for matchday in first_leg
    ]

    return tuple(first_leg + second_leg)
