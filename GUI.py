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