import pandas as pd
from src.preprocessing.process_severity import process_severity

def main():
    df = pd.read_csv("dataset/raw/severity_synthetic.csv")
    processed = process_severity(df)
    processed.to_csv("dataset/cleaned/severity_cleaned.csv", index=False)

    print("\nSeverity cleaned dataset saved!")
    print(processed.head())
    print(processed.shape, "\n")

if __name__ == "__main__":
    main()
