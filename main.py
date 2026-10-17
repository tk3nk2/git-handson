import typer
from pathlib import Path
import json
import production_record

app = typer.Typer()

@app.command()
def hello(name: str, times: int = 1):
    """あいさつする"""
    for _ in range(times):
        print(f"Hello, {name}!")


@app.command()
def dummy_production_data(
    output: Path=typer.Argument("data/dummy_productions.json", help="保存先のJSONのファイルパス"), 
    count: int=typer.Argument(10, help="生成するレコード件数")
    ):
    """
    ダミーの製造実績を生成し、JSONファイルに保存する
    
    Example: python main.py dummy-production-data --output-path "data/dummy.jdon" --count 4
    """
    data = [production_record.production_record(i) for i in range(count)]

    with open(output, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"ダミーデータを{output}に出力しました。")


if __name__ == "__main__":
    app()