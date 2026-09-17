import csv

from src.domain.team import Team


def load_teams(file_path: str) -> list[Team]:

    if not isinstance(file_path, str):
        raise TypeError(f'Expected file_path as str, got {type(file_path).__name__} instead.')

    teams = []
    with open(file=file_path, mode='r', newline='') as file:
        reader = csv.DictReader(    # lines commented with # will be ignored
            line for line in file
            if line.strip() and not line.lstrip().startswith('#')
        )

        required_columns = {'name', 'code', 'attack', 'defense'}
        missing_columns = required_columns - set(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(f'Missing CSV columns: {', '.join(sorted(missing_columns))}')

        for row in reader:
            team = Team(
                name = row['name'],
                code = row['code'],
                attack = int(row['attack']),
                defense = int(row['defense'])
            )
            teams.append(team)

    return teams
