# REDCap–Epic Patient Data Merger

This Python script merges patient data from two separate Excel/CSV spreadsheets:

1. **REDCap report** (must be selected first)
2. **CS-Link/Epic export** (must be selected second)

The script matches patients based on **First Name**, **Last Name**, and **Appointment Date**, and intelligently handles slight differences in name spelling by using a fuzzy matching algorithm (4+ consecutive matching letters). Only rows from the **REDCap spreadsheet** are included in the final output, with matching diagnosis and cognitive data pulled in from Epic.

---

## 🚀 Features

- 🧠 Fuzzy name matching (4-letter consecutive match)
- 📅 Robust date format standardization
- 🔗 Combines $Dx Code$ and $Cognitive Impairment$ fields (semicolon-separated)
- 🧹 Keeps only REDCap patient records
- 🧾 Capitalizes names for cleaner output
- 💾 Outputs merged file as `merged.csv`


## Requirements

- Python 3.7 or later
- `pandas` and `openpyxl` libraries

---

## Installation Instructions

### 🪟 Windows

#### 1. Install Python

- Go to the official Python website: [https://www.python.org/downloads/windows](https://www.python.org/downloads/windows)
- Download the latest version (Python 3.x)
- Run the installer and **check the box that says "Add Python to PATH"**
- Click **Install Now**

To verify Python is installed, open Command Prompt and run:
```
python --version
```

#### 2. Install required packages

In Command Prompt, run:
```
pip install pandas openpyxl
```

---

### 🍎 macOS

#### 1. Install Python

Open the **Terminal** app (press `Cmd + Space`, type `Terminal`, hit Enter)

Check if Python is already installed:
```
python3 --version
```

If not installed, install Homebrew first (if needed):
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install Python:
```
brew install python
```

#### 2. Install required packages

Run:
```
pip3 install pandas openpyxl
```

---

## How to Run the Script

1. **Open Terminal (macOS) or Command Prompt (Windows).**

2. **Navigate to the folder where your `merger.py` script is saved.**

- On **Windows**, if your script is in `C:\Users\YourName\Documents\`: cd C:\Users\YourName\Documents


- On **macOS**, if your script is in `/Users/yourname/Documents/`: cd /Users/yourname/Documents


3. **Run the script:**

- On **Windows**:
``
python merger.py
``

- On **macOS**:
``
python3 merger.py
``

4. A file dialog window will open. Select your REDCap CSV or Excel file.

5. The script will create a new file with the same name but ending with `_merged.csv` in the same folder.

---

## Example

Before (multiple rows per patient):

| Record ID | Repeat Instrument      | First Name | Last Name | Age | DOB     |
|-----------|------------------------|------------|-----------|-----|---------|
| 125       |                        | John       | Doe       |     |         |
| 125       | Survey                 |            |           | 52  | 4/12/53 |
| 125       | Patient Assessments    |            |           |     |         |

After (merged into one row):

| Record ID | Repeat Instrument | First Name | Last Name | Age | DOB     |
|-----------|-------------------|------------|-----------|-----|---------|
| 125       | Survey            | John       | Doe       | 52  | 4/12/53 |

---

## Notes

- Your input file must contain a column named exactly: `Record ID`
- Column headers with extra spaces will be cleaned automatically
- Output file is saved in the same folder as the input file
- If reading Excel files, `openpyxl` is required

---

## License

MIT License — free for personal or commercial use.
```
