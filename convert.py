import csv
import requests
import os
import time

# Define a function to convert language code to language name
def get_language_name(code):
    languages = {
        '1': 'English',
        '2': 'French',
        '3': 'German',
        '4': 'Spanish',
        '5': 'Italian',
        '6': 'Simplified Chinese',
        '7': 'Japanese',
        '8': 'Portuguese',
        '9': 'Russian',
        '10': 'Korean',
        '11': 'Traditional Chinese'
    }
    return languages.get(code, '')

# Define a function to convert condition code to condition name
def get_condition_name(code):
    conditions = {
        'MT': 'M',
        'NM': 'NM',
        'EX': 'LP',
        'GD': 'LP',
        'LP': 'MP',
        'PL': 'HP',
        'PO': 'D'
    }
    return conditions.get(code, 'NM')

# Define a function to get a unique filename
def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    i = 1
    while os.path.exists(filename):
        filename = f"{base}_{i}{ext}"
        i += 1
    return filename

print("Loading the input CSV...")
try:
    with open('input.csv', 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        if 'idProduct' not in reader.fieldnames:
            raise ValueError('idProduct column missing in input.csv')
        input_data = list(reader)
except FileNotFoundError:
    print('input.csv file is missing')
    input_data = []

output_filename = get_unique_filename('output.csv')
with open(output_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Count', 'Name', 'Edition', 'Language', 'Foil', 'Collector Number', 'Alter', 'Condition', 'Purchase Price'], delimiter=',')
    writer.writeheader()
    missing_ids = []
    for row in input_data:
        print(f"Checking Cardmarket ID: {row['idProduct']}...")
        response = requests.get(f'https://api.scryfall.com/cards/cardmarket/{row["idProduct"]}')
        if response.status_code == 200:
            card = response.json()
            writer.writerow({
                'Count': row['groupCount'] if 'groupCount' in row else '',
                'Name': card['name'],
                'Edition': card['set'],
                'Language': get_language_name(row['idLanguage']) if 'idLanguage' in row else '',
                'Foil': 'etched' if 'isFoil' in row and row['isFoil'] == '1' and 'etched' in card['finishes'] and 'foil' not in card['finishes'] else 'foil' if 'isFoil' in row and row['isFoil'] == '1' else '',
                'Collector Number': card['collector_number'],
                'Alter': 'TRUE' if 'isAltered' in row and row['isAltered'] == 'true' else 'FALSE',
                'Condition': get_condition_name(row['condition']) if 'condition' in row else 'NM',
                'Purchase Price': row['price'] if 'price' in row else ''
            })
        else:
            print(f"Cardmarket ID {row['idProduct']} not found.")
            missing_ids.append(row['idProduct'])
        time.sleep(0.1)  # delay for 100 milliseconds

# Write the missing IDs to a text file only if there are missing IDs
if missing_ids:
    print("Writing the missing IDs to a text file...")
    missing_ids_filename = get_unique_filename('missing_cardmarket_ids.txt')
    with open(missing_ids_filename, 'w') as f:
        for id in missing_ids:
            f.write(f'{id}\n')

print("Finished!")
