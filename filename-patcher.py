import os
import shutil

# TODO: Add replace functionality, throughout the filename.
# TODO: Add Windows Support.
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
    return file.startswith('.') 


def isValid(file):
    return file not in [os.path.basename(__file__)] and not isHidden(file)


def insertBeg(text):
    num = 0
    for file in os.listdir():
        if isValid(file):
            shutil.move(file, text + file)
            num += 1
    return num


def insertEnd(text):
    num = 0
    for file in os.listdir():
        if isValid(file):
            shutil.move(file, file + text)
            num += 1
    return num


def deleteBeg(text):
    num = 0
    for file in os.listdir():
        if file.startswith(text) and isValid(file):
            shutil.move(file, file[len(text):])
            num += 1
    return num


def deleteEnd(text):
    num = 0
    for file in os.listdir():
        if file.endswith(text) and isValid(file):
            shutil.move(file, file[:-len(text)])
            num += 1
    return num


def process(choice):
    PROCESS_DICT = {"I1": insertBeg, "I2": insertEnd, "D1": deleteBeg, "D2":deleteEnd}
    folder, text = getInput()
    if os.path.exists(folder):
        os.chdir(folder)
        return PROCESS_DICT[choice](text)


def main():
    choice = getChoice()
    numChanged = process(choice)
    print(f"{numChanged} filenames have been modified.")


if __name__ == "__main__":
    main()