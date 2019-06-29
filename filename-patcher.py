import os
import shutil


if os.name == 'nt':
    import win32api, win32con


# TODO: Add replace functionality, throughout the filename.
def getChoice():
    print("Enter 'I1' to insert text to the beginning of the filename.")
    print("Enter 'I2' to insert text to the end of the filename.")
    print("Enter 'D1' to delete text from the beginning of the filename.")
    print("Enter 'D2' to delete text from the end of the filename.")
    return input()


def getInput():
    folder = input("Enter the folder containing the files (Enter '.' if current folder): ")
    text = input("Enter the text: ")
    return folder, text


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
            shutil.move(file, text + file)
            num += 1
    return num


def insertEnd(text):
    num = 0
    for file in os.listdir():
        if file != os.path.basename(__file__) and not isHidden(file):
            shutil.move(file, file + text)
            num += 1
    return num


def deleteBeg(text):
    num = 0
    for file in os.listdir():
        if file.startswith(text):
            shutil.move(file, file[len(text):])
            num += 1
    return num


def deleteEnd(text):
    num = 0
    for file in os.listdir():
        if file.endswith(text):
            shutil.move(file, file[:-len(text)])
            num += 1
    return num


def process(choice):
    PROCESS_DICT = {"I1": insertBeg, "I2": insertEnd, "D1": deleteBeg, "D2":deleteEnd}
    folder, text = getInput()
    if os.path.exists(folder):
        os.chdir(folder)
        return PROCESS_DICT[choice](text)


# TODO: Add GUI.
def main():
    choice = getChoice()
    numChanged = process(choice)
    print(f"{numChanged} filenames have been modified.")


if __name__ == "__main__":
    main()