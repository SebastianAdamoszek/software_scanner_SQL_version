from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()


# =========================
# MENU
# =========================
def show_menu(search, publisher, missing):

    status = f"""
    Filtry aktywne:
    • nazwa: {search or '-'}
    • producent: {publisher or '-'}
    • brak wersji: {missing}
    """

    console.print(
        Panel(
            status,
            title="STATUS",
            border_style="yellow"
        )
    )

    table = Table(
        title="MENU",
        border_style="cyan",
        row_styles=["", "on grey11"],
        show_lines=False
    )

    table.add_column(
        "Opcja",
        width=6,
        justify="center"
    )

    table.add_column("Akcja")

    table.add_row("[cyan]1[/cyan]", "Skanuj system")
    table.add_row("[cyan]2[/cyan]", "Filtruj wg nazwy")
    table.add_row("[cyan]3[/cyan]", "Filtruj wg producenta")
    table.add_row(
        "[cyan]4[/cyan]",
        f"Pokaż tylko programy bez wersji: {'TAK' if missing else 'NIE'}"
    )
    table.add_row("[yellow]5[/yellow]", "Resetuj filtry")
    table.add_row("[red]6[/red]", "Wyjście")

    console.print(table)

    console.print(
        "\n[grey62]Wpisz numer opcji i Enter[/grey62]"
    )


# =========================
# HEADER
# =========================
def show_header():
    console.print(
        Panel.fit(
            "[bold cyan]SOFTWARE INVENTORY SCANNER[/bold cyan]\n"
            "[grey62]Skaner zainstalowanego oprogramowania Windows[/grey62]",
            border_style="cyan",
        )
    )


# =========================
# SYSTEM INFO
# =========================
def show_system_status(system_info):

    table = Table.grid(padding=(0, 2))

    table.add_column(style="bold")
    table.add_column()

    table.add_row(
        "Administrator",
        format_bool_pl(system_info.get("is_admin", False))
    )

    system = system_info.get("system", "N/A")
    release = system_info.get("release", "")
    machine = system_info.get("machine", "")

    table.add_row(
        "System",
        f"{system} {release} ({machine})"
    )

    border_style = (
        "green"
        if system_info.get("is_admin")
        else "yellow"
    )

    console.print(
        Panel(
            table,
            title="System",
            border_style=border_style
        )
    )


# =========================
# SCAN INFO
# =========================
def show_scan_start():
    console.print(
        "[cyan]Skanowanie zainstalowanych programow...[/cyan]"
    )


def show_no_programs_found():
    console.print(
        "[red]Nie znaleziono programow albo skanowanie nie powiodlo sie.[/red]"
    )


def show_no_filter_results(total_before_filters):
    console.print(
        "[yellow]Brak wyników po filtrach.[/yellow]"
    )

    console.print(
        f"Przed filtrem: [bold]{total_before_filters}[/bold]"
    )


# =========================
# SUMMARY
# =========================
def show_summary(summary):

    table = Table(
        title="Podsumowanie",
        border_style="cyan"
    )

    table.add_column(
        "Metryka",
        style="bold"
    )

    table.add_column(
        "Wartość",
        justify="right"
    )

    table.add_row(
        "Programy",
        str(summary.get("program_count", 0))
    )

    table.add_row(
        "Przed filtrem",
        str(summary.get("total_before_filters", 0))
    )

    table.add_row(
        "Producenci",
        str(summary.get("publisher_count", 0))
    )

    table.add_row(
        "Bez wersji",
        str(summary.get("missing_version_count", 0))
    )

    table.add_row(
        "Bez producenta",
        str(summary.get("missing_publisher_count", 0))
    )

    console.print(table)


# =========================
# FILTERS
# =========================
def show_filters(filter_info):

    if not filter_info.get("active"):

        console.print(
            "[grey62]Brak aktywnych filtrów[/grey62]"
        )

        return

    table = Table(
        title="Filtry",
        border_style="magenta"
    )

    table.add_column("Filtr")
    table.add_column("Wartość")

    if filter_info.get("search"):
        table.add_row(
            "Nazwa",
            filter_info["search"]
        )

    if filter_info.get("publisher"):
        table.add_row(
            "Producent",
            filter_info["publisher"]
        )

    if filter_info.get("missing_version_only"):
        table.add_row(
            "Bez wersji",
            "TAK"
        )

    console.print(table)


# =========================
# TOP PRODUCENCI
# =========================
def show_top_publishers(summary, limit=5):

    top = summary.get(
        "top_publishers",
        []
    )

    if not top:

        console.print(
            "[grey62]Brak danych o producentach[/grey62]"
        )

        return


    table = Table(
        title="LISTA PRODUCENTÓW",
        border_style="green"
    )

    table.add_column("Producent")
    table.add_column(
        "Ilość",
        justify="right"
    )


    for item in top[:limit]:

        table.add_row(
            str(item.get("publisher", "-")),
            str(item.get("count", 0))
        )


    console.print(table)


# =========================
# TABLE PROGRAMS
# =========================
def show_programs_table(programs, limit=30):

    if not programs:

        console.print(
            "[yellow]Brak programów[/yellow]"
        )

        return


    table = Table(
        title="ZAINSTALOWANE PROGRAMY",
        border_style="cyan",
        show_lines=False,
        row_styles=["", "grey62"],
    )


    table.add_column(
        "LP",
        justify="right",
        width=4
    )

    table.add_column(
        "Program",
        overflow="fold",
        min_width=35
    )

    table.add_column(
        "Wersja",
        width=18
    )

    table.add_column(
        "Producent",
        overflow="fold",
        min_width=25
    )


    for i, p in enumerate(
        programs[:limit],
        start=1
    ):

        table.add_row(
            str(i),
            p.get("name", "-"),
            p.get("version") or "-",
            p.get("publisher") or "-"
        )


    console.print(table)


    if len(programs) > limit:

        console.print(
            f"[grey62]Pokazano {limit} z {len(programs)}[/grey62]"
        )


# =========================
# FILES
# =========================
def show_saved_files(files):

    table = Table(
        title="Zapisane raporty",
        border_style="blue"
    )

    table.add_column(
        "Plik",
        overflow="fold"
    )


    for f in files:

        table.add_row(
            str(f)
        )


    console.print(table)


# =========================
# SUCCESS
# =========================
def show_success():

    console.print(
        "[bold green]Gotowe.[/bold green]"
    )


# =========================
# UTIL
# =========================
def format_bool_pl(value):

    return (
        "[green]TAK[/green]"
        if value
        else "[yellow]NIE[/yellow]"
    )
