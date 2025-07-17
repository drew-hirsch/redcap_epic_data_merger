import pandas as pd
from tkinter import Tk, filedialog
from datetime import datetime
import re

def standardize_date(date_str):
    """Try to parse date from various formats; return yyyy-mm-dd or None if fail."""
    if pd.isna(date_str):
        return None
    # If input includes time and other text, strip to just date (first part)
    date_part = str(date_str).split()[0]  # get first chunk before space
    # For second file, extract date from '10/19/2023 14:00 - Jennifer ...'
    # Regex for MM/DD/YYYY at start of string
    m = re.match(r"(\d{1,2}/\d{1,2}/\d{4})", str(date_str))
    if m:
        date_part = m.group(1)
    for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%m/%d/%y", "%m-%d-%y"):
        try:
            dt = datetime.strptime(date_part, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

def load_and_standardize(file_path, is_first_file):
    df = pd.read_csv(file_path)

    # Map names for consistency
    col_map = {
        "First Name": "First Name",
        "Last Name": "Last Name",
        "Patient's first name": "First Name",
        "Patient's last name": "Last Name",
    }
    df.rename(columns=col_map, inplace=True)

    # Select and rename date column
    if is_first_file:
        if "Date of appointment" in df.columns:
            df.rename(columns={"Date of appointment": "Date"}, inplace=True)
        else:
            raise ValueError("First file must have 'Date of appointment' column")
    else:
        if "Last Visit in Neuro" in df.columns:
            df.rename(columns={"Last Visit in Neuro": "Date"}, inplace=True)
        else:
            raise ValueError("Second file must have 'Last Visit in Neuro' column")

    # Clean names
    df["First Name"] = df["First Name"].astype(str).str.strip().str.lower()
    df["Last Name"] = df["Last Name"].astype(str).str.strip().str.lower()

    # Standardize dates
    df["Date"] = df["Date"].apply(standardize_date)

    return df

def name_match(name1, name2):
    for i in range(len(name1) - 3):
        if name1[i:i+4] in name2:
            return True
    return False

def append_matching_info(primary_df, secondary_df):
    appended_rows = []

    # Identify extra columns in secondary_df (excluding names and date)
    base_columns = {"First Name", "Last Name", "Date"}
    extra_columns = [col for col in secondary_df.columns if col not in base_columns]

    for _, row in primary_df.iterrows():
        fn1 = row["First Name"]
        ln1 = row["Last Name"]
        date1 = row["Date"]

        if pd.notna(date1):
            matches = secondary_df[
                (secondary_df["Date"] == date1) &
                (secondary_df["First Name"].apply(lambda fn2: name_match(fn1, fn2))) &
                (secondary_df["Last Name"].apply(lambda ln2: name_match(ln1, ln2)))
            ]
        else:
            matches = secondary_df[
                (secondary_df["First Name"] == fn1) &
                (secondary_df["Last Name"] == ln1)
            ]

        enriched_row = row.copy()

        # For each extra column, gather all unique values from matches
        for col in extra_columns:
            values = set()
            for _, match_row in matches.iterrows():
                if col in match_row and pd.notna(match_row[col]):
                    values.update(map(str.strip, str(match_row[col]).split(';')))
            enriched_row[col] = '; '.join(sorted(values)) if values else ""

        appended_rows.append(enriched_row)

    enriched_df = pd.DataFrame(appended_rows)

    # Capitalize names
    enriched_df["First Name"] = enriched_df["First Name"].str.title()
    enriched_df["Last Name"] = enriched_df["Last Name"].str.title()

    return enriched_df


def main():
    Tk().withdraw()

    print("Select the FIRST file (with 'Date of appointment'):")
    file1 = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    print("Select the SECOND file (with 'Last Visit in Neuro'):")
    file2 = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    df1 = load_and_standardize(file1, is_first_file=True)
    df2 = load_and_standardize(file2, is_first_file=False)

    final_df = append_matching_info(df1, df2)

    final_df.to_csv("merged.csv", index=False)
    print("✅ Merged file saved as 'merged.csv'.")

if __name__ == "__main__":
    main()
