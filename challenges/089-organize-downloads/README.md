# Challenge 089: Organize Downloads

## Difficulty: Easy

## Task

The file `setup/organizer.py` contains a stub. Implement a function that organizes files from a source directory into categorized subdirectories within a target directory.

## Requirements

1. `organize(source_dir, target_dir) -> dict` -- Move files from `source_dir` into subdirectories of `target_dir` based on file extension category. Return a dict mapping each category name to a list of filenames moved into it.

### Categories

| Category     | Extensions                          |
|-------------|-------------------------------------|
| documents   | .pdf, .txt, .md, .docx, .pptx, .xlsx |
| images      | .jpg, .png, .gif, .svg              |
| code        | .py, .js, .css, .html               |
| media       | .mp3, .mp4, .wav                    |
| data        | .csv, .json, .xml                   |
| archives    | .zip, .tar, .gz                     |
| other       | anything else                       |

### Behavior

- Create target subdirectories as needed.
- Move (not copy) each file into the appropriate category subdirectory.
- If a file's extension does not match any category, place it in `other/`.
- Return a dict where keys are category names and values are sorted lists of filenames placed in that category. Only include categories that received at least one file.

## Rules

- Only modify files in the `setup/` directory.
- Use only the Python standard library.

## Example

```python
result = organize("downloads/", "organized/")
# {
#     "documents": ["notes.txt", "report.pdf"],
#     "images": ["diagram.png", "photo.jpg"],
#     "code": ["index.html", "script.py", "style.css"],
#     ...
# }
```
