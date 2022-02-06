

import nltk.tokenize
import os
import re as myregex
from re import search
from tkinter import messagebox
from helpers import pdf_reader, plaintext_reader, doc_reader


############### INPUT PARSING ###############

class my_dict(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value

def mainprog(dic, targ):

    us_list = []
    scnfl = my_dict()

    with open(dic, 'r') as file:
        for row in file:
            us_list.append(row.rstrip('\n').rstrip('\r'))

    path = os.getcwd()
    newpath = os.path.join(path, "tmp")
    refpath = os.path.join(newpath, "reference.txt")
    outpath = os.path.join(newpath, "output.txt")

    if not os.path.exists(newpath):
        os.mkdir(newpath)
    else:
        filename, file_ext = os.path.splitext(targ)


        # Control for reading each file type
        if file_ext == ".txt":
            scnfl, encoding = plaintext_reader(targ)

        elif file_ext == ".pdf":
            scnfl, encoding = pdf_reader(targ)

        elif file_ext == ".docx":
            scnfl, encoding = doc_reader(targ)

        else:
            messagebox.showinfo("Error", "Unsupported Filetype")
            exit()


        ############### OUTPUT ###############

        # Creates reference file
        with open (refpath, 'w', encoding="UTF-8") as ref:     # ISO-8859-1
            for entry in scnfl:
                print(entry, scnfl[entry], file=ref)



    # Checks if word is in dictionary and creates output file
    with open(outpath, "w", encoding="UTF-8") as out:
        for key in scnfl:

            # This is much slower because each word in dict is tested against every single word in string
            for entry in us_list:

                hits = myregex.findall(rf"\b{entry}\b", scnfl[key], myregex.IGNORECASE)

                if hits:
                    for hit in hits:
                        print(key, hit, file=out)

            #words = nltk.tokenize.word_tokenize(scnfl[key])

            #for word in words:
            #    word = word.lower()
            #    split_test = myregex.search("[-]", word)
            #    if split_test:
            #        split_list = word.split("-")

            #        for w in split_list:
            #            if w in us_list:
            #                print(key, w, file=out)

            #    if word in us_list:
            #        print((key), word, file=out)

    return ref, out


