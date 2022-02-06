############## GUI ##############

from tkinter import *
from tkinter import filedialog
import os
from scan import mainprog

root = Tk()

file_path_dict = None

def store_dict():
    global file_path_dict
    file_path_dict = filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose dictionary file", filetypes=(("text files", "*.txt"), ("word files", "*.docx")))
    dict_path_label = Label(root, text=file_path_dict).grid(row=0, column=0)


def get_target():
    global file_path_targ
    file_path_targ = filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose dictionary file", filetypes=(("text files", "*.txt"), ("pdf files", "*.pdf"), ("word files", "*.docx")))
    targ_path_label = Label(root, text=file_path_targ).grid(row=2, column=0)

def run_check():
    mainprog(file_path_dict, file_path_targ)

    
        


my_button = Button(root, text="Select Dictionary File", command=store_dict)
my_button.grid(row=1, column=0)

my_button2 = Button(root, text="Select File to Proof", command=get_target)
my_button2.grid(row=3, column=0)

my_button3 = Button(root, text="Launch", command=run_check)
my_button3.grid(row=4, column=0)

root.mainloop()

############## Scan ##############

import nltk
from sys import argv
import json
import os
import shutil
import re
from tkinter import messagebox


############### INPUT PARSING ###############

class my_dict(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value

def mainprog(dic, targ):

    us_list = []

    with open(dic, 'r') as file:
        for row in file:
            us_list.append(row.rstrip('\n').rstrip('\r'))

    # Creates dict of text line by line so it can reference the line the error was found on
    with open(targ, 'r', encoding="ISO-8859-1") as targ:

        scnfl = my_dict()
        i = 0
        for line in targ:
            scnfl.key = i
            scnfl.value = line.rstrip('\n')
            scnfl.add(scnfl.key, scnfl.value)
            i += 1


    ############### OUTPUT ###############

    # Creates folder based on title of proof file
    strpath = targ.name
    filename = os.path.basename(strpath)
    p = re.compile("^([^.]+)")
    extract = p.search(filename)
    folder = extract.group(1)

    path = os.getcwd()
    path = os.path.join(folder)

    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print("error")
            exit()
    else:
        try:
            shutil.rmtree(path)
        except OSError:
            messagebox.showinfo("Error", "Close any open files before re-running program")
            exit()

        try:
            os.mkdir(path)
        except OSError:
            print("newerror")
            exit()


    # Creates reference file
    with open ("reference.txt", 'w', encoding="ISO-8859-1") as f:
        for entry in scnfl:
            print(entry, scnfl[entry], file=f)


    # Checks if word is in dictionary
    with open("output.txt", "w", encoding="ISO-8859-1") as out:
        for key in scnfl:
            words = nltk.tokenize.word_tokenize(scnfl[key])
            for word in words:
                word = word.lower()
                if word in us_list:
                    print((key), word, file=out)

    shutil.move("reference.txt", path)
    shutil.move("output.txt", path)

    # TODO Find out how to create new folders for each output


    ############## OLD FILEPATH MANIPULATION JUNK ##############

    # Creates folder based on title of proof file
    #strpath = targ.name
    #filename = os.path.basename(strpath)
    #p = re.compile("^([^.]+)")
    #extract = p.search(filename)
    #folder = extract.group(1)

    #path = os.getcwd()
    #path = os.path.join(folder)

    #if not os.path.exists(path):
    #    try:
    #        os.mkdir(path)
    #    except OSError:
    #        print("error")
    #        exit()
    #else:
    #    try:
    #        shutil.rmtree(path)
    #    except OSError:
    #        messagebox.showinfo("Error", "Close any open files before re-running program")
    #        exit()

    #    try:
    #        os.mkdir(path)
    #    except OSError:
    #        print("newerror")
    #        exit()


    ## Creates reference file
    #with open ("reference.txt", 'w', encoding="ISO-8859-1") as f:
    #    for entry in scnfl:
    #        print(entry, scnfl[entry], file=f)


    ## Checks if word is in dictionary
    #with open("output.txt", "w", encoding="ISO-8859-1") as out:
    #    for key in scnfl:
    #        words = nltk.tokenize.word_tokenize(scnfl[key])
    #        for word in words:
    #            word = word.lower()
    #            if word in us_list:
    #                print((key), word, file=out)

    #shutil.move("reference.txt", path)
    #shutil.move("output.txt", path)

    ## TODO Find out how to create new folders for each output








#################### Tk Removal ####################


import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import os
from scan import mainprog


class CntrlWin:

    xpad = 2
    ypad = 3
    alignment = "left"

    


    def __init__(self, root):
        root.title("Spell Right")
        root.geometry("400x110")
        root.iconbitmap(os.path.join("burger.ico"))

        self.folder_image = PhotoImage(file = os.path.join("folder.png"))

        # Buttons
        self.dict_button = tk.Button(root, image=self.folder_image, command=self.store_dict).grid(row=0, column=2, padx=self.xpad, pady=self.ypad, sticky="w")
        self.proof_button = tk.Button(root, image=self.folder_image, command=self.get_target).grid(row=1, column=2, padx=self.xpad, pady=self.ypad, sticky="w")
        self.run_button = tk.Button(root, text="Run", command=self.run_check).grid(row=3, column=1, padx=self.xpad, pady=self.ypad)

        #### Labels ####

        # Title
        self.dict_title = tk.Label(root, text="Choose Dictionary File: ").grid(row=0, column=0, sticky="e", padx=self.xpad, pady=self.ypad)
        self.targ_title = tk.Label(root, text="Choose Proof File: ").grid(row=1, column=0, sticky="e", padx=self.xpad, pady=self.ypad)

        # Files placeholder
        self.dict_path_label = tk.Label(root, text="", width=30, bg = "#ffffff", relief="sunken").grid(row=0, column=1, padx=self.xpad, pady=self.ypad)
        self.targ_path_label = tk.Label(root, text="", width=30, bg = "#ffffff", relief="sunken").grid(row=1, column=1, padx=self.xpad, pady=self.ypad)


    
    # Gets dictionary file path
    def store_dict(self):
        self.file_path_dict = filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose dictionary file", filetypes=(("text files", "*.txt"), ("word files", "*.docx")))
        self.dict_path_label = tk.Label(root, text=os.path.basename(self.file_path_dict), width=30, bg = "#ffffff", relief="sunken").grid(row=0, column=1, padx=self.xpad, pady=self.ypad)
    
    # Gets proof file path
    def get_target(self):
        self.file_path_targ = filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose proof file", filetypes=(("text files", "*.txt"), ("pdf files", "*.pdf"), ("word files", "*.docx")))
        self.targ_path_label = tk.Label(root, text=os.path.basename(self.file_path_targ), width=30, bg = "#ffffff", relief="sunken").grid(row=1, column=1, padx=self.xpad, pady=self.ypad)
    
    # Runs the check
    def run_check(self):

        try:
            self.reference, self.output = mainprog(self.file_path_dict, self.file_path_targ)

            nw = tk.Toplevel(root)
            nw.title("Output")

            try:
                with open(self.reference.name, 'r', encoding="UTF-8") as t:          # alt encoding ISO-8859-1

                    ref = tk.Text(nw, wrap="word", width=120)
                    ref.insert(tk.INSERT, t.read())
                    ref.pack()

                with open(self.output.name, 'r', encoding="UTF-8") as t:          # alt encoding ISO-8859-1

                    out = tk.Text(nw, width=120)
                    out.insert(tk.INSERT, t.read())
                    out.pack()

            except:
                with open(self.reference.name, 'r', encoding="ISO-8859-1") as t:          # alt encoding ISO-8859-1

                    ref = tk.Text(nw, wrap="word", width=120)
                    ref.insert(tk.INSERT, t.read())
                    ref.pack()

                with open(self.output.name, 'r', encoding="ISO-8859-1") as t:          # alt encoding ISO-8859-1

                    out = tk.Text(nw, width=120)
                    out.insert(tk.INSERT, t.read())
                    out.pack()
        except:
            messagebox.showinfo("Error", "Could not run. Please select the correct files and try again")
            exit()


if __name__ == "__main__":
    root = tk.Tk()
    cw = CntrlWin(root)
    root.mainloop()

