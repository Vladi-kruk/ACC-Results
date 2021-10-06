
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
import glob
import os
import _datetime as data


# all presses path
myPC = "\\\\KRUK3\\c$\\"
ora1 = "\\\\ora-1\\s$\\Indigo\\CnA\\Statistics\\"
ora0 = "\\\\Ora-2_2\\s$\\Indigo\\CnA\\Statistics\\"
ora2_2 = "\\\\Ora-2_2\\s$\\Indigo\\CnA\\Statistics\\"
ora2_1 = "\\\\Ora-2_1\\s$\\Indigo\\CnA\\Statistics\\"
MR117 = "\\\\arad-mr117\\s$\\Indigo\\CnA\\Statistics\\"
LP3_2 = "\\\\arad-lp3-2\\s$\\Indigo\\CnA\\Statistics\\"
MR278 = "\\\\arad_mr278\\s$\\Indigo\\CnA\\Statistics\\"

# global variables
files_name = ['CnAStatistic','AlgorithmSolidsCalibrationStatistics']
DateList = ['Printed VDeveloper', 'VElectrode/LP', 'Density', 'Conductivity', "Optical Density" ]
path = "S:/Indigo/CnA/Statistics/"

def file_save():
    if ChackBoxIsEmpty():  # check chooces
        df = getACC_DataFrame()
        if ~(df.empty):
            file = filedialog.asksaveasfile(mode='w', defaultextension=".csv",
                                            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
            if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            # print(file.name)
            df.to_csv(file.name, index= False)
            file.close() # `()` was missing.

def ShowOnScreen():
    if ChackBoxIsEmpty():
        df_results = getACC_DataFrame()  # collect data and insert to DF
        if ~(df_results.empty):
            DisplyOnTk(df_results)           # print DF on new Tk (function)

def DisplyOnTk(df_Results):
    NewWin = Toplevel(root)
    NewWin.title("Results")

    rows = []
    cols = []
    i, j = 0, 0

    # print columns names in new Tk
    for col in df_Results.columns:
        # print (col)
        e = Entry(NewWin,relief = GROOVE)
        e.grid(row=i,column=j,sticky = NSEW)
        e.insert(END,col)
        cols.append(e)
        j = j + 1
    rows.append(cols)

    # print all values on new Tk
    i = 1
    for index, row in df_Results.iterrows():
        j = 0
        for col in df_Results.columns:
            e = Entry(NewWin,relief = GROOVE)
            e.grid(row=index,column=j,sticky = NSEW)
            e.insert(END,row[col])
            cols.append(e)
            j = j + 1
        rows.append(cols)
        i = i + 1

def DisplyErrorOnTk(str):
    messagebox.showerror('Error', str)

def ChackBoxIsEmpty():
    # print(list(lng.state()))
    for check in list(lng.state()):  # check the check-box bar (all choices)
        if check:
            return True
    return False

def getDataFromCheckBox():
    # Change check-box (binary) to cols names (global array)
    DataChecked = list()
    for index,var in enumerate(list(lng.state())):
        if var:
            DataChecked.append(DateList[index])
    return DataChecked

def currentDate():
    # get current date (NOW) to choose right file
    current_date = data.date.today()
    if current_date.strftime("%d") < '10':
        day = current_date.strftime("%d.").replace('0', '')
    else:
        day = current_date.strftime("%d.")
    if current_date.strftime("%m") < '10':
        month = current_date.strftime("%m.").replace('0', '')
    else:
        month = current_date.strftime("%m.")
    return day + month + current_date.strftime("%Y")

def getFile(path, file_Name):
    try:
        files = glob.glob(path + file_Name + "*.CSV")
        # print(files[0])
        files.sort(key=os.path.getmtime, reverse=True)
        # print(files[0])
        df = pd.read_csv(files[0])
        # print(df.head(5))
        df.sort_values(by='Time', ascending=False, inplace=True)
        # print(df.head(5))
        return df
    except:
        DisplyErrorOnTk("Statistics folder is empty from ACC data")
        # logsFile = open(r'C:\Users\krukv\OneDrive - HP Inc\Desktop\ACC Results Logs.txt', 'w')
        logsFile = open(r'C:/Users/Unicorn/Desktop/ACC Results Logs.txt', 'w')
        line = ['The direction is incorrect \n', 'Data : ' + currentDate() + '\n', 'Path : ' + path + file_Name]
        logsFile.writelines(line)
        logsFile.close()

def GetResultsFromFile(df,date_list):
    ink_list = list()
    df_temp = pd.DataFrame()
    for index, row in df.iterrows():
        if row['ink'] not in ink_list:
            ink_list.append(row['ink'])
            df_temp = df_temp.append(row)
        else:
            break

    df_Final_result = df_temp[['Time', 'ink', 'Result']]
    pd.set_option('display.max_columns', None)
    # print(date_list)
    for col in date_list:
        if col == "Optical Density":
            df_Final_result[['Measured OD/DA', 'Target OD/DA']] = df_temp[['Measured OD/DA', 'Target OD/DA']]
        else:
            df_Final_result[col] = df_temp[col]

    # print(df_result)
    return df_Final_result

def getACC_DataFrame():
    date_list = getDataFromCheckBox()
    path_name = path
    # get data of today
    datetime = currentDate()

    df_Calib = getFile(path, files_name[0])
    df_Calib = df_Calib[(df_Calib['Status'] == 'Passed') & (
            (df_Calib['Calibration'] == 'AdvancedColorCalibration') | (
            df_Calib['Calibration'] == 'ColorCalibration') | (
            df_Calib['Calibration'] == 'AdvancedColorCalibrationLegasy'))]

    # last_ACC_date = df_Calib.iloc[0, 0]
    last_ACC_date = df_Calib.iloc[0, 0]
    print(last_ACC_date)

    df_results = getFile(path, files_name[1])
    df_results = df_results[((df_results['Result'] == 'SUCCESS') | (df_results['Result'] == 'ERROR')) & (
            df_results['Algorithm type'] == 'V-Developer Calibration') & (df_results['Time'] <= last_ACC_date)]

    df_final_results = GetResultsFromFile(df_results, date_list)

    return df_final_results


class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
    def state(self):
        return map((lambda var: var.get()), self.vars)

if __name__ == '__main__':
    root = Tk()
    root.geometry("450x90")
    root.resizable(False, False)
    root.title("ACC Statistics (By Vladi Kruk)")
    lng = Checkbar(root, ['Developer', 'Electroda',
                          'Density', 'Conductivity',
                          "Optical Density" ])
    lng.place(x=8,y=5)
    # tgl = Checkbar(root, ['English','German']).place(x=8,y=5)
    lng.config(relief=GROOVE, bd=2)

    # def ShowOnScreen():
    #     if ChackBoxIsEmpty():
    #         print(getACC_DataFrame())

    # file_frame = LabelFrame(root, text="Save To",width=60, padx=10, pady=4)
    # file_frame.grid(row= 1, column=1,columnspan=4)#pack(side=TOP)
    # #   Input field
    # file_path = Entry(file_frame, width=70, border=2)
    # file_path.insert(0,"")
    # file_path.grid(row=0, column=0)
    Button(root, text='Save', command=lambda: file_save(), width=10, padx=0, pady=8).place(width = 100,x=240,y=40)
    Button(root, text='Show', command=lambda: ShowOnScreen(), width=10, padx=0, pady=8).place(width = 100,x=110,y=40)
    root.mainloop()
