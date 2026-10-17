from rich.table import Table
from rich.console import Console

def display_records(records: list[dict], limit:int | None):
    """製造実績の一覧をテーブルで表示する"""
    
    console = Console()

    table = Table(show_header=True, title="製造実績一覧")

    for col in records[0].keys():
        table.add_column(col)

    for i, record in enumerate(records):
        if limit != None and i >= limit:
            break
        table.add_row(*[str(v) for v in record.values()])

    console.print(table);


