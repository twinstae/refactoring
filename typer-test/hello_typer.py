import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    """Hello, {name} 을 출력합니다."""
    typer.echo(f"Hello {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
    """
    Bye, {name}!을 출력합니다.

    --formal 이면 Goodbye Ms. {name}. Have a good day.를 출력합니다.
    """
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")

style_success = lambda content: typer.style(content, fg=typer.colors.GREEN, bold=True)
style_warning = lambda content: typer.style(content, fg=typer.colors.WHITE, bg=typer.colors.RED)

@app.command()
def iam(good: bool = True):
    message_start = "everything is "

    if good:
        ending = style_success("good")
    else:
        ending = style_warning("bad")

    typer.echo(message_start + ending)

if __name__ == "__main__":
    app()
