import argparse
from pathlib import Path

from inventory.console_ui import (
    show_filters,
    show_header,
    show_no_filter_results,
    show_no_programs_found,
    show_saved_files,
    show_scan_start,
    show_success,
    show_summary,
    show_system_status,
    show_top_publishers,
)
from inventory.filters import apply_filters, build_filter_info
from inventory.logger_setup import setup_logging
from inventory.reports import save_reports
from inventory.scanner import scan_installed_programs
from inventory.summary import build_summary
from inventory.system_info import get_system_info


DEFAULT_OUTPUT_DIR = "reports"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Software Inventory Scanner - skaner zainstalowanego oprogramowania Windows."
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Folder zapisu raportow. Domyslnie: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--format",
        choices=["txt", "csv", "json", "all"],
        default="all",
        help="Format raportu. Domyslnie: all",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Limit czasu skanowania w sekundach. Domyslnie: 30",
    )
    parser.add_argument(
        "--search",
        default="",
        help="Filtr nazwy programu, np. --search python",
    )
    parser.add_argument(
        "--publisher",
        default="",
        help="Filtr producenta, np. --publisher Microsoft",
    )
    parser.add_argument(
        "--missing-version-only",
        action="store_true",
        help="Pokaz tylko programy bez numeru wersji.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging()

    show_header()
    system_info = get_system_info()
    show_system_status(system_info)

    show_scan_start()

    programs = scan_installed_programs(timeout=args.timeout)

    if not programs:
        show_no_programs_found()
        return

    total_before_filters = len(programs)
    filter_info = build_filter_info(
        search=args.search,
        publisher=args.publisher,
        missing_version_only=args.missing_version_only,
    )
    programs = apply_filters(
        programs,
        search=args.search,
        publisher=args.publisher,
        missing_version_only=args.missing_version_only,
    )

    if not programs:
        show_no_filter_results(total_before_filters)
        return

    output_dir = Path(args.output)
    summary = build_summary(
        programs,
        system_info,
        filter_info=filter_info,
        total_before_filters=total_before_filters,
    )
    saved_files = save_reports(programs, output_dir, args.format, summary)

    show_summary(summary)
    show_filters(summary["filters"])
    show_top_publishers(summary)
    show_saved_files(saved_files)
    show_success()


if __name__ == "__main__":
    main()
