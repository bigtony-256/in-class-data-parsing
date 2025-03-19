import csv
import json
import xml.etree.ElementTree as ET
import re



def read(filename):
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            return [line.strip().split('\t') for line in file]
    except UnicodeDecodeError:
        with open(filename, 'r', newline='', encoding='ISO-8859-1') as file:
            return [line.strip().split('\t') for line in file]


def write_csv(data, output_filename):
    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def write_json(data, output_filename):
    keys = [sanitize_key(key) for key in data[0]]
    json_data = [dict(zip(keys, row)) for row in data[1:]]
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)


def sanitize_key(key): # XML breaks very easily and won't display without many failsafes
    key = re.sub(r'[^a-zA-Z0-9_]', '_', key)
    return f'_{key}' if key[0].isdigit() else key

def write_xml(data, output_filename):
    root = ET.Element("root")
    keys = [sanitize_key(key) for key in data[0]] # Checking illegal characters
    for row in data[1:]:
        item = ET.SubElement(root, "item")
        for key, value in zip(keys, row):
            if value.strip() and value != "#N/A":
                ET.SubElement(item, key).text = value
            else:
                ET.SubElement(item, key).text = "N/A"
    tree = ET.ElementTree(root)
    tree.write(output_filename, encoding='utf-8', xml_declaration=True)


def main():
    filename = input("Enter file name: ")
    format_option = input("Enter format (-c, -x, -j): ")
    data = read(filename)

    if format_option == '-c':
        output_filename = filename.rsplit('.', 1)[0] + '.csv'
        write_csv(data, output_filename)
    elif format_option == '-j':
        output_filename = filename.rsplit('.', 1)[0] + '.json'
        write_json(data, output_filename)
    elif format_option == '-x':
        output_filename = filename.rsplit('.', 1)[0] + '.xml'
        write_xml(data, output_filename)
    else:
        print("Invalid format ")
        return

    print(f"Conversion successful: {output_filename}")


if __name__ == "__main__":
    main()