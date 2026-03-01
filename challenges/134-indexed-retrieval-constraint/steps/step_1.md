# Step 1: Build the Index

The directory `setup/data/` contains 20 JSON files named `record_01.json` through `record_20.json`.

Each file has the following structure:

```json
{
  "id": 1,
  "category": "A",
  "value": 12
}
```

Each record belongs to one of three categories: `"A"`, `"B"`, or `"C"`.

Your task: Read all 20 files and build an index in `setup/index.json` that maps each category to a list of filenames that contain records of that category.

**Important:** The index should contain only filenames, NOT the full file contents or values. For example:

```json
{
  "A": ["record_01.json", "record_04.json"],
  "B": ["record_02.json", "record_07.json"],
  "C": ["record_03.json", "record_05.json"]
}
```

Do NOT modify any of the record files in `setup/data/`.
