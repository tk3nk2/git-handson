import typer
from typing import Optional
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from faker import Faker
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
    """
    IDで指定されたタスクのcompletedをstatusに書き換えて上書き保存する
    成功した場合は書き換えたタスクのインデックスを返す
    IDが存在しない場合は-1を返す
    """
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
def list(
    limit: Optional[int]=typer.Option(None, help="表示する件数"),
    completed : Optional[bool]=typer.Option(None, "--completed/--no-completed", help="状態で絞り込み")
): 
    """
    保存されているタスクを一覧表示する。

    --limitで表示件数を指定できる。
    --completedまたは--no-completedで完了状態を絞り込める。
    オプションを省略した場合は、全タスクを表示する。

    Exampls:
        python main.py list
        python main.py list --limit 3
        python main.py list --completed
        python main.py list --no-completed
        python main.py list --completed --limit 3
    """
    tasks = load_tasks()

    if completed is not None:
        tasks = [task for task in tasks if task["completed"] == completed]

    if len(tasks) == 0:
        print("登録されているタスクはありません。")
        return

    table = Table(title="タスク一覧")

    table.add_column("ID", style="white")
    table.add_column("タスク名", style="cyan")
    table.add_column("状態", style="green")

    for task in tasks[:limit]:
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
    
    Example: python main.py complete 1
    """
    tasks = load_tasks()
    result = status_change(tasks, id, True)
    if result == -1:
        print("指定したIDは無効です")
    else:
        list()

@app.command()
def complete(
    id: int=typer.Argument(help="完了にするタスクのID")
):
    """
    タスクのIDを指定して、完了状態にする
    
    Example: python main.py complete 1
    """
    tasks = load_tasks()
    result = status_change(tasks, id, True)
    if result == -1:
        print("指定したIDは無効です")
    else:
        list(limit=None, completed=None)


@app.command()
def reopen(
    id: int=typer.Argument(help="未完了にするタスクのID")
):
    """
    タスクのIDを指定して、未完了にする
    
    Example: python main.py reopen 1
    """
    tasks = load_tasks()
    result = status_change(tasks, id, False)
    if result == -1:
        print("指定したIDは無効です")
    else:
        list(limit=None, completed=None)
        

# === 製造実績 ===
def load_dummy_production(input=Path("data/dummy_productions.json")):
    if not input.exists():
        print("JSONファイルが見つかりませんでした")
        return

    with open(input, "r", encoding="utf-8") as f:
        return json.load(f)


@app.command()
def reopen(
    id: int=typer.Argument(help="未完了にするタスクのID")
):
    """
    タスクのIDを指定して、未完了にする
    
    Example: python main.py reopen 1
    """
    tasks = load_tasks()
    result = status_change(tasks, id, False)
    if result == -1:
        print("指定したIDは無効です")
    else:
        list()
        
@app.command()
def fake_task(
    count: int=typer.Argument(help="ダミーの件数")
):
    """
    指定した件数のダミーのタスクを追加する

    Example: python main.py fake-task 10
    """
    fake = Faker("ja_JP")
    for i in range(count):
        add(fake.sentence(2))
        

# === 製造実績 ===

@app.command()
def generate(
    output: Path=typer.Option("data/dummy_productions.json", help="保存先のJSONのファイルパス"), 
    count: int=typer.Option(10, help="生成するレコード件数")
    ):
    """
    ダミーの製造実績を生成し、JSONファイルに保存する
    
    Example: python main.py generate --output "data/dummy_productions.json" --count 20
    """
    data = [production_record.production_record(i) for i in range(count)]

    with open(output, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"ダミーデータを{output}に出力しました。")


@app.command()
def display(limit: Optional[int]=typer.Option(None, help="表示する件数")):
    """
    指定したJSONファイルから製造実績の一覧を表示する
    
    Example: python main.py display --limit 10
    """

    data = load_dummy_production()
    display_records.display_records(data, limit)


@app.command()
def sort(limit: Optional[int]=typer.Option(None, help="表示する件数")):
    """
    start_timeまたはend_timeでソートした製造実績の一覧を表示する

    Example: python main.py sort --limit 10
    """
    data = load_dummy_production()

    print("ソートする項目を選択してください")
    print("1. start_time")
    print("2. end_time")

    while True:
        sort_item = input("選択：")

        if sort_item == "1":
            sort_key = "start_time"
            break

        elif sort_item == "2":
            sort_key = "end_time"
            break

        else:
            print("1または2を入力してください")

    print("ソートする方法を選択してください")
    print("1. 昇順")
    print("2. 降順")

    while True:
        sort_direction = input("選択：")

        if sort_direction == "1":
            descending = False
            break

        elif sort_direction == "2":
            descending = True
            break

        else:
            print("1または2を選択してください")

    sorted_records = sorted(data, key=lambda record: record[sort_key], reverse=descending)

    display_records.display_records(sorted_records, limit)


if __name__ == "__main__":
    app()
