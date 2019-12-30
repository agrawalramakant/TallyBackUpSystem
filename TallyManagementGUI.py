from tkinter import *
from tkinter import filedialog
import os
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import datetime
from datetime import date
import json


five_digit_regex = r"^[0-9]{5}$"
prop_file = "Config.properties"
setup_file = "setup.properties"
setup_items = ['tally_path', 'tally_back_path', 'tally_back_ext_path', 'final_acc', 'default_tally_acc',
                   'doc_path', 'doc_back_path']
setup_map = dict()

class TallyManagementApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.winfo_toplevel().title("Tally management")
        self.winfo_toplevel().resizable(0, 0)
        self.winfo_toplevel().geometry("+450+300")

        TallyManagementApp.load_setting()
        self._frame = None
        self.switch_frame(StartPage)
        menu_frame = Frame(self)
        menu_frame.grid(row=0, column=0, padx=1, pady=1)

        Button(menu_frame, text="Back up Tally", fg="black", width=21, height=2, bd=0, bg="#fff", cursor="hand2",
               command=lambda: self.switch_frame(BackUpTally)).grid(row=0, column=0, columnspan=1, padx=5, pady=1)

        Button(menu_frame, text="Import Company", fg="black", width=21, height=2, bd=0, bg="#fff", cursor="hand2",
               command=lambda: self.switch_frame(ImportCompany)).grid(row=1, column=0, columnspan=1, padx=5, pady=1)

        Button(menu_frame, text="Finalise a company", fg="black", width=21, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: self.switch_frame(FinalizeCompany))\
            .grid(row=2, column=0, columnspan=1, padx=5, pady=1)

        Button(menu_frame, text="Add Company", fg="black", width=21, height=2, bd=0, bg="#fff", cursor="hand2",
               command=lambda: self.switch_frame(AddCompany))\
            .grid(row=3, column=0, columnspan=1, padx=5, pady=1)

        Button(menu_frame, text="Rename Company number", fg="black", width=21, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: self.switch_frame(RenameCompany))\
            .grid(row=4, column=0, columnspan=1, padx=5, pady=1)

        Button(menu_frame, text="Back up Documents", fg="black", width=21, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: self.switch_frame(BackUpDocuments))\
            .grid(row=5, column=0, columnspan=1, padx=5, pady=1)

        Button(menu_frame, text="Setup", fg="black", width=21, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: self.switch_frame(SetupPage)) \
            .grid(row=6, column=0, columnspan=1, padx=5, pady=1)

        status_frame = Frame(self)
        status_frame.grid(row=1, column=0, columnspan=2, padx=1, pady=1, sticky=W)

        status_label = Label(status_frame, text="Status:", bd=1, width=5)
        status_label.grid(row=0, column=0, padx=5, pady=1)

        self.status_var = StringVar()
        self.status_var.set("Application Initiated")
        statusbar = Entry(status_frame, textvariable=self.status_var, bd=1, width=42, relief=SUNKEN,
                          state='readonly')
        scroll = Scrollbar(self, orient='horizontal', command=statusbar.xview)
        statusbar.config(xscrollcommand=scroll.set)

        statusbar.grid(row=0, column=1, padx=1, pady=1, sticky=W)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=1, padx=1, pady=1)

    @staticmethod
    def browse_btn(var):
        old_name = var.get()
        file_path = filedialog.askdirectory()
        if file_path:
            var.set(file_path)
        else:
            var.set(old_name)

    def log(self, msg):
        self.status_var.set(msg)

    @staticmethod
    def is_valid_company_nr(nr):
        return re.fullmatch(five_digit_regex, nr)

    @staticmethod
    def company_already_exists(nr):
        files = TallyManagementApp.get_all_companies_in_tally()
        return nr in files

    @staticmethod
    def copy_folder(src_path, dest_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        copy_tree(src_path, dest_path)

    @staticmethod
    def copy_file(src_file, dest_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        copy_file(src_file, dest_path)

    @staticmethod
    def get_company_number_mapping():
        with open(prop_file) as f:
            l = [line.split("=") for line in f.readlines()]
            d = {key.strip(): value.strip() for key, value in l}
        return d

    @staticmethod
    def get_all_companies_in_tally():
        files = os.listdir(setup_map['tally_path'].get())
        files = [file for file in files if TallyManagementApp.is_valid_company_nr(file)]
        files.sort()
        return files

    @staticmethod
    def load_setting():
        with open(setup_file, 'r') as fp:
            data = json.load(fp)
        for item in setup_items:
            setup_map[item] = StringVar()
            setup_map[item].set(data.get(item, ""))


class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is the start page").grid(row=0, column=0, padx=1, pady=1)


class BackUpTally(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        master.log("Clicked Back up Tally!!")
        company_var = StringVar()
        files = TallyManagementApp.get_all_companies_in_tally()
        company_var.set(files[0])

        year_label = Label(self, text="Company Nr.", anchor=NE)
        year_label.grid(row=0, column=0)
        company_dd = OptionMenu(self, company_var, *files)
        company_dd.grid(row=0, column=1)

        all_label = Label(self, text="All ", anchor=NE)
        all_label.grid(row=1, column=0)

        all_var = IntVar()
        all_checkbox = Checkbutton(self, text="", variable=all_var)
        all_checkbox.grid(row=1, column=1)

        Button(self, text="Execute", fg="black", width=10, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: BackUpTally.logic(company_var.get(), all_var.get(), master)).grid(
            row=2, column=0, columnspan=2, padx=1, pady=10, sticky=SE)

    @staticmethod
    def logic(company_nr, is_all, master):
        now = datetime.datetime.now()
        original_loc = setup_map['tally_path'].get()
        back_up_stem = str(now.year) + os.sep + str(now.month) + os.sep + str(now.day)
        back_up_folder = setup_map['tally_back_path'].get() + os.sep + back_up_stem
        back_up_ext_folder = setup_map['tally_back_ext_path'].get() + os.sep + back_up_stem
        if not is_all:
            if TallyManagementApp.is_valid_company_nr(company_nr):
                original_loc = original_loc + os.sep + company_nr
                back_up_suffix = company_nr + os.sep + company_nr
                back_up_folder = back_up_folder + "_" + back_up_suffix
                back_up_ext_folder = back_up_ext_folder + "_" + back_up_suffix
            else:
                master.log("Sorry!! The company number is not 5 digits")
                return

        TallyManagementApp.copy_folder(original_loc, back_up_folder)
        TallyManagementApp.copy_folder(original_loc, back_up_ext_folder)
        master.switch_frame(StartPage)
        master.log("Back taken at " + back_up_folder)


class ImportCompany(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        master.log("Clicked Import Company!!")

        company_path_var = StringVar()
        company_path_label = Label(self, text="Company to Import", anchor=NE)
        company_path_label.grid(row=0, column=0, sticky=W)
        company_nr_entry = Entry(self, textvariable=company_path_var,
                                     bd=1, width=30, relief=SUNKEN, state='readonly')
        company_nr_entry.xview_moveto(0.5)
        company_nr_entry.grid(row=0, column=1)
        Button(self, text="Browse", fg="black", bd=0, bg="#fff", cursor="hand2",
               command=lambda: TallyManagementApp.browse_btn(company_path_var)) \
            .grid(row=0, column=2, padx=1, pady=1, sticky=SE)

        overwrite_label = Label(self, text="Overwrite:", anchor=NE)
        overwrite_label.grid(row=1, column=0)

        overwrite_var = IntVar()
        overwrite_checkbox = Checkbutton(self, text="", variable=overwrite_var)
        overwrite_checkbox.grid(row=1, column=1)

        Button(self, text="Execute", fg="black", width=10, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: ImportCompany.logic(company_path_var.get(), overwrite_var.get(), master)).grid(
            row=2, column=0, columnspan=2, padx=1, pady=10, sticky=SE)

    @staticmethod
    def logic(company_path, is_overwrite, master):
        company_nr = company_path.split(os.sep)[-1]
        if not is_overwrite:
            company_nr = "99" + company_nr[2:]
        import_path = setup_map['tally_path'].get() + os.sep + company_nr

        TallyManagementApp.copy_folder(company_path, import_path)
        master.switch_frame(StartPage)
        master.log("Company imported at " + import_path)


class FinalizeCompany(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        master.log("Clicked Finalise Company!!")
        company_var = StringVar()
        files = TallyManagementApp.get_all_companies_in_tally()
        company_var.set(files[0])
        company_dd = OptionMenu(self, company_var, *files)
        company_dd.grid(row=0, column=1)

        comp_nr_label = Label(self, text="Company Nr.", anchor=NE)
        comp_nr_label.grid(row=0, column=0)

        comp_mapping_label = Label(self, text="Company Number Mapping:", anchor=NE)
        comp_mapping_label.grid(row=1, column=0, columnspan=2, sticky=W)
        scroll = Scrollbar(self, orient=VERTICAL)
        self.select = Listbox(self, yscrollcommand=scroll.set, height=9, width=23, relief=SUNKEN)
        scroll.config(command=self.select.yview)
        scroll.grid(sticky=E)
        self.select.grid(row=2, column=0, columnspan=2)
        self.set_select()

        Button(self, text="Execute", fg="black", width=10, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: FinalizeCompany.logic(company_var.get(), master)).grid(
            row=3, column=0, columnspan=2, padx=1, pady=10, sticky=SE)

    @staticmethod
    def logic(company_name, master):
        company_location = setup_map['tally_path'].get() + os.sep + company_name
        year = company_name[0:2]
        accounting_year = "20" + year + "-" + str(int(year) + 1)
        final_account_loc = setup_map['final_acc'].get() + os.sep + accounting_year + os.sep + company_name

        TallyManagementApp.copy_folder(company_location, final_account_loc)
        master.switch_frame(StartPage)
        master.log("Company " + company_name + " finalized for year " + accounting_year)

    def set_select(self):
        self.select.delete(0, END)
        mapping = TallyManagementApp.get_company_number_mapping()
        for entry in mapping:
            self.select.insert(END, "{0} --> {1}".format(entry, mapping[entry]))


class AddCompany(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        master.log("Clicked Add Company!!")
        comp_nr_var = StringVar()
        comp_nr_label = Label(self, text="Company Number:", anchor=NW)
        comp_nr_label.grid(row=0, column=0)
        comp_nr_entry = Entry(self, width=10, textvariable=comp_nr_var)
        comp_nr_entry.grid(row=0, column=1)

        comp_name_var = StringVar()
        comp_name_label = Label(self, text="Company Name:", anchor=NW)
        comp_name_label.grid(row=1, column=0)
        comp_name_label = Entry(self, width=10, textvariable=comp_name_var)
        comp_name_label.grid(row=1, column=1)
        Button(self, text="Execute", fg="black", width=10, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: AddCompany.logic(comp_name_var.get(), comp_nr_var.get(), master))\
            .grid(row=2, column=0, columnspan=2, padx=1, pady=10, sticky=SE)

    @staticmethod
    def logic(company_name, company_nr, master):
        default_company_number = setup_map['default_tally_acc']
        if TallyManagementApp.is_valid_company_nr(company_nr):
            if TallyManagementApp.company_already_exists(default_company_number):
                status = RenameCompany.logic(default_company_number, company_nr, master)
                if status:
                    with open(prop_file, "a+") as f:
                        f.write("\n")
                        f.write(company_nr[2:] + "=" + company_name)
                    master.switch_frame(StartPage)
                    master.log("Company " + company_nr + " added")
            else:
                master.log("Sorry!! Company " + default_company_number + " does not exists")
        else:
            master.log("Sorry!! The company number is not 5 digits")


class RenameCompany(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        master.log("Clicked Rename Company!!")

        curr_comp_nr_label = Label(self, text="Current Company Nr:", anchor=NW)
        curr_comp_nr_label.grid(row=0, column=0)

        curr_comp_nr_var = StringVar()
        files = TallyManagementApp.get_all_companies_in_tally()
        curr_comp_nr_var.set(files[0])
        comp_nr_dd = OptionMenu(self, curr_comp_nr_var, *files)
        comp_nr_dd.grid(row=0, column=1)

        new_comp_nr_var = StringVar()
        comp_name_label = Label(self, text="New Company Nr:", anchor=NE)
        comp_name_label.grid(row=1, column=0)
        comp_name_label = Entry(self, width=8, textvariable=new_comp_nr_var)
        comp_name_label.grid(row=1, column=1)
        Button(self, text="Execute", fg="black", width=10, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: RenameCompany.logic(curr_comp_nr_var.get(), new_comp_nr_var.get(), master)).grid(
            row=5, column=0, columnspan=2, padx=1, pady=10, sticky=SE)

    @staticmethod
    def logic(old_company, new_company, master):
        if TallyManagementApp.is_valid_company_nr(old_company):
            if not TallyManagementApp.company_already_exists(old_company):
                master.log("Sorry!! The company " + old_company + " does not exists in Tally")
            else:
                if TallyManagementApp.is_valid_company_nr(new_company):
                    if TallyManagementApp.company_already_exists(new_company):
                        master.log("Sorry!! The company " + new_company + " already exists")
                        return False
                    else:
                        os.rename(setup_map['tally_path'].get() + os.sep + old_company, setup_map['tally_path'].get() + os.sep + new_company)
                        master.log("Company number renamed from " + old_company + " to " + new_company)
                else:
                    master.log("Sorry!! The new company number is not 5 digits")
        else:
            master.log("Sorry!! The current company number is not 5 digits")
        master.switch_frame(StartPage)
        return True


class BackUpDocuments(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        master.log("Clicked Back up documents!!")
        company_var = StringVar()
        files = os.listdir(setup_map['doc_path'].get())
        company_var.set(files[0])

        year_label = Label(self, text="Document", anchor=NE)
        year_label.grid(row=0, column=0)
        company_dd = OptionMenu(self, company_var, *files)
        company_dd.grid(row=0, column=1)

        all_label = Label(self, text="All ", anchor=NE)
        all_label.grid(row=1, column=0)

        all_var = IntVar()
        all_checkbox = Checkbutton(self, text="", variable=all_var)
        all_checkbox.grid(row=1, column=1)

        Button(self, text="Execute", fg="black", width=10, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: BackUpDocuments.logic(company_var.get(), all_var.get(), master)).grid(
            row=2, column=0, columnspan=2, padx=1, pady=10, sticky=SE)

    @staticmethod
    def logic(document, is_all, master):
        original_location = setup_map['doc_path'].get()
        back_up_location = setup_map['doc_back_path'].get()
        today = date.today()
        if is_all:
            back_up_location = back_up_location + os.sep + str(today)
            TallyManagementApp.copy_folder(original_location, back_up_location)
        else:
            original_file_location = original_location + os.sep + document
            back_up_location = back_up_location + os.sep + str(today) + "-" + document.split(".")[0]
            TallyManagementApp.copy_file(original_file_location, back_up_location)
        master.log("Back up taken at " + back_up_location)


class SetupPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        master.log("Clicked Setup page!!")

        tally_loc_var = setup_map[setup_items[0]]
        tally_location_label = Label(self, text="Tally Data path", anchor=NE)
        tally_location_label.grid(row=0, column=0, sticky= W)
        tally_location_entry = Entry(self, textvariable=tally_loc_var,
                                     bd=1, width=30, relief=SUNKEN, state='readonly')
        tally_location_entry.xview_moveto(0.5)
        tally_location_entry.grid(row=0, column=1)
        Button(self, text="Browse", fg="black", bd=0, bg="#fff", cursor="hand2",
               command=lambda: TallyManagementApp.browse_btn(tally_loc_var))\
            .grid(row=0, column=2, padx=1, pady=1, sticky=SE)

        tally_backup_loc = setup_map[setup_items[1]]
        tally_backup_location_label = Label(self, text="Tally Back up path:", anchor=NE)
        tally_backup_location_label.grid(row=1, column=0, sticky= W)
        tally_backup_location_entry = Entry(self, textvariable=tally_backup_loc,
                                     bd=1, width=30, relief=SUNKEN, state='readonly')
        tally_backup_location_entry.xview_moveto(0.5)
        tally_backup_location_entry.grid(row=1, column=1)
        Button(self, text="Browse", fg="black", bd=0, bg="#fff", cursor="hand2",
               command=lambda: TallyManagementApp.browse_btn(tally_backup_loc)) \
            .grid(row=1, column=2, padx=1, pady=1, sticky=SE)

        tally_ext_backup_loc = setup_map[setup_items[2]]
        tally_ext_backup_location_label = Label(self, text="Tally Back up Ext path", anchor=NE)
        tally_ext_backup_location_label.grid(row=2, column=0, sticky= W)
        tally_backup_location_entry = Entry(self, textvariable=tally_ext_backup_loc,
                                            bd=1, width=30, relief=SUNKEN, state='readonly')
        tally_backup_location_entry.xview_moveto(0.5)
        tally_backup_location_entry.grid(row=2, column=1)
        Button(self, text="Browse", fg="black", bd=0, bg="#fff", cursor="hand2",
               command=lambda: TallyManagementApp.browse_btn(tally_ext_backup_loc)) \
            .grid(row=2, column=2, padx=1, pady=1, sticky=SE)

        final_acc_loc = setup_map[setup_items[3]]
        final_acc_label = Label(self, text="Final Account path", anchor=NE)
        final_acc_label.grid(row=3, column=0, sticky= W)
        final_acc_location_entry = Entry(self, textvariable=final_acc_loc,
                                            bd=1, width=30, relief=SUNKEN, state='readonly')
        final_acc_location_entry.xview_moveto(0.5)
        final_acc_location_entry.grid(row=3, column=1)
        Button(self, text="Browse", fg="black", bd=0, bg="#fff", cursor="hand2",
               command=lambda: TallyManagementApp.browse_btn(final_acc_loc)) \
            .grid(row=3, column=2, padx=1, pady=1, sticky=SE)

        default_account_nr = setup_map[setup_items[4]]
        default_account_nr_label = Label(self, text="Default Tally Account Nr.", anchor=NE)
        default_account_nr_label.grid(row=4, column=0, sticky=W)
        default_account_nr_entry = Entry(self, textvariable=default_account_nr,
                                         bd=1, width=30, relief=SUNKEN)
        default_account_nr_entry.xview_moveto(0.5)
        default_account_nr_entry.grid(row=4, column=1)

        documents_loc = setup_map[setup_items[5]]
        documents_location_label = Label(self, text="Documents path", anchor=NE)
        documents_location_label.grid(row=5, column=0, sticky= W)
        documents_location_entry = Entry(self, textvariable=documents_loc,
                                         bd=1, width=30, relief=SUNKEN, state='readonly')
        documents_location_entry.xview_moveto(0.5)
        documents_location_entry.grid(row=5, column=1)
        Button(self, text="Browse", fg="black", bd=0, bg="#fff", cursor="hand2",
               command=lambda: TallyManagementApp.browse_btn(documents_loc)) \
            .grid(row=5, column=2, padx=1, pady=1, sticky=SE)

        document_backup_loc = setup_map[setup_items[6]]
        document_backup_location_label = Label(self, text="Documents Back up path", anchor=NE)
        document_backup_location_label.grid(row=6, column=0, sticky= W)
        documents_backup_location_entry = Entry(self, textvariable=document_backup_loc,
                                         bd=1, width=30, relief=SUNKEN, state='readonly')
        documents_backup_location_entry.xview_moveto(0.5)
        documents_backup_location_entry.grid(row=6, column=1)
        Button(self, text="Browse", fg="black", bd=0, bg="#fff", cursor="hand2",
               command=lambda: TallyManagementApp.browse_btn(document_backup_loc)) \
            .grid(row=6, column=2, padx=1, pady=1, sticky=SE)

        Button(self, text="Save", fg="black", width=10, height=2, bd=0, bg="#fff",
               cursor="hand2", command=lambda: SetupPage.save(master)).grid(
            row=7, column=1, columnspan=2, padx=1, pady=10, sticky=SE)

    @staticmethod
    def save(master):
        data = dict()
        for entry in setup_map:
            data[entry] = setup_map[entry].get()
        with open(setup_file, 'w') as outfile:
            json.dump(data, outfile)
        master.log("The configuration is saved!!")


if __name__ == "__main__":
    app = TallyManagementApp()
    app.mainloop()
