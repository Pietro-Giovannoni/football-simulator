import pytest

from src.domain.team import Team


@pytest.fixture
def juventus():
    return Team(name='Juventus')

@pytest.fixture
def milan():
    return Team(name='Milan')

@pytest.fixture
def inter():
    return Team(name='Inter')

@pytest.fixture
def roma():
    return Team(name='Roma')
