from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import shutil
import sys
import logging


if os.name == 'nt':
    import win32api, win32con


def initLogging():
    logging.basicConfig(
        filename = "xkcdwld.log",
        filemode = 'w',
        level = logging.DEBUG,
        format = " %(asctime)s - %(levelname)s - %(message)s",
    )
    # logging.disable(logging.CRITICAL)


def isHidden(file):
    if os.name== 'nt':
        # Windows
        attribute = win32api.GetFileAttributes(file)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        # Linux / Unix
        return file.startswith('.') 


def insertBeg(text):
    num = 0
    for file in os.listdir():
        if file != os.path.basename(__file__) and not isHidden(file):
            logging.debug(f"Modifying {file} to {text + file}.")
            shutil.move(file, text + file)
            num += 1
    return num


def insertEnd(text):
    num = 0
    for file in os.listdir():
        if file != os.path.basename(__file__) and not isHidden(file):
            logging.debug(f"Modifying {file} to {file + text}.")
            shutil.move(file, file + text)
            num += 1
    return num


def deleteBeg(text):
    num = 0
    for file in os.listdir():
        if file.startswith(text):
            logging.debug(f"Modifying {file} to {file[len(text):]}.")
            shutil.move(file, file[len(text):])
            num += 1
    return num


def deleteEnd(text):
    num = 0
    for file in os.listdir():
        if file.endswith(text):
            logging.debug(f"Modifying {file} to {file[:-len(text)]}.")
            shutil.move(file, file[:-len(text)])
            num += 1
    return num


class userChoiceWindow:
    def __init__(self, master):
        logging.info("Initialising user choice GUI...")
        self.window = master
        self.window.title("Select Operation")
        self.window.resizable(False, False)
        self.window.config(background = "#BBBBBB")

        self.style = ttk.Style()
        self.style.configure('TButton', background = '#BBBBBB')
        self.style.configure('TLabel', background = '#BBBBBB', font = ('Comic Sans', 12, 'bold'))
        self.style.configure('TRadiobutton', background = '#BBBBBB', font = ('Arial', 11))

        ttk.Label(self.window, text = "Select the appropriate operation: ").pack(pady = 10)
        self.radioChoice = StringVar()
        self.insertBegRadio = ttk.Radiobutton(self.window, 
            text = "Insert text to the beginning of the filename.",
            variable = self.radioChoice, value = "InsertBeg")
        self.insertEndRadio = ttk.Radiobutton(self.window,
            text = "Insert text to the end of the filename.",
            variable = self.radioChoice, value = "InsertEnd")
        self.deleteBegRadio = ttk.Radiobutton(self.window,
            text = "Delete text from the beginning of the filename.",
            variable = self.radioChoice, value = "DeleteBeg")
        self.deleteEndRadio = ttk.Radiobutton(self.window,
            text = "Delete text from the end of the filename.",
            variable = self.radioChoice, value = "DeleteEnd")

        self.insertBegRadio.pack(anchor = 'w', padx = 10, pady = 5)
        self.insertEndRadio.pack(anchor = 'w', padx = 10, pady = 5)
        self.deleteBegRadio.pack(anchor = 'w', padx = 10, pady = 5)
        self.deleteEndRadio.pack(anchor = 'w', padx = 10, pady = 5)
        
        ttk.Button(self.window, text = "Submit", command = self.processChoice).pack(side = LEFT, anchor = 's', padx = 10, pady = 10)
        ttk.Button(self.window, text = "Quit", command = sys.exit).pack(side = RIGHT, anchor = 's', padx = 10, pady = 10)

    def processChoice(self):
        logging.debug(f"User has chosen {self.radioChoice.get()} option.")
        self.window.state('withdrawn')
        processGUI(self.window, self.radioChoice.get())


# TODO: Add option [Checkbox] to ignore file extensions.
# TODO: Add replace functionality, throughout the filename.
class processGUI:
    _operation_dict = {
                        "InsertBeg": insertBeg, 
                        "InsertEnd": insertEnd,
                        "DeleteBeg": deleteBeg,
                        "DeleteEnd": deleteEnd
                      }

    def __init__(self, master, choice):
        logging.info("Initialising processing GUI...")
        self.window = Toplevel(master)
        self.window.title("filename-patcher")
        self.window.resizable(False, False)
        self.window.config(background = "#BBBBBB")
        self.userChoice = choice

        self.style = ttk.Style()
        self.style.configure('TButton', background = '#BBBBBB')
        self.style.configure('TLabel', background = '#BBBBBB', font = ('Comic Sans', 12, 'bold'))
        self.style.configure('TEntry', background = '#BBBBBB', font = ("Calibri 14"))

        self.dir = ttk.Entry(self.window, width = 80)
        self.text = ttk.Entry(self.window, width = 80)
        ttk.Label(self.window, 
            text = f"The current folder is {os.getcwd()}").pack(anchor = 'w', pady = 5, padx = 10)
        ttk.Label(self.window, 
            text = "Enter the folder containing the files (Enter '.' if current folder): ").pack(anchor = 'w', padx = 10)
        self.dir.pack(anchor = 'w', padx = 10, pady = 5)
        ttk.Label(self.window, text = "Enter the text: ").pack(anchor = 'w', padx = 10)
        self.text.pack(anchor = 'w', padx = 10, pady = 5)
        
        ttk.Button(self.window, text = "Submit", command = self.processChoice).pack(side = LEFT, anchor = 's', padx = 10, pady = 10)
        ttk.Button(self.window, text = "Quit", command = sys.exit).pack(side = RIGHT, anchor = 's', padx = 10, pady = 10)

    def processChoice(self):
        folder = self.dir.get()
        text = self.text.get()
        logging.debug(f"User has select {folder} as the working directory.")
        logging.debug(f"User has select {text} as the processing text.")
        if os.path.exists(folder):
            logging.debug(f"Changing directory to {os.path.abspath(folder)}.")
            os.chdir(folder)
            self.displayReport(self._operation_dict[self.userChoice](text))

    def displayReport(self, num):
        logging.debug(f"{num} filenames have been modified.")
        messagebox.showinfo(title = "Report", message = f"{num} filenames have been modified.")
        self.window.master.destroy()


def main():
    initLogging()

    root = Tk()
    app = userChoiceWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()