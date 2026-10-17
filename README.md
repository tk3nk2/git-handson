# CLIタスク管理ツール

このツールは、コマンドラインで操作できるシンプルなタスク管理のツールです


## インストール

```bash
git clone https://github.com/tk3nk2/git-handson.git
cd git-handson
pip install -r requirements.txt
```

## コマンド一覧
`list`<br>
タスク一覧を表示します

`add`<br>
新しいタスクを追加します

`complete`<br>
指定したタスクを完了にします

`reopen`<br>
完了済みタスクを未完了に戻します

`generate`<br>
製造実績のダミーデータを生成します

`display`<br>
製造実績一覧を表示します


## 使用例
新しいタスク "task 1" を追加する<br>
`python main.py add "task 1"`

保存されているタスクを一覧表示する<br>
`python main.py list`

IDが1のタスクを完了状態にする<br>
`python main.py complete 1`

IDが1のタスクを未完了にする<br>
`python main.py reopen 1`

ダミーの製造実績20件を生成し、JSONファイルに保存する<br>
`python main.py generate --output "data/dummy.jdon" --count 20`

指定したJSONファイルから製造実績の一覧を最大10件表示する<br>
`python main.py display --input data/dummy_productions.json --limit 10`