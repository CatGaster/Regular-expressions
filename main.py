import csv 
import re
from pprint import pprint

def read_file(name):
    with open ("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def split_name(names_list):
    full_name = ["", "", ""]
    start = 0
    for name in names_list:
        if name:
            name = name.split()
            stop = len(name)
            full_name[start:start + stop] = name
            start += stop
    return full_name


def remove_duplicates(contacts_list):
    result_dict = {}
    for row in contacts_list:
        key = row[0], row[1]
        data_dict = {'surname': row[2], 'organization': row[3], 'position': row[4], 'phone': row[5], 'email': row[6]}
        if result_dict.get(key):
            for value in result_dict.get(key):
                if row[2] in value.get('surname'):
                    value.update({key: data_dict.get(key) for key in value if not value.get(key)})
                else:
                    result_dict.get(key).append(data_dict)
        else:
            result_dict[key] = [data_dict]
    return result_dict


def extract_names(contacts_list):

    for row in contacts_list:
        row[:3] = split_name(row[:3])
    return contacts_list


def write_contacts(result_dict, header):
    with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
        datawriter = csv.DictWriter(f, fieldnames=header, delimiter=',')
        datawriter.writeheader()
        for key, value_list in result_dict.items():
            for value in value_list:
                datawriter.writerow({'lastname': key[0], 'firstname': key[1], 'surname': value.get('surname'),
                                     'organization': value.get('organization'), 'position': value.get('position'),
                                     'phone': value.get('phone'), 'email': value.get('email')}
                                    )
        

def fix_phone():

    with open("phonebook.csv", encoding="utf-8") as f:
        read_file = f.read()

    sub_pattern = r'+7(\2)\3-\4-\5\6\7\8'
    pattern = re.compile(r"(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})(\s*)\(?(доб\.)*[\s]*(\d+)*[\)]*")
    result = pattern.sub(sub_pattern, read_file)
    with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
        f.write(result)


if __name__ == '__main__':
    NAME = 'phonebook_raw.csv'
    contacts_list = read_file(NAME)
    extract_names(contacts_list[1:])
    remove_duplicates_dict = remove_duplicates(contacts_list[1:])
    header = contacts_list[0]
    write_contacts(remove_duplicates_dict, header)
    fix_phone()



