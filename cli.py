#!/usr/bin/env python
import subprocess

import click


@click.group()
def cli():
    """Утилита для управления миграциями базы данных."""
    pass


@cli.command()
@click.option("--message", "-m", required=True, help="Сообщение для миграции")
@click.option(
    "--autogenerate",
    is_flag=True,
    default=True,
    help="Автоматически генерировать миграцию на основе моделей",
)
def make_migration(message: str, autogenerate: bool) -> None:
    """Создать новую миграцию."""
    cmd = ["alembic", "revision"]
    if autogenerate:
        cmd.append("--autogenerate")
    cmd.extend(["-m", message])

    click.echo(f"Создание миграции: {message}")
    subprocess.run(cmd)
    click.echo("Миграция создана.")


@cli.command()
@click.option("--revision", help="Идентификатор ревизии (по умолчанию: последняя)")
def migrate(revision: str | None = None) -> None:
    """Накатить миграции до указанной ревизии (по умолчанию: до последней)."""
    cmd = ["alembic", "upgrade"]
    if revision:
        cmd.append(revision)
    else:
        cmd.append("head")

    target = revision if revision else "последней версии"
    click.echo(f"Обновление БД до {target}...")
    subprocess.run(cmd)
    click.echo("Миграции успешно применены.")


@cli.command()
@click.option("--steps", "-n", default=1, help="Количество шагов для отката")
def rollback(steps: int) -> None:
    """Откатить миграции на указанное количество шагов назад."""
    cmd = ["alembic", "downgrade", f"-{steps}"]

    click.echo(f"Откат на {steps} {'шаг' if steps == 1 else 'шагов'}...")
    subprocess.run(cmd)
    click.echo("Откат выполнен.")


@cli.command()
def history() -> None:
    """Показать историю миграций."""
    cmd = ["alembic", "history"]

    click.echo("История миграций:")
    subprocess.run(cmd)


@cli.command()
def current() -> None:
    """Показать текущую версию базы данных."""
    cmd = ["alembic", "current"]

    click.echo("Текущая версия БД:")
    subprocess.run(cmd)


if __name__ == "__main__":
    cli()
