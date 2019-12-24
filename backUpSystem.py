#!/usr/bin/env python
from distutils.dir_util import copy_tree
import os
import datetime
from datetime import date

root_back_up_location = "/Users/r.agrawal/rk/TallyProject/Backup"
root_back_up_external_hd = "/Users/r.agrawal/rk/TallyProject/Backup_ext"
root_final_account_location = "/Users/r.agrawal/rk/TallyProject/FinalAccounts"
tally_location = "/Users/r.agrawal/rk/TallyProject/Tally.ERP9"

root_excel_back_location = "/Users/r.agrawal/rk/TallyProject/Excel_Backup"


tally_data_location = tally_location + os.sep + "Data"
company_to_process = "001"
year_to_process = "19"
prop_file = "Config.properties"

company_number_mapping = {
    "001": "Company1",
    "002": "Company2",
    "003": "Company1",
    "004": "Company2",
    "005": "ABC"
}


def get_company_number_mapping():
    with open(prop_file) as f:
        l = [line.split("=") for line in f.readlines()]
        d = {key.strip(): value.strip() for key, value in l}
    return d


def print_map(map_to_print):
    for entry in map_to_print:
        print(entry, '-->', map_to_print[entry])


def get_full_company_number(year, comp):
    return year + comp


def copy_folder(src_path, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    copy_tree(src_path, dest_path)


def excel_back_up():
    original_location = "/Users/r.agrawal/rk/certificate"
    today = date.today()
    print(today)
    back_up_location = root_excel_back_location + os.sep + str(today) #str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    copy_folder(original_location, back_up_location)


def back_up_all():
    now = datetime.datetime.now()

    back_up_folder = root_back_up_location + os.sep + str(now.year) + os.sep + str(now.month) + os.sep + str(now.day)
    back_up_ext_folder = root_back_up_external_hd + os.sep + str(now.year) + os.sep + str(now.month) + os.sep + str(now.day)

    copy_folder(tally_data_location, back_up_folder)
    copy_folder(tally_data_location, back_up_ext_folder)


def finalise_account():
    print("Please find the company information below:")
    # print(get_company_number_mapping())
    print_map(get_company_number_mapping())
    company_name = input("Please enter the company number(press enter for " + company_to_process + "):") or company_to_process
    year = input("Please enter the year which needs to be backed up(e.g. 19 for 2019-20, press enter for " + year_to_process + "):") or year_to_process
    company_location = tally_data_location + os.sep + get_full_company_number(year, company_name)
    final_account_loc = root_final_account_location + os.sep + "20" + year + "-" + str(int(year) + 1) + os.sep + \
                  get_full_company_number(year, company_name)

    copy_folder(company_location, final_account_loc)


def get_available_company_nr():
    files = os.listdir(tally_data_location)
    files.sort()
    print("Available Company numbers = ", files)
    return files


def rename_company():
    files = get_available_company_nr()

    old_company = input("Please provide the current company number(complete name pls):")
    if old_company not in files:
        print("The provided current company number does not exists")
    else:
        new_company = input("Please provide the new company number:")
        os.rename(tally_data_location + os.sep + old_company, tally_data_location + os.sep + new_company)


def add_company():
    company_name = input("Please provide company name:")
    files = get_available_company_nr()
    next_company_nr = int(files[-1]) + 1
    company_nr = input("Please enter company number(press enter for " + str(next_company_nr) + "):") or str(next_company_nr)
    with open(prop_file, "a+") as f:
        f.write("\n")
        f.write(company_nr[2:] + "=" + company_name)
    os.rename(tally_data_location + os.sep + "10000", tally_data_location + os.sep + company_nr)


def invalid_choice():
    print("Invalid argument. Please enter a valid choice")


def handle_choice(ch):
    function_map = {
        '1': back_up_all,
        '2': finalise_account,
        '3': rename_company,
        '4': excel_back_up,
        '5': add_company
    }
    func = function_map.get(ch, invalid_choice)
    func()


def print_choice():
    print("Please find the below options:\n"
          "1. Take today's back up\n"
          "2. Finalise a company\n"
          "3. Rename Company number\n"
          "4. Take Excel back up\n"
          "5. Add Company")


if __name__ == '__main__':
    print_choice()
    choice = input("Enter your choice:")
    handle_choice(choice)
