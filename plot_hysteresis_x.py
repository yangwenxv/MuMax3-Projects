import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def normalize_header(name: str) -> str:
    text = name.strip()
    if text.startswith("#"):
        text = text[1:].strip()
    return text


def load_hysteresis_data(table_path: Path) -> tuple[list[float], list[float]]:
    with table_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        rows = list(reader)

    if not rows:
        raise ValueError(f"Table is empty: {table_path}")

    headers = [normalize_header(item) for item in rows[0]]

    try:
        b_index = headers.index("B_extx (T)")
        mx_index = headers.index("mx ()")
    except ValueError as exc:
        raise ValueError(f"Required columns were not found. Headers: {headers}") from exc

    b_values: list[float] = []
    mx_values: list[float] = []

    for row in rows[1:]:
        if not row or len(row) <= max(b_index, mx_index):
            continue
        b_values.append(float(row[b_index]))
        mx_values.append(float(row[mx_index]))

    if not b_values:
        raise ValueError(f"No valid data rows were read: {table_path}")

    return b_values, mx_values


def plot_hysteresis(b_values: list[float], mx_values: list[float], output: Path | None) -> None:
    plt.figure(figsize=(7, 5))
    plt.plot(b_values, mx_values, color="tab:blue", linewidth=1.8)
    plt.scatter(b_values, mx_values, s=10, color="tab:blue")
    plt.xlabel("B_extx (T)")
    plt.ylabel("mx")
    plt.title("X-direction Hysteresis Loop")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    if output is not None:
        plt.savefig(output, dpi=300)
        print(f"Figure saved to: {output}")

    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot the MuMax3 x-direction hysteresis loop (mx-B_extx).")
    parser.add_argument(
        "table",
        nargs="?",
        default="demo1.out/table.txt",
        help="Path to MuMax3 table.txt. Default: demo1.out/table.txt",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output image path, for example: hysteresis_x.png",
    )
    args = parser.parse_args()

    table_path = Path(args.table)
    if not table_path.is_file():
        raise FileNotFoundError(f"Data file not found: {table_path}")

    output_path = Path(args.output) if args.output else None
    b_values, mx_values = load_hysteresis_data(table_path)
    plot_hysteresis(b_values, mx_values, output_path)


if __name__ == "__main__":
    main()
