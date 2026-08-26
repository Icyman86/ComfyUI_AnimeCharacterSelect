import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

source_files = sorted(
    ROOT.glob("output_*.json"),
    key=lambda path: int(path.stem.split("_")[1]),
)

if not source_files:
    raise SystemExit("No output_*.json files found.")

for source_path in source_files:
    print(f"Converting {source_path.name}...")

    with source_path.open("r", encoding="utf-8") as file:
        source_data = json.load(file)

    if not isinstance(source_data, list):
        print(f"  SKIPPED: expected a list, got {type(source_data).__name__}")
        continue

    converted = {}

    for index, entry in enumerate(source_data):
        if not isinstance(entry, dict):
            print(f"  WARNING: item {index} is not a dictionary; skipped")
            continue

        for character_name, image_data in entry.items():
            if character_name in converted:
                print(f"  WARNING: duplicate character: {character_name}")

            converted[character_name] = {
                "prompt": character_name,
                "image": image_data,
            }

    destination = ROOT / f"dict{source_path.name}"

    # Refuse to silently overwrite an earlier conversion.
    if destination.exists():
        print(f"  SKIPPED: {destination.name} already exists")
        continue

    with destination.open("w", encoding="utf-8") as file:
        json.dump(converted, file, ensure_ascii=False, indent=2)

    print(f"  Created {destination.name} with {len(converted)} characters")

print("Conversion finished.")
