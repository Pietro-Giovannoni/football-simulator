from pathlib import Path

from rich.console import Console
from rich.table import Table

from src.domain.championship import Championship
from src.domain.match import Match
from src.services.data_loader import load_teams


def display_calendar(calendar: dict[int, list[Match]]):
    '''
    displays the calendar through a rich table.
    '''
    table = Table(title = 'Serie A')
    table.add_column('Matchday', style='bold yellow', justify='center')
    table.add_column('Matches')
    table.add_column('Results', justify='center')

    for matchday_number, matchday in calendar.items():
            matches = "\n".join(
                f"{match.home.code} – {match.away.code}"
                for match in matchday
            )
            results = "\n".join(
                f"{match.score}"
                for match in matchday
            )
            table.add_row(
                str(matchday_number),
                matches,
                results,
                end_section=(True, matchday_number==len(calendar))
            )

    Console().print(table)


def main():
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / 'data' / 'teams.csv'
    teams = load_teams(str(csv_path))
    seriea = Championship(teams=teams)
    calendar = seriea.schedule(seed=99)
    display_calendar(calendar)


if __name__ == '__main__':
    main()
