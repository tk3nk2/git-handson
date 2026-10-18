# CLIタスク管理ツール

Pythonで作成した、コマンドラインから操作できるシンプルなタスク管理のツールです。

タスクの追加・一覧表示・完了状態の変更・削除などを行えます。
タスクデータはJSONファイルに保存されます


## インストール

リポジトリをクローンします。

```bash
git clone https://github.com/tk3nk2/git-handson.git
cd git-handson
```

必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```


## 使い方

### `add`: タスクの追加

新しいタスクを追加します。

```bash
python main.py add "task-name"
```


### `list`: タスクの一覧表示

すべてのタスクを表示します。

```bash
python main.py list
```

表示件数を指定する場合:

```bash
python main.py list --limit 3
```

完了済みのタスクのみ表示する場合:

```bash
python main.py list --completed
```

未完了のタスクのみを表示する場合:

```bash
python main.py list --no-completed
```


### `complete`: タスクの完了

指定したIDのタスクを完了状態に変更します。

```bash
python main.py complete 1
```


### `reopen`: タスクの再開

指定したIDのタスクを未完了状態に戻します。

```bash
python main.py reopen 1
```


### `delete`: タスクの削除

指定したIDのタスクを削除します。

```bash
python main.py delete 1
```

完了済みのタスクを一括削除する場合:

```bash
python main.py delete --completed
```

未完了のタスクを一括削除する場合:

```bash
python main.py delete --no-completed
```


### `fake-task`: ダミータスクの生成

指定した件数のダミータスクを生成します。

```bash
python main.py fake-task 10
```


### `generate`: ダミー製造実績の生成

指定した件数のダミー製造実績を生成します。

```bash
python main.py generate --output "data/dummy_productions.json" --count 20
```


### `display`: 製造実績の一覧表示

すべての製造実績を表示します。

```bash
python main.py display
```

表示件数を指定する場合:

```bash
python main.py display --limit 10
```


### `sort`: 製造実績のソート表示

timeでソートした製造実績の一覧を表示します。

```bash
python main.py sort
```

表示件数を指定する場合:

```bash
python main.py sort --limit 10
```


## コマンド一覧

| コマンド | 説明 |
|---|---|
| `add` | 新しいタスクを追加 |
| `list` | タスク一覧を表示 |
| `complete` | タスクを完了状態に変更 |
| `reopen` | タスクを未完了状態に変更 |
| `delete` | タスクを削除 |
| `fake-task` | ダミータスクを生成 |
| `generate` | ダミー製造実績を生成 |
| `display` | 製造実績一覧を表示 |
| `sort` | 製造実績を時間でソートして表示 |

各コマンドの詳細は、`--help`で確認できます。

```bash
python main.py --help
python main.py add --help
```


## データの保存先

タスクデータは以下のJSONファイルに保存されます。

```text
data/tasks.json
```

保存形式の例：

```json
[
    {
        "id": 1,
        "title": "task 1",
        "completed": false
    },
    {
        "id": 2,
        "title": "task 2",
        "completed": true
    }
]
```


## 使用技術

- Python
- Typer
- Rich
- Faker