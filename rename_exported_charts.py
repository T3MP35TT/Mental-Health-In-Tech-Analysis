from pathlib import Path
import re
import shutil

# Mental Health in Tech Analytics
# Rename exported EDA charts using the actual notebook chart order

PROJECT_DIR = Path(r"D:\Mental-Health-in-Tech-Analytics")
CHARTS_DIR = PROJECT_DIR / "outputs" / "charts"


def natural_sort_key(path):
    """Sort chart filenames naturally by their embedded numbers."""
    parts = re.split(r"(\d+)", path.name)
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def main():
    if not CHARTS_DIR.exists():
        print("ERROR: Charts folder not found:")
        print(CHARTS_DIR)
        return

    chart_files = [
        p for p in CHARTS_DIR.iterdir()
        if p.is_file()
        and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]

    chart_files.sort(key=natural_sort_key)

    if not chart_files:
        print("ERROR: No chart files found.")
        return

    # These names match the 35 chart headings in Mental_Health_Tech_EDA.ipynb.
    chart_names = [
        "01_age_distribution",
        "02_gender_distribution",
        "03_age_group_distribution",
        "04_company_size_distribution",
        "05_remote_work_distribution",
        "06_mental_health_treatment_distribution",
        "07_family_history_distribution",
        "08_treatment_rate_by_family_history",
        "09_mental_health_work_interference",
        "10_treatment_rate_by_work_interference",
        "11_treatment_rate_by_gender",
        "12_treatment_rate_by_age_group",
        "13_family_history_by_age_group",
        "14_treatment_rate_by_remote_work",
        "15_treatment_rate_by_company_size",
        "16_mental_health_benefits",
        "17_mental_health_care_options",
        "18_workplace_wellness_program",
        "19_treatment_rate_by_mental_health_benefits",
        "20_treatment_rate_by_care_options",
        "21_treatment_rate_by_wellness_program",
        "22_workplace_help_seeking_resources",
        "23_treatment_rate_by_help_seeking_resources",
        "24_perceived_anonymity",
        "25_treatment_rate_by_perceived_anonymity",
        "26_ease_of_taking_mental_health_leave",
        "27_treatment_rate_by_ease_of_taking_leave",
        "28_coworker_attitudes_toward_mental_health",
        "29_supervisor_attitudes_toward_mental_health",
        "30_perceived_mental_health_consequences",
        "31_treatment_rate_by_perceived_mental_health_consequences",
        "32_mental_health_interview_perception",
        "33_treatment_rate_by_mental_health_interview_perception",
        "34_mental_health_vs_physical_health_perception",
        "35_observed_mental_health_consequences",
    ]

    if len(chart_files) != len(chart_names):
        print(f"ERROR: Found {len(chart_files)} chart files,")
        print(f"but the notebook contains {len(chart_names)} chart names.")
        print()
        print("Charts found:")
        for i, chart in enumerate(chart_files, start=1):
            print(f"{i:02d}. {chart.name}")
        return

    # Temporary directory prevents filename collisions during renaming.
    temp_dir = CHARTS_DIR / "_rename_temp"

    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    temp_dir.mkdir()

    print(f"Found {len(chart_files)} chart files.")
    print()
    print("Renaming charts based on the actual notebook order:")
    print("-" * 90)

    temp_files = []

    for index, chart in enumerate(chart_files, start=1):
        temp_name = f"chart_temp_{index:02d}{chart.suffix.lower()}"
        temp_path = temp_dir / temp_name

        shutil.move(str(chart), str(temp_path))
        temp_files.append((temp_path, chart_names[index - 1]))

        print(
            f"{index:02d}. {chart.name}"
            f"  ->  {chart_names[index - 1]}{chart.suffix.lower()}"
        )

    print()

    for temp_path, new_name in temp_files:
        destination = CHARTS_DIR / f"{new_name}{temp_path.suffix}"

        if destination.exists():
            destination.unlink()

        shutil.move(str(temp_path), str(destination))

    temp_dir.rmdir()

    print("=" * 90)
    print("SUCCESS")
    print("=" * 90)
    print(f"Renamed {len(chart_files)} charts.")
    print()
    print("Charts are stored in:")
    print(CHARTS_DIR)


if __name__ == "__main__":
    main()
