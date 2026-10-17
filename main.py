import typer
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

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


if __name__ == "__main__":
    app()