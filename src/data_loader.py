"""
NASA FEMTO (PRONOSTIA) Bearing Dataset Inspector and Loader

Inspects the raw dataset structure, detects file formats, validates data integrity,
and flags anomalies before RUL labeling.
Uses only Python standard library (no external dependencies).
"""

import os
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional


@dataclass
class FileInfo:
    """Metadata about a single data file"""
    path: str
    rows: int
    columns: int
    delimiter: str
    has_header: bool
    column_names: List[str]
    missing_values: int
    empty: bool
    file_size_kb: float

    def __repr__(self):
        return (f"FileInfo(rows={self.rows}, cols={self.columns}, "
                f"delim='{self.delimiter}', empty={self.empty}, "
                f"missing={self.missing_values}, size={self.file_size_kb:.2f}KB)")


@dataclass
class BearingInfo:
    """Metadata about a bearing condition"""
    name: str
    folder_path: str
    file_count: int
    total_rows: int
    files: List[FileInfo]
    total_size_kb: float
    anomalies: List[str]


class FEMTOInspector:
    """
    Inspects NASA FEMTO bearing dataset for structure, format, and data quality.
    """

    def __init__(self, data_root: str = "data/raw"):
        self.data_root = Path(data_root)
        self.learning_set_path = self.data_root / "Learning_set"
        self.test_set_path = self.data_root / "Test_set"
        self.results = {
            "learning_set": {},
            "test_set": {},
            "issues": []
        }

    def detect_delimiter(self, file_path: str) -> str:
        """Detect CSV delimiter by sampling first line"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline()

            # Check common delimiters
            delimiters = [',', '\t', ';', ' ', '|']
            for delim in delimiters:
                if delim in first_line:
                    return delim
            return ','  # Default to comma
        except Exception as e:
            self.results["issues"].append(f"Error detecting delimiter in {file_path}: {e}")
            return ','

    def count_rows(self, file_path: str) -> int:
        """Count total rows in file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return -1

    def inspect_file(self, file_path: str) -> FileInfo:
        """Inspect a single CSV file for structure and quality"""
        file_size_kb = os.path.getsize(file_path) / 1024

        try:
            delimiter = self.detect_delimiter(file_path)
            total_rows = self.count_rows(file_path)

            if total_rows <= 0:
                return FileInfo(
                    path=file_path,
                    rows=0,
                    columns=0,
                    delimiter=delimiter,
                    has_header=False,
                    column_names=[],
                    missing_values=0,
                    empty=True,
                    file_size_kb=file_size_kb
                )

            # Read first row to detect header and structure
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f, delimiter=delimiter)
                first_row = next(reader, None)

                if first_row is None:
                    return FileInfo(
                        path=file_path,
                        rows=0,
                        columns=0,
                        delimiter=delimiter,
                        has_header=False,
                        column_names=[],
                        missing_values=0,
                        empty=True,
                        file_size_kb=file_size_kb
                    )

                # Simple heuristic: if first row contains non-numeric values, treat as header
                has_header = False
                try:
                    for val in first_row:
                        float(val)
                except ValueError:
                    has_header = True

                column_names = first_row if has_header else [f"col_{i}" for i in range(len(first_row))]
                columns = len(first_row)

                # Count missing values
                missing_count = 0
                row_count = total_rows - (1 if has_header else 0)

                # Rescan for missing values
                f.seek(0)
                reader = csv.reader(f, delimiter=delimiter)
                if has_header:
                    next(reader)  # Skip header

                for row in reader:
                    for cell in row:
                        if cell.strip() == '' or cell.lower() in ['nan', 'na', 'none', 'null']:
                            missing_count += 1

            return FileInfo(
                path=file_path,
                rows=row_count,
                columns=columns,
                delimiter=delimiter,
                has_header=has_header,
                column_names=column_names,
                missing_values=missing_count,
                empty=False,
                file_size_kb=file_size_kb
            )

        except Exception as e:
            error_msg = f"Error reading {file_path}: {str(e)}"
            self.results["issues"].append(error_msg)
            return FileInfo(
                path=file_path,
                rows=-1,
                columns=-1,
                delimiter='?',
                has_header=False,
                column_names=[],
                missing_values=-1,
                empty=False,
                file_size_kb=file_size_kb
            )

    def inspect_bearing_condition(self, condition_path: str) -> BearingInfo:
        """Inspect all files within a bearing operating condition folder"""
        condition_name = os.path.basename(condition_path)

        try:
            files = sorted([f for f in os.listdir(condition_path)
                          if f.endswith(('.csv', '.txt', '.dat'))])
        except Exception as e:
            self.results["issues"].append(f"Cannot list files in {condition_path}: {e}")
            return BearingInfo(
                name=condition_name,
                folder_path=condition_path,
                file_count=0,
                total_rows=0,
                files=[],
                total_size_kb=0,
                anomalies=[f"Cannot access folder: {e}"]
            )

        file_infos = []
        total_rows = 0
        total_size = 0
        anomalies = []

        for fname in files:
            fpath = os.path.join(condition_path, fname)
            file_info = self.inspect_file(fpath)
            file_infos.append(file_info)

            if file_info.empty:
                anomalies.append(f"Empty file: {fname}")
            elif file_info.rows < 0:
                anomalies.append(f"Unreadable file: {fname}")
            else:
                total_rows += file_info.rows
                total_size += file_info.file_size_kb

            # Flag missing values
            if file_info.missing_values > 0:
                anomalies.append(
                    f"{fname}: {file_info.missing_values} missing values"
                )

        # Check for consistent structure
        if file_infos:
            first_valid = next((f for f in file_infos if f.rows > 0), None)
            if first_valid:
                for f in file_infos:
                    if f.rows > 0 and f.columns != first_valid.columns:
                        anomalies.append(
                            f"{os.path.basename(f.path)}: Column count mismatch "
                            f"({f.columns} vs {first_valid.columns})"
                        )
                    if f.delimiter != first_valid.delimiter:
                        anomalies.append(
                            f"{os.path.basename(f.path)}: Delimiter mismatch "
                            f"('{f.delimiter}' vs '{first_valid.delimiter}')"
                        )

        return BearingInfo(
            name=condition_name,
            folder_path=condition_path,
            file_count=len(files),
            total_rows=total_rows,
            files=file_infos,
            total_size_kb=total_size,
            anomalies=anomalies
        )

    def inspect_dataset_set(self, set_path: Path, set_name: str) -> Dict:
        """Inspect an entire Learning or Test set"""
        set_results = {
            "name": set_name,
            "path": str(set_path),
            "exists": set_path.exists(),
            "bearing_conditions": {},
            "summary": {}
        }

        if not set_path.exists():
            self.results["issues"].append(f"{set_name} not found at {set_path}")
            return set_results

        # Find all bearing folders (Bearing1_*, Bearing2_*, Bearing3_*)
        bearing_dirs = sorted([
            d for d in os.listdir(set_path)
            if os.path.isdir(os.path.join(set_path, d))
            and d.startswith('Bearing')
        ])

        total_conditions = 0
        total_rows_all = 0
        total_size_all = 0

        for bearing_dir in bearing_dirs:
            bearing_path = os.path.join(set_path, bearing_dir)
            bearing_info = self.inspect_bearing_condition(bearing_path)
            set_results["bearing_conditions"][bearing_dir] = bearing_info

            total_conditions += 1
            total_rows_all += bearing_info.total_rows
            total_size_all += bearing_info.total_size_kb

        set_results["summary"] = {
            "total_bearing_folders": total_conditions,
            "total_files": sum(b.file_count for b in set_results["bearing_conditions"].values()),
            "total_rows": total_rows_all,
            "total_size_mb": total_size_all / 1024
        }

        return set_results

    def run_full_inspection(self) -> Dict:
        """Run complete inspection of Learning and Test sets"""
        print("=" * 80)
        print("NASA FEMTO Bearing Dataset Inspector")
        print("=" * 80)

        self.results["learning_set"] = self.inspect_dataset_set(
            self.learning_set_path, "Learning_set"
        )
        self.results["test_set"] = self.inspect_dataset_set(
            self.test_set_path, "Test_set"
        )

        return self.results

    def print_summary(self):
        """Print a human-readable summary of inspection results"""
        print("\n" + "=" * 80)
        print("DATASET SUMMARY")
        print("=" * 80)

        for set_name in ["learning_set", "test_set"]:
            set_data = self.results[set_name]
            if not set_data.get("exists"):
                print(f"\n{set_name.upper()}: NOT FOUND at {set_data['path']}")
                continue

            print(f"\n{set_data['name'].upper()}")
            print("-" * 80)
            summary = set_data.get("summary", {})
            print(f"  Bearing folders: {summary.get('total_bearing_folders', 0)}")
            print(f"  Total files: {summary.get('total_files', 0)}")
            print(f"  Total rows: {summary.get('total_rows', 0):,}")
            print(f"  Total size: {summary.get('total_size_mb', 0):.2f} MB")

            # Print per-bearing details
            if summary.get('total_bearing_folders', 0) > 0:
                print(f"\n  Bearing Conditions:")
                for bearing_name, bearing_info in sorted(set_data.get("bearing_conditions", {}).items()):
                    print(f"\n    {bearing_name}:")
                    print(f"      Files: {bearing_info.file_count}")
                    print(f"      Total rows: {bearing_info.total_rows:,}")
                    print(f"      Total size: {bearing_info.total_size_kb:.2f} KB")

                    if bearing_info.files:
                        first_file = bearing_info.files[0]
                        if not first_file.empty:
                            print(f"      Columns: {first_file.columns}")
                            print(f"      Column names: {', '.join(first_file.column_names)}")
                            print(f"      Delimiter: '{first_file.delimiter}'")
                            print(f"      Has header: {first_file.has_header}")

                    if bearing_info.anomalies:
                        print(f"      ⚠️  ANOMALIES:")
                        for anomaly in bearing_info.anomalies:
                            print(f"         - {anomaly}")

        # Print global issues
        if self.results.get("issues"):
            print("\n" + "=" * 80)
            print("GLOBAL ISSUES")
            print("=" * 80)
            for issue in self.results["issues"]:
                print(f"  ⚠️  {issue}")

        print("\n" + "=" * 80)

    def export_inspection_report(self, output_file: str = "inspection_report.txt"):
        """Export detailed inspection report to file"""
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("NASA FEMTO Bearing Dataset - Detailed Inspection Report\n")
            f.write("=" * 80 + "\n\n")

            for set_name in ["learning_set", "test_set"]:
                set_data = self.results[set_name]
                if not set_data.get("exists"):
                    f.write(f"{set_name.upper()}: NOT FOUND at {set_data['path']}\n\n")
                    continue

                f.write(f"{set_data['name'].upper()}\n")
                f.write("-" * 80 + "\n")
                summary = set_data.get("summary", {})
                f.write(f"Path: {set_data['path']}\n")
                f.write(f"Bearing folders: {summary.get('total_bearing_folders', 0)}\n")
                f.write(f"Total files: {summary.get('total_files', 0)}\n")
                f.write(f"Total rows: {summary.get('total_rows', 0):,}\n")
                f.write(f"Total size: {summary.get('total_size_mb', 0):.2f} MB\n\n")

                for bearing_name, bearing_info in sorted(set_data.get("bearing_conditions", {}).items()):
                    f.write(f"  {bearing_name}\n")
                    f.write(f"  {'-' * 76}\n")
                    f.write(f"  Files: {bearing_info.file_count}\n")
                    f.write(f"  Total rows: {bearing_info.total_rows:,}\n")
                    f.write(f"  Total size: {bearing_info.total_size_kb:.2f} KB\n")

                    if bearing_info.files:
                        first_valid = next((f for f in bearing_info.files if f.rows > 0), None)
                        if first_valid:
                            f.write(f"  Format: {first_valid.columns} columns, "
                                    f"delimiter='{first_valid.delimiter}', "
                                    f"header={first_valid.has_header}\n")
                            f.write(f"  Columns: {', '.join(first_valid.column_names)}\n")

                    if bearing_info.anomalies:
                        f.write(f"  ANOMALIES:\n")
                        for anomaly in bearing_info.anomalies:
                            f.write(f"    - {anomaly}\n")
                    f.write("\n")

            if self.results.get("issues"):
                f.write("=" * 80 + "\n")
                f.write("GLOBAL ISSUES\n")
                f.write("=" * 80 + "\n")
                for issue in self.results["issues"]:
                    f.write(f"  - {issue}\n")

        print(f"\nDetailed report exported to: {output_file}")


def main():
    """Run inspection and display results"""
    inspector = FEMTOInspector(data_root="data/raw")
    inspector.run_full_inspection()
    inspector.print_summary()
    inspector.export_inspection_report("inspection_report.txt")


if __name__ == "__main__":
    main()
