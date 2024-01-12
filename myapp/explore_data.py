import pandas as pd
import re
import logging
from pathlib import Path

from myapp.db_operations import data_already_loaded, insert_summary_data, insert_detailed_data
from myapp.database import create_db_and_tables

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Helper functions
def to_snake_case(name: str) -> str:
    """Converts a string to snake_case."""
    return re.sub(r'\W+', '_', name).lower()

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from an Excel file into a Pandas DataFrame.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        logging.error(f"Error occurred while reading the file: {e}")
        return pd.DataFrame()

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess data by dropping empty columns and renaming columns."""
    df.dropna(axis=1, how='all', inplace=True)
    df.columns = [to_snake_case(col) for col in df.columns]
    return df.rename(columns={
        'franch_base_name': 'base_name',
        'french_unit': 'unit',
        'french_attribute_name': 'attribute_name',
        'elemnt_id': 'id',
        'french_tags': 'tags',
        'french_comment': 'comment',
        'french_emission_type_name': 'emission_type_name',
        'other_french_name': 'other_name'
    })

def handle_uncertainty(df: pd.DataFrame) -> pd.DataFrame:
    """Handle and clean the 'uncertainty' column in the DataFrame, dropping rows where uncertainty is equal to or above 100%."""
    df['uncertainty'] = df['uncertainty'].str.replace('%', '').astype(float) / 100
    df.drop(df[df['uncertainty'] >= 1].index, inplace=True)
    return df

def convert_date_language(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date language to English."""
    french_to_english = {
    'Janvier': 'January',
    'Février': 'February', 'Fevrier': 'February',
    'Mars': 'March',
    'Avril': 'April',
    'Mai': 'May',
    'Juin': 'June',
    'Juillet': 'July',
    'Août': 'August', 'Aout': 'August',
    'Septembre': 'September',
    'Octobre': 'October',
    'Novembre': 'November',
    'Décembre': 'December', 'Decembre': 'December'
    }

    date_columns = ['creation_date', 'last_update_date', 'validity_period']
    for col in date_columns:
        df[col] = df[col].str.title().replace(french_to_english, regex=True)
    return df

def calculate_validity_period(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the average validity period and apply it to the DataFrame."""
    temp_df = df.copy()
    temp_df['validity_period_converted'] = pd.to_datetime(temp_df['validity_period'], format='%B %Y', errors='coerce')
    temp_df['validity_delta'] = (temp_df['validity_period_converted'] - temp_df['creation_date']).dt.days
    average_validity_days = temp_df['validity_delta'].dropna().mean()
    average_validity_months = round(average_validity_days / 30)
    df['validity_period'] = df['creation_date'] + pd.DateOffset(months=average_validity_months)
    return df

def update_gas_values(df: pd.DataFrame) -> pd.DataFrame:
    """Update gas values based on conditions. sf6 has it's own column and divers values are mixed into the other_greenhouse_gas column"""
    df['sf6'] = df.apply(lambda row: row['additional_gaz_value_1'] if row['additional_gaz_1'] == 'sf6' else 0, axis=1)
    df['other_greenhouse_gas'] = df.apply(
        lambda row: row['other_greenhouse_gas'] + row['additional_gaz_value_1'] if row['additional_gaz_1'] == 'divers' else row['other_greenhouse_gas'],
        axis=1
    )
    return df.drop(['additional_gaz_1', 'additional_gaz_value_1'], axis=1)

def handle_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing data and fill NaNs."""
    df['emission_type'] = df['emission_type'].fillna('Toutes')
    emission_columns = ['co2f', 'ch4f', 'ch4b', 'n2o', 'sf6', 'other_greenhouse_gas', 'co2b']
    for col in emission_columns:
        df[col] = df[col].fillna(0)
    df['sub_location'] = df['sub_location'].fillna(df['location'])
    df['unit'] = df['unit'].fillna('undefined')

    return df



def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert and clean data types."""
    df['unit'] = df['unit'].str.lower().str.strip()
    categorical_columns = ['line_type', 'element_status', 'category_code', 'unit', 'location', 'emission_type', 'sub_location']
    for col in categorical_columns:
        df[col] = df[col].astype('category')
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        df[col] = df[col].str.strip().str.lower()
    return df

def convert_columns_to_string(df, string_columns):
    """
    Convert the specified columns of a DataFrame to strings.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        string_columns (list of str): List of column names to convert to strings.
    """
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)
        else:
            logging.warning(f"Warning: Column '{col}' not found in DataFrame")
    return df

def validate_data(df: pd.DataFrame):
    """
    Perform data validation checks on the main DataFrame before splitting.
    """
    warnings_issued = False
    # Check for high uncertainty values (e.g., greater than 100%)
    if df['uncertainty'].gt(1).any():
        logging.warning("Warning: Uncertainty values greater than 100% found.")
        warnings_issued = True

    # Check for unexpected NaN values in date columns
    for col in ['creation_date', 'last_update_date', 'validity_period']:
        if df[col].isna().any():
            logging.warning(f"Warning: NaN values found in {col}")
            warnings_issued = True
    # Check for date range validity
    if not df['creation_date'].le(df['validity_period']).all():
        logging.warning("Warning: 'validity_period' dates precede 'creation_date'")
        warnings_issued = True
    # Check for duplicates
    if df.duplicated().any():
        logging.warning("Warning: Duplicate rows found")
        warnings_issued = True

    # List of columns that should not allow missing values
    non_missing_columns = [
        'structure',
        'element_status',
        'base_name',
        'category_code',
        'unit',
        'creation_date',
        'last_update_date',
        'validity_period',
        'emission_type',
        'unaggregated_total',
        'co2f',
        'ch4f',
        'ch4b',
        'n2o',
        'other_greenhouse_gas',
        'co2b',
        'sf6'
    ]
    missing_values = df[non_missing_columns].isnull().sum()
    missing_columns = missing_values[missing_values > 0]
    if not missing_columns.empty:
        logging.warning("Columns with missing values:")
        logging.info(missing_columns)
        warnings_issued = True

    if not warnings_issued:
        logging.info("No validation warnings")

def split_data(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    Splits the data into summary and detailed DataFrames, converting unique 'Poste' rows to 'Elément' where necessary.

    Args:
        df (pd.DataFrame): The original DataFrame.

    Returns:
        summary_df (pd.DataFrame): DataFrame containing summary data.
        detailed_df (pd.DataFrame): DataFrame containing detailed data.
    """
    # Columns to sum
    sum_columns = ['unaggregated_total', 'co2f', 'ch4f', 'ch4b', 'n2o', 'sf6', 'other_greenhouse_gas', 'co2b']

    # Identify 'Poste' rows that are unique (no corresponding 'Elément')
    poste_rows = df[df['line_type'] == 'Poste']
    element_rows = df[df['line_type'] == 'Elément']

    # Initialize summary dataframe
    summary_df = element_rows.copy(deep=True)

    # Identify rows in poste_rows with unique IDs, transform them and add them to the summary_df
    unique_poste_rows = df[(df['line_type'] == 'Poste') & ~df['id'].duplicated(keep=False)]
    unique_poste_rows['line_type'] = 'Elément'
    summary_df = pd.concat([summary_df, unique_poste_rows])
    poste_rows = poste_rows.drop(unique_poste_rows.index)

    data_types = {col: dtype for col, dtype in summary_df.dtypes.items()}
    new_rows_summary = pd.DataFrame(columns=df.columns).astype(data_types)

    # Identify 'Poste' row groups that don't have a 'Elément' row and create one
    grouped_poste_rows = poste_rows.groupby('id')

    for group_id, group_data in grouped_poste_rows:
        if group_id not in element_rows['id'].values:
            new_row = group_data.iloc[0].copy()
            new_row['line_type'] = 'Elément'

            # Aggregate the sum_columns for the current group
            for col in sum_columns:
                new_row[col] = group_data[col].sum()
            # Concatenate the new row to new_rows_summary
            new_rows_summary.loc[len(new_rows_summary)] = new_row

    # Concatenate new_rows_summary with summary_df
    summary_df = pd.concat([summary_df, new_rows_summary], ignore_index=True).astype(data_types)

    summary_df.info()

    detailed_df = poste_rows.copy(deep = True)

    # Drop the 'line_type' column and reset index
    summary_df.drop(['line_type'], axis=1, inplace=True)
    detailed_df.drop(['line_type'], axis=1, inplace=True)

    summary_df.reset_index(drop=True, inplace=True)
    detailed_df.reset_index(drop=True, inplace=True)

    return summary_df, detailed_df

def validate_split_dataframes(df_detailed: pd.DataFrame, df_summary: pd.DataFrame) -> bool:
    """
    Checks that every row in the summary DataFrame has a unique id and then validates that every 'id' in the detailed DataFrame corresponds to an 'id' in the summary DataFrame.

    Lists the rows from summary DataFrame that are not unique and detailed DataFrame that do not have a corresponding summary entry.

    Args:
        df_detailed (pd.DataFrame): The detailed DataFrame.
        df_summary (pd.DataFrame): The summary DataFrame.

    Returns:
        bool: True if all 'id' values are valid, False otherwise.
    """

    duplicate_ids = df_summary[df_summary['id'].duplicated()]['id'].unique()
    if len(duplicate_ids) > 0:
        logging.warning("Repeated Element ids found:", duplicate_ids)

    mask = ~df_detailed['id'].isin(df_summary['id'])
    invalid_detailed_rows = df_detailed[mask]

    if not invalid_detailed_rows.empty:
        logging.warning("The following detailed data entries do not have a corresponding summary data entry:")
        logging.info(invalid_detailed_rows)
        return False


def process_and_load_data() -> None:
    """
    Main function to process and load data into the database.
    """

    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "data" / "data.xlsx"

    if data_already_loaded():
        logging.info("Data is already loaded in the database.")
        return

    df = load_data(data_path)

    logging.info("Processing data")

    df = preprocess_data(df)

    df = handle_uncertainty(df)

    df = convert_date_language(df)
    df['creation_date'] = pd.to_datetime(df['creation_date'], format='%B %Y', errors='coerce')
    df['last_update_date'] = pd.to_datetime(df['last_update_date'], format='%B %Y', errors='coerce')
    df['last_update_date'] = df['last_update_date'].fillna(df['creation_date'])
    df = calculate_validity_period(df)

    df = update_gas_values(df)

    df = handle_missing_data(df)

    df = convert_data_types(df)

    string_columns = ['attribute_name', 'other_name', 'tags', 'contributor', 'program', 'program_url', 'source', 'location', 'sub_location', 'comment', 'emission_type', 'emission_type_name']
    df = convert_columns_to_string(df, string_columns)

    validate_data(df)

    summary_df, detailed_df = split_data(df)
    validate_split_dataframes(detailed_df, summary_df)

    logging.info("Result data:")

    detailed_df.info()
    summary_df.info()

    logging.info('Inserting data into postgresql database')

    insert_summary_data(summary_df)
    insert_detailed_data(detailed_df)

    logging.info('Data successfully inserted')

if __name__ == "__main__":
    process_and_load_data()