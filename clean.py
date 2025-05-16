import pandas as pd

def load_and_clean_data(file_path="CARS_COUNTRY.xlsx"):
    df = pd.read_excel(file_path, sheet_name="data")

    # Drop rows with missing essential numeric values
    df = df.dropna(subset=["Engine HP", "Engine Cylinders", "Number of Doors"])

    cat_cols = [
        "Origin", "Make", "Model", "Engine Fuel Type", "Transmission Type",
        "Driven_Wheels", "Market Category", "Vehicle Size", "Vehicle Style"
    ]

    for col in cat_cols:
        df[col] = df[col].astype(str)      # Convert all values to string first
        df[col] = df[col].astype(object)   # Then convert dtype from category to object

    # Also convert Year and Popularity to string + object dtype
    df["Year"] = df["Year"].astype(str)
    df["Year"] = df["Year"].astype(object)

    df["Popularity"] = df["Popularity"].astype(str)
    df["Popularity"] = df["Popularity"].astype(object)

    return df
