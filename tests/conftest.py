import pytest

from src.team import Team


@pytest.fixture
def juventus():
    return Team(name='Juventus')

@pytest.fixture
def milan():
    return Team(name='Milan')
