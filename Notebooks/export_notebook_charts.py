import json
import base64
from pathlib import Path


# Configuration
NOTEBOOK_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = NOTEBOOK_DIR / "exported_charts"


# Find notebooks
notebooks = [
    p for p in NOTEBOOK_DIR.glob("*.ipynb")
    if p.stat().st_size > 0
]


if not notebooks:
    print("ERROR: No non-empty .ipynb file found.")
    print(f"Checked folder: {NOTEBOOK_DIR}")
    raise SystemExit(1)


if len(notebooks) > 1:
    print("Multiple notebooks found:")
    for i, notebook in enumerate(notebooks, start=1):
        print(f"{i}. {notebook.name}")

    print()
    choice = input("Enter the number of the notebook to process: ").strip()

    try:
        notebook_path = notebooks[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        raise SystemExit(1)
else:
    notebook_path = notebooks[0]


print(f"Notebook: {notebook_path.name}")
print(f"Size: {notebook_path.stat().st_size:,} bytes")


# Load notebook
try:
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

except json.JSONDecodeError as e:
    print()
    print("ERROR: The selected .ipynb file is not valid JSON.")
    print(f"Details: {e}")
    print()
    print("Open the notebook in Jupyter/VS Code and save it again.")
    raise SystemExit(1)


# Create output folder
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


chart_count = 0


# Extract rendered chart/image outputs
for cell_index, cell in enumerate(
    notebook.get("cells", []),
    start=1
):

    if cell.get("cell_type") != "code":
        continue

    outputs = cell.get("outputs", [])

    for output_index, output in enumerate(
        outputs,
        start=1
    ):

        data = output.get("data", {})


        # PNG
        if "image/png" in data:

            image_data = data["image/png"]

            if isinstance(image_data, list):
                image_data = "".join(image_data)

            image_bytes = base64.b64decode(image_data)

            chart_count += 1

            filename = (
                OUTPUT_DIR
                / f"Chart_{chart_count:02d}_Cell_{cell_index}.png"
            )

            with open(filename, "wb") as f:
                f.write(image_bytes)

            print(f"Exported: {filename.name}")


        # JPEG
        elif "image/jpeg" in data:

            image_data = data["image/jpeg"]

            if isinstance(image_data, list):
                image_data = "".join(image_data)

            image_bytes = base64.b64decode(image_data)

            chart_count += 1

            filename = (
                OUTPUT_DIR
                / f"Chart_{chart_count:02d}_Cell_{cell_index}.jpg"
            )

            with open(filename, "wb") as f:
                f.write(image_bytes)

            print(f"Exported: {filename.name}")


print()
print("=" * 50)
print(f"Charts/images exported: {chart_count}")
print(f"Output folder: {OUTPUT_DIR}")
print("=" * 50)