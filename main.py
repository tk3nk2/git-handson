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
def dummy_production_data(output_path: Path="data/dummy_productions.json", count: int=10):
    """ダミーの製造実績をJsonファイルで出力する"""

    data = [production_record.production_record(i) for i in range(count)]

    with open(output_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"ダミーデータを{output_path}に出力しました。")


if __name__ == "__main__":
    app()