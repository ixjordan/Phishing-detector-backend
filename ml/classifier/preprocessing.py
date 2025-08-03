import pandas as pd
import os

def clean_csv(input_path:str, output_path:str):
    """
    Cleans a CSV file by normalizing labels, removing unnecessary columns, and cleaning text data.
    Args:
        input_path (str): Path to the input CSV file.
    Returns:
        Will save to cleanedcsv file in the ml/datasets directory.
    """
    try:

        # Check if the input path is a valid file
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"File not found: {input_path}")
        return None
     
    except pd.errors.EmptyDataError:
        print(f"File is empty: {input_path}")
        return None
    except pd.errors.ParserError:
        print(f"Error parsing file: {input_path}")
        return None

    df = df[["LABEL", "TEXT"]]

    # normalise tables - change labels to either 1 if smishing/spam or 0 if ham
    df["LABEL"] = df["LABEL"].str.lower().map({
        "ham": 0,
        "smishing": 1,
        "spam":1
        })
    
    df = df.dropna(subset=["LABEL"])
    df = df.dropna(subset=["TEXT"])
    df = df[df["TEXT"].str.strip() != ""]


    df["TEXT"] = df["TEXT"].str.replace(r"\s+", " ",regex=True).str.strip().str.lower()

    # Save cleaned dataset to a new CSV file
    output_dir = "ml/datasets"
    os.makedirs(output_dir, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to {output_path}")
    
    # return dataframe
    return df


def clean_text(input_path):
    pass


if __name__ == "__main__":
    input_path = "/Users/jordancroft/Documents/Documents - Jordan.’s MacBook Air/GitHub/Phishing-detector-backend/ml/datasets/Dataset_5971.csv"
    output_path = "ml/datasets/cleaned_dataset.csv"
    # Call the clean_csv function with the input path
    df = clean_csv(input_path, output_path)

    print(df.head())