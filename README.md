# Cardmarket to Moxfield CSV Converter

This Python script fetches card data from the Scryfall API using Cardmarket IDs from a Cardmarket input CSV file, and writes the matched card data to an output CSV file that can be used to import into Moxfield. If a Cardmarket ID from the input CSV file is not found in the Scryfall API, it is written to a text file.

## Requirements

- Python 3.6 or higher
- `requests` module

You can install the `requests` module using pip: `pip install requests`

## Usage

1. Prepare your input CSV file with the following columns (other columns will be ignored):
   - idProduct: The Cardmarket ID of the card.
   - groupCount: The quantity of the card.
   - idLanguage: The language code of the card.
   - isFoil: Whether the card is a foil card. '1' for yes, '0' for no.
   - isAltered: Whether the card is altered. 'true' for yes, 'false' for no.
   - condition: The condition of the card. Possible values are 'MT', 'NM', 'EX', 'GD', 'LP', 'PL', 'PO'. Anything else will default to `NM`
   - price: The purchase price of the card.
2. Run the script:

   - `python convert.py`

3. The script will create a Moxfield-formatted output CSV file with the matched card data. The columns in the output CSV file are:
   - Count
   - Name
   - Edition
   - Language
   - Foil
   - Collector Number
   - Alter
   - Condition
   - Purchase Price
4. If there are Cardmarket IDs from the input CSV file that are not found in Scryfall's database, they will be written to a text file.

## Notes

- You must have input.csv in the same folder as convert.py before running the script.
- The script includes a delay of 100 milliseconds between each API request to the Scryfall API to prevent rate limiting.
- The script uses UTF-8 encoding to read and write files.
- If the output CSV file or the missing Cardmarket IDs text file already exist, the script will create a new file with a numbered suffix instead of overwriting the existing file.
