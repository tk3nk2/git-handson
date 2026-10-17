import typer
from typing import Optional
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
import production_record
import display_records

app = typer.Typer()
file_path = Path("data/tasks.json")


# === タスク管理 ===
def load_tasks():
    """
    tasks.jsonからファイルを読み込む
    tasks.jsonが存在しない場合は、data/に新規作成する
    """
    if not file_path.exists():
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    """
    tasks.jsonに新規タスクを保存する
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def status_change(tasks: list[dict], id: int, status: bool):
    """IDで指定されたタスクのcompletedをstatusに書き換えて上書き保存する"""
    for i in range(len(tasks)):
        if tasks[i]["id"] == id:
            tasks[i]["completed"] = status
            save_tasks(tasks)
            return i
    return -1


@app.command()
def add(title: str=typer.Argument(help="タスク名")):
    """
    新規タスクをtasks.jsonに追加する
    Example: python main.py add "task 1"
    """
    tasks = load_tasks()

    new_id = max([task["id"] for task in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": title,
        "completed": False
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"タスクを追加しました！ (ID: {new_id}, タスク: {title})")


@app.command()
def list():
    """
    保存されているタスクを一覧表示する
    Example: python main.py list
    """
    tasks = load_tasks()

    if len(tasks) == 0:
        print("登録されているタスクはありません。")
        return

    table = Table(title="タスク一覧")

    table.add_column("ID", style="white")
    table.add_column("タスク名", style="cyan")
    table.add_column("状態", style="green")

    for task in tasks:
        status = "完了" if task["completed"] else "未完了"

        table.add_row(str(task["id"]), task["title"], status)

    console = Console()
    console.print(table)

@app.command()
def complete(
    id: int=typer.Argument(help="完了にするタスクのID")
):
    """
    タスクのIDを指定して、完了状態にする
    
    Exsample: python main.py complete 1
    """
    tasks = load_tasks()
    result = status_change(tasks, id, True)
    if result == -1:
        print("指定したIDは無効です")
    else:
        list()


@app.command()
def reopen(
    id: int=typer.Argument(help="未完了にするタスクのID")
):
    """
    タスクのIDを指定して、未完了にする
    
    Exsample: python main.py reopen 1
    """
    tasks = load_tasks()
    result = status_change(tasks, id, False)
    if result == -1:
        print("指定したIDは無効です")
    else:
        list()
        

# === 製造実績 ===

@app.command()
def generate(
    output: Path=typer.Option("data/dummy_productions.json", help="保存先のJSONのファイルパス"), 
    count: int=typer.Option(10, help="生成するレコード件数")
    ):
    """
    ダミーの製造実績を生成し、JSONファイルに保存する
    
    Example: python main.py generate --output "data/dummy.jdon" --count 20
    """
    data = [production_record.production_record(i) for i in range(count)]

    with open(output, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"ダミーデータを{output}に出力しました。")


@app.command()
def display(
    input: Path=typer.Option("data/dummy_productions.json", help="リスト表示するJSONのファイルパス"),
    limit: Optional[int]=typer.Option(None, help="表示する件数")
):
    """
    指定したJSONファイルから製造実績の一覧を表示する
    
    Example: python main.py display --input data/dummy_productions.json --limit 10
    """
    if not input.exists():
        print("JSONファイルが見つかりませんでした")
        return
        
    with open(input, "r") as f:
        data = json.load(f)

    display_records.display_records(data, limit)


if __name__ == "__main__":
    app()
