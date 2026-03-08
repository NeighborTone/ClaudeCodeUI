---
name: read-excel
description: Read Excel files using openpyxl
---

# Read Excel File

## Usage
```
/read-excel <file_path> [--sheet <name>] [--range <A1:Z100>]
```

## Description
Read Excel files (.xlsx) using openpyxl and output as text.

## Implementation

```python
import openpyxl
import sys

file_path = sys.argv[1]
sheet_name = None  # parse from args if provided
cell_range = None  # parse from args if provided

wb = openpyxl.load_workbook(file_path, data_only=True)

if sheet_name:
    ws = wb[sheet_name]
else:
    ws = wb.active

print(f"Sheets: {wb.sheetnames}")
print(f"Active: {ws.title}")
print()

for row in ws.iter_rows(values_only=False):
    values = [str(cell.value) if cell.value is not None else "" for cell in row]
    print(f"{row[0].row}\t" + "\t".join(values))
```

## Requirements
- Python 3.x
- openpyxl (`pip install openpyxl`)
