# ---/import library/--- #
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from datetime import datetime


# ---/declaring global var at the module level/--- #
employee_name = ""
number_of_allocated = ""
number_of_closed = ""
filename = ""
percentage_of_completion = 0.0
percentage = 0.0
kpi_s = 0.0


# ---/definitions/--- #
def formatted_date_now():
    now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    now = str(now)
    return now


def get_fields_and_save():
    global employee_name
    global number_of_allocated
    global number_of_closed
    global percentage_of_completion
    employee_name = employee_name_entry.get()
    number_of_allocated = allocated_cases_entry.get()
    number_of_closed = close_cases_entry.get()
    percentage_of_completion = percentage_calculation_output_label.cget("text")
    save_to_file()


def save_to_file():
    file_path_a = open("save_data_cases.txt", "a")
    file_path_r = open("save_data_cases.txt", "r")

    if file_path_r.read(1):
        query = "\nemployee name: {0}\ndate: {1}\nallocated cases: {2}\nclosed cases: {3}" \
                "\npercentage of completion: {4}".format(employee_name, formatted_date_now(), number_of_allocated,
                                                         number_of_closed, percentage_of_completion)
    else:
        query = "employee name: {0}\ndate: {1}\nallocated cases: {2}\nclosed cases: {3}" \
                "\npercentage of completion: {4}".format(employee_name, formatted_date_now(), number_of_allocated,
                                                         number_of_closed, percentage_of_completion)

    file_path_a.writelines(query + "\n")
    file_path_a.close()
    file_path_r.close()


def percentage_calculation_button():
    global percentage
    allocated_cases = allocated_cases_entry.get()
    close_cases = close_cases_entry.get()
    kpi_test = kpi_entry.get()
    if str(allocated_cases).isalpha() or str(close_cases).isalpha() or str(kpi_test).isalpha():
        showinfo(title="Wrong Input", message="please use numbers not letters")
    elif allocated_cases.isnumeric() and close_cases.isnumeric() and kpi_test.isnumeric:
        percentage = 100 * float(close_cases) / float(allocated_cases)
        percentage = "{:.2f}".format(percentage)
        percentage_calculation_output_label.config(text=f"{str(percentage)} %")
        compare_percentage_kpi()
    else:
        showinfo(title="Wrong Input", message="Allocated & Closed Cases use a whole number"
                                              "\nKPI you can use whole number or decimal"
                                              "\nYou can reset fields by pressing the Clear button")


def compare_percentage_kpi():
    global kpi_s
    kpi_s = kpi_entry.get()
    kpi_s = "{:.2f}".format(float(kpi_s))
    # compare kpi to percentage
    if float(kpi_s) == float(percentage):
        kpi_result_label.config(text=f"Current Performance: {str(percentage)} % "
                                     f"| Expected Performance: {kpi_s} % you are at expected performance", bg="yellow")
    elif float(kpi_s) > float(percentage):
        kpi_result_label.config(text=f"Current Performance: {str(percentage)} % "
                                     f"| Expected Performance: {kpi_s} % you are not meeting your requirements", bg="red")
    elif float(kpi_s) < float(percentage):
        kpi_result_label.config(text=f"Current Performance: {str(percentage)} % "
                                     f"| Expected Performance: {kpi_s} % you are meeting your requirements", bg="green")
    else:
        kpi_result_label.config(text=f"Current Performance: {str(percentage)} % "
                                     f"| Expected Performance: {kpi_s} % bad things have happened", bg="brown")


def clear_button():
    employee_name_entry.delete(0, END)
    allocated_cases_entry.delete(0, END)
    close_cases_entry.delete(0, END)
    percentage_calculation_output_label.config(text="")
    kpi_entry.delete(0, END)
    kpi_result_label.config(text="")
    kpi_result_label.config(bg="grey")


def select_file():
    global filename
    filetypes = (("text files", "*.txt"), ("All files", "*.*"))
    filename = fd.askopenfile(mode="r", title="Open a file", initialdir="./", filetypes=filetypes)
    get_push_filename()


def get_push_filename():
    if filename is not None:
        content = filename.readlines()

        for i in range(len(content)):
            content[i] = content[i].replace("\n", "")

        file_employee_name, file_allocated, file_closed, file_kpi = content

        employee_name_entry.delete(0, END)
        allocated_cases_entry.delete(0, END)
        close_cases_entry.delete(0, END)
        kpi_entry.delete(0, END)

        employee_name_entry.insert(0, str(file_employee_name))
        allocated_cases_entry.insert(0, str(file_allocated))
        close_cases_entry.insert(0, str(file_closed))
        kpi_entry.insert(0, str(file_kpi))


# ############### #
# ##---/GUI/---## #
# ############### #
root = Tk()
root.title("Case Completion Percentage Calculator")
root.resizable(False, False)
# ---/Button/--- #
open_button = Button(root, width=25, height=2, text="Open a File", command=select_file)
button_Save = Button(root, text="Save", width=25, height=2, command=get_fields_and_save)
button_Calc = Button(root, text="Calculate", width=25, height=2, command=percentage_calculation_button)
button_Clear = Button(root, text="Clear", width=25, height=2, command=clear_button)
# ---/Fields/--- #
close_cases_entry = Entry(root, width=25, borderwidth=5)
allocated_cases_entry = Entry(root, width=25, borderwidth=5)
kpi_entry = Entry(root, width=25, borderwidth=5)
employee_name_entry = Entry(root, width=25, borderwidth=5)
# ---/Labels/--- #
date_label = Label(root, text=formatted_date_now())
allocated_cases_label = Label(root, width=25, text="Allocated Cases")
close_cases_label = Label(root, width=25, text="Closed Cases")
percentage_calculation_label = Label(root, width=25, text="Percentage of Completion")
percentage_calculation_output_label = Label(root, width=25, text=str(percentage) + " %")
kpi_label = Label(root, width=25, text="KPI")
kpi_result_label = Label(root, width=104, borderwidth=5, text=kpi_s, bg="grey")
# -------------------------------------------------------------------------------------------------------------------- #
# ---/button grid layout/--- #
open_button.grid(row=5, column=0)
button_Save.grid(row=5, column=1)
button_Calc.grid(row=5, column=2)
button_Clear.grid(row=5, column=3)
# ---/field grid layout/--- #
allocated_cases_entry.grid(row=2, column=0)
close_cases_entry.grid(row=2, column=1)
percentage_calculation_output_label.grid(row=2, column=3)
kpi_entry.grid(row=2, column=2)
employee_name_entry.grid(row=0, column=2)
# ---/label grid layout/--- #
date_label.grid(row=0, column=0)
allocated_cases_label.grid(row=1, column=0)
close_cases_label.grid(row=1, column=1)
percentage_calculation_label.grid(row=1, column=3)
kpi_label.grid(row=1, column=2)
kpi_result_label.grid(row=6, column=0, columnspan=4)
# ---/test section/--- #
employee_name_label = Label(root, width=25, text="Employee Name")
employee_name_label.grid(row=0, column=1)


root.mainloop()
