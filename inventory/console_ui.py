from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()


def show_header():
    console.print(
        Panel.fit(
            "[bold cyan]SOFTWARE INVENTORY SCANNER[/bold cyan]\n"
            "[dim]Skaner zainstalowanego oprogramowania Windows[/dim]",
            border_style="cyan",
        )
    )


def show_system_status(system_info):
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    table.add_row("Administrator", format_bool_pl(system_info["is_admin"]))
    table.add_row(
        "System",
        f"{system_info['system']} {system_info['release']} ({system_info['machine']})",
    )

    border_style = "green" if system_info["is_admin"] else "yellow"
    console.print(Panel(table, title="System", border_style=border_style))

    if not system_info["is_admin"]:
        console.print(
            "[yellow]Uwaga:[/yellow] czesc danych moze byc niedostepna bez uprawnien administratora."
        )


def show_scan_start():
    console.print("[cyan]Skanowanie zainstalowanych programow...[/cyan]")


def show_no_programs_found():
    console.print("[red]Nie znaleziono programow albo skanowanie nie powiodlo sie.[/red]")
    console.print("[dim]Szczegoly sprawdzisz w folderze logs.[/dim]")


def show_no_filter_results(total_before_filters):
    console.print("[yellow]Skanowanie zakonczone, ale filtry nie zwrocily zadnych programow.[/yellow]")
    console.print(f"Liczba programow przed filtrowaniem: [bold]{total_before_filters}[/bold]")


def show_summary(summary):
    table = Table(title="Podsumowanie", border_style="cyan")
    table.add_column("Metryka", style="bold")
    table.add_column("Wartosc", justify="right")

    table.add_row("Programy w raporcie", str(summary["program_count"]))
    table.add_row("Programy przed filtrowaniem", str(summary["total_before_filters"]))
    table.add_row("Producenci", str(summary["publisher_count"]))
    table.add_row("Bez wersji", str(summary["missing_version_count"]))
    table.add_row("Bez producenta", str(summary["missing_publisher_count"]))

    console.print(table)


def show_filters(filter_info):
    if not filter_info["active"]:
        console.print("[dim]Filtry: brak aktywnych filtrow[/dim]")
        return

    table = Table(title="Aktywne filtry", border_style="magenta")
    table.add_column("Filtr", style="bold")
    table.add_column("Wartosc")

    if filter_info["search"]:
        table.add_row("Nazwa zawiera", filter_info["search"])
    if filter_info["publisher"]:
        table.add_row("Producent zawiera", filter_info["publisher"])
    if filter_info["missing_version_only"]:
        table.add_row("Tylko bez wersji", "TAK")

    console.print(table)


def show_top_publishers(summary, limit=5):
    if not summary["top_publishers"]:
        console.print("[dim]Brak danych o producentach.[/dim]")
        return

    table = Table(title="Najczesti producenci", border_style="green")
    table.add_column("Producent")
    table.add_column("Liczba", justify="right")

    for item in summary["top_publishers"][:limit]:
        table.add_row(item["publisher"], str(item["count"]))

    console.print(table)


def show_saved_files(saved_files):
    table = Table(title="Zapisane raporty", border_style="blue")
    table.add_column("Plik", overflow="fold")

    for file_path in saved_files:
        table.add_row(str(file_path))

    console.print(table)


def show_success():
    console.print("[bold green]Gotowe.[/bold green]")


def format_bool_pl(value):
    return "[green]TAK[/green]" if value else "[yellow]NIE[/yellow]"
