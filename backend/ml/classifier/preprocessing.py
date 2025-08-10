import pandas as pd
import os
from sklearn.model_selection import train_test_split

def clean_csv(input_path:str, output_dir:str="ml/datasets/cleaned_dataset.csv"):
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

    # count the number of ham and smishing messages
    label_counts = df["LABEL"].value_counts()
    print("***Label counts for DATASET 1***:")
    print(f"Ham (0): {label_counts.get(0, 0)}")
    print(f"Smishing (1): {label_counts.get(1, 0)}")

    
    # return dataframe
    return df


def txt_to_csv(input_path):
    """
    clens a text file containing SMS messages, normalizes labels, and saves the cleaned data to a CSV file.
    Args:
        input_path (str): Path to the input text file.
    Returns:
        DataFrame: A pandas DataFrame containing the cleaned data.
    Will save to cleaned/txt_cleaned.csv
    """
    df = None
    dict = []
    try:
        # read txt file 
        with open(input_path, 'r', encoding='utf-8') as file:
            for line in file:
                # strip spaces from each line 
                line = line.strip()

                # skip empty lines
                if not line:
                    continue
                
                # split line into label and text
                try:
                    label, text = line.split('\t', 1)
                    label = 1 if label.lower() == 'smish' else 0
                    dict.append({'LABEL': label, 'TEXT': text})
                except ValueError:
                    print(f"Skipping line due to ValueError: {line}")
    
        # Convert list of dictionaries to DataFrame & clean text
        df = pd.DataFrame(dict)
        df = df[df["TEXT"].str.strip() != ""]
        df["TEXT"] = df["TEXT"].str.replace(r"\s+", " ",regex=True).str.strip().str.lower()

        # vount the number of ham and smishing messages
        print("***Label counts for DATASET 2***:")
        label_counts = df["LABEL"].value_counts()
        print(f"Ham (0): {label_counts.get(0, 0)}")
        print(f"Smishing (1): {label_counts.get(1, 0)}")


    except Exception as e:
        print(f"An error occurred while cleaning text: {e}")
    

    return df


def merge_datasets():
    """
    Merges two DataFrames and returns the combined DataFrame.
    Args:
        df1 (DataFrame): First DataFrame.
        df2 (DataFrame): Second DataFrame.
    Returns:
        DataFrame: Combined DataFrame.
    """

    # call clean functions on two datasets
    csv_df = clean_csv("/Users/jordancroft/Documents/Documents - Jordan.’s MacBook Air/GitHub/Phishing-detector-backend/ml/datasets/Dataset_5971.csv")
    txt_df = txt_to_csv("/Users/jordancroft/Documents/Documents - Jordan.’s MacBook Air/GitHub/Phishing-detector-backend/ml/datasets/SMSSmishCollection.txt")

    if csv_df is not None and txt_df is not None:
        csv_df.columns = csv_df.columns.str.upper()
        txt_df.columns = txt_df.columns.str.upper()

        # merge both datasets
        combined_df = pd.concat([csv_df, txt_df], ignore_index=True)
        # remove duplicates based on TEXT column
        combined_df = combined_df.drop_duplicates(subset=["TEXT"], keep='first')

        # reset index
        combined_df = combined_df.sample(frac=1).reset_index(drop=True)

        # write combined set to csv file for splitting later
        combined_df.to_csv("cleaned/combined_dataset.csv", index=False)
        print("Datasets merged and saved to ml/datasets/combined_dataset.csv")

        print(f"Merged dataset saved with {len(combined_df)} rows.")
        label_counts = combined_df["LABEL"].value_counts()
        print(f"Ham (0): {label_counts.get(0, 0)}")
        print(f"Smishing (1): {label_counts.get(1, 0)}")
        return combined_df
    else:
        print("One or both datasets are empty. Cannot merge.")
        return None


def split_dataset():
    """
    splits a DataFrame into training and testing sets.
    Args:
        df (DataFrame): DataFrame to split.
    Returns:
        DataFrame: Training set.
        DataFrame: Testing set.
    """

    # load dataset 
    df = pd.read_csv("cleaned/combined_dataset.csv")

    # split dataset into trainging and test sets
    train_df, temp_df = train_test_split(
        df,
        test_size=0.2,  # 20% for validation and testing
        random_state=42,  # For reproducibility
        stratify=df["LABEL"]  # Ensure the same proportion of labels in both sets
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,  # Split the remaining 20% into 10% validation and 10% testing
        random_state=42,
        stratify=temp_df["LABEL"]
    )

    # Save the datasets to CSV files
    os.makedirs("cleaned", exist_ok=True)  # Ensure the directory exists
    print("Saving datasets to cleaned directory...")
    train_df.to_csv("cleaned/train_dataset.csv", index=False)
    val_df.to_csv("cleaned/val_dataset.csv", index=False)
    test_df.to_csv("cleaned/test_dataset.csv", index=False)

    print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    print("Class balance in train set: \n", train_df["LABEL"].value_counts(normalize=True))



if __name__ == "__main__":
    # csv_input = "/Users/jordancroft/Documents/Documents - Jordan.’s MacBook Air/GitHub/Phishing-detector-backend/ml/datasets/Dataset_5971.csv"
    # csv_output = "cleaned/cleaned_dataset.csv"
    # df_csv = clean_csv(csv_input, csv_output)

    # txt_input = "/Users/jordancroft/Documents/Documents - Jordan.’s MacBook Air/GitHub/Phishing-detector-backend/ml/datasets/SMSSmishCollection.txt"
    # df_txt = txt_to_csv(txt_input)

    # print(df_csv.head())
    # print(df_txt.head())
    # print("Preprocessing complete.")
    # merge_datasets()

    split_dataset()



