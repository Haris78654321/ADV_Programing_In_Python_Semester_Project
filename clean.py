import pandas as pd

def load_and_clean_data(file_path="CARS_COUNTRY.xlsx"):
    df = pd.read_excel(file_path, sheet_name="data")
    
    # Standardize column names (remove extra spaces and ensure consistent capitalization)
    df.columns = df.columns.str.strip()
    
    # Convert Year to numeric
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    
    # Ensure numeric columns are properly typed
    numeric_cols = ['Engine HP', 'city mpg', 'highway MPG', 
                   'Engine Cylinders', 'Popularity', 'Number of Doors',
                   'MSRP']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Clean categorical columns
    cat_cols = ["Origin", "Make", "Model", "Engine Fuel Type", 
               "Transmission Type", "Driven_Wheels", "Market Category", 
               "Vehicle Size", "Vehicle Style"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)
    
    return df