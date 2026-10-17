import typer

app = typer.Typer()

@app.command()
def hello(name: str, times: int = 1):
    """あいさつする"""
    for _ in range(times):
        print(f"Hello, {name}!")

if __name__ == "__main__":
    app()