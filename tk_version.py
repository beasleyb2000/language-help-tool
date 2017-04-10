from main import *
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import csv
import os

global inputFocus

class User():
    def ___init__(self, username, password, name, usertype):

        self.name = name
        self.username = username
        self.password = password
        self.usertype = usertype

class langApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.container = Frame(self)
        self.container.pack(side="top", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.title("Translator")
        self.iconbitmap('mainIcon.ico')

        self.option_add("*Font", 'TkDefaultFont')

        self.mainMenu = Menu(self)
        makeMenusItem(self.mainMenu, {}, {"Log Out": self.logOut,
                                          "Close": self.closeWindowCommand,
                                          "Reset": self.reset})
        generateMenuBar(self, self.mainMenu)

        self.resizable(width=False, height=False)
        
        self.frames = {}

        for F in (loginPage, homePage):
            self.frame = F(self.container, self)
            self.frames[F] = self.frame
            self.frame.grid(row=0, column=0, sticky="nsew", pady=5)

        self.show_frame(loginPage)

        self.bind("<Control-w>", self.closeWindowCommand)

    def show_frame(self, frame):
        self.frame = self.frames[frame]
        self.frame.tkraise()

    def closeWindowCommand(self, event=None):
        if messagebox.askyesno("Quit", "Do you really wish to quit?"):
            quit()

    def logOut(self):
        if messagebox.askyesno("Logout", "Do you really want to log out?"):
            self.geometry("300x100")
            self.mainMenu.delete(4, END)
            self.mainMenu.entryconfig("Log Out", state="disabled")
            self.mainMenu.entryconfig("Reset", state="disabled")
            self.frames[loginPage].usernameEntry.focus()
            self.show_frame(loginPage)

    def reset(self):
        dicts, langDict, engDict = updateDicts()

        for F in [homePage]:
            self.frame = F(self.container, self)
            self.frames[F] = self.frame
            self.frame.grid(row=0, column=0, sticky="nsew", pady=5)

        self.show_frame(homePage)

class addUserDataPage(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.option_add("*Font", 'TkDefaultFont')

        self.title("Register User")

        self.entryFrame = Frame(self, relief=FLAT)
        self.entryFrame.pack(padx=10, pady=10)
        self.entryFrame.grid_rowconfigure(0, weight=0)
        self.entryFrame.grid_columnconfigure(0, weight=0)
        
        self.resizable(width=False, height=False)

        self.firstNameInput = StringVar()
        self.lastNameInput = StringVar()
        self.usernameInput = StringVar()
        self.passwordInput = StringVar()
        self.userTypeOption = StringVar()
        self.userTypeOption.set("User")

        self.firstNameLabel = Label(self.entryFrame, text="First Name:", relief=FLAT).grid(column=0, row=0)
        self.firstNameEntry = Entry(self.entryFrame, textvariable=self.firstNameInput).grid(column=1, row=0)

        self.lastNameLabel = Label(self.entryFrame, text="Last Name:", relief=FLAT).grid(column=0, row=1)
        self.lastNameEntry = Entry(self.entryFrame, textvariable=self.lastNameInput).grid(column=1, row=1)

        self.usernameLabel = Label(self.entryFrame, text="Username:", relief=FLAT).grid(column=0, row=2)
        self.usernameEntry = Entry(self.entryFrame, textvariable=self.usernameInput).grid(column=1, row=2)

        self.passwordLabel = Label(self.entryFrame, text="Password:", relief=FLAT).grid(column=0, row=3)
        self.passwordEntry = Entry(self.entryFrame, textvariable=self.passwordInput, show= "*").grid(column=1, row=3)

        self.userTypeLabel = Label(self.entryFrame, text="User Type:", relief=FLAT).grid(column=0, row=4)
        self.userTypeUserRadiobutton = Radiobutton(self.entryFrame, text="User", relief=FLAT, variable=self.userTypeOption, value="User").grid(column=1, row=4)
        self.userTypeAdminRadiobutton = Radiobutton(self.entryFrame, text="Admin", relief=FLAT, variable=self.userTypeOption, value="Admin").grid(column=1, row=5)

        self.addUserDetailsButton = ttk.Button(self.entryFrame, text="Add User", command=self.addData).grid(row=6, columnspan=2, column=0)

    def addData(self):
        if messagebox.askyesno("Save", "Do you wish to add this user?"):
            self.detailsFile = open(os.getcwd()+"/loginDetails.txt", 'a')
            toAdd = "{0} {1} | {2} | {3} | {4}\n".format(self.firstNameInput.get(), self.lastNameInput.get(), self.usernameInput.get(), self.passwordInput.get(), self.userTypeOption.get())
            self.detailsFile.write(toAdd)
            self.detailsFile.close()
            users.append([self.usernameInput.get(), self.passwordInput.get(), self.firstNameInput.get()+" "+self.firstNameInput.get(), self.userTypeOption.get()])

            specuser = []
            for i in range(len(users)):
                if users[i] == self.firstNameInput.get()+" "+self.lastNameInput.get():
                    specuser = users[i]

            self.destroy()

class DisplayLangDetails(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Lang Details")
        self.option_add("*Font", 'TkDefaultFont')
        
        Label(self, text="Lang | English").grid(row=0, column=0)

        self.textScrollBar = Scrollbar(self)
        self.textScrollBar.grid(row=0, column=1, sticky="nsew", pady=10, padx=5)

        self.text = Text(self, yscrollcommand=self.textScrollBar.set, width=30, height=17)
        for word, translation in sorted(langDict.items()):
            if "(verb)" not in word:
                self.text.insert(END, "{0}|{1}\n".format(word, translation))

        self.textScrollBar.config(command=self.text.yview)
        
        self.text.grid(row=0, column=0, sticky=NSEW, pady=10, padx=5)
        self.text.config(state=DISABLED)
        
        self.resizable(width=False, height=False)
        self.text.edit_reset()

class DisplayEnglishDetails(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Display English Details")
        self.option_add("*Font", 'TkDefaultFont')
        
        Label(self, text="English | Lang").grid(row=0, column=0)

        self.textScrollBar = Scrollbar(self)
        self.textScrollBar.grid(row=1, column=1, sticky="nsew", pady=10, padx=5)

        self.text = Text(self, yscrollcommand=self.textScrollBar.set, width=30, height=17)

        for word, translation in sorted(engDict.items()):
            if "(verb)" not in word:
                self.text.insert(END, "{0}|{1}\n".format(word, translation))

        self.textScrollBar.config(command=self.text.yview)
        
        self.text.grid(row=1, column=0, sticky=NSEW, pady=10, padx=5)
        self.text.config(state=DISABLED)
        
        self.resizable(width=False, height=False)
        self.text.edit_reset()

class DisplayVerbDetails(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Display English Details")
        self.option_add("*Font", 'TkDefaultFont')
        
        Label(self, text="Verb | Translation").grid(row=0, column=0)

        self.textScrollBar = Scrollbar(self)
        self.textScrollBar.grid(row=1, column=1, sticky="nsew", pady=10, padx=5)

        self.text = Text(self, yscrollcommand=self.textScrollBar.set, width=30, height=17)

        for word, translation in sorted(engDict.items()):
            if "(verb)" in word:
                self.text.insert(END, "{0}|{1}\n".format(word.replace("(verb) ", ""), translation))

        self.textScrollBar.config(command=self.text.yview)
        
        self.text.grid(row=1, column=0, sticky=NSEW, pady=10, padx=5)
        self.text.config(state=DISABLED)
        
        self.resizable(width=False, height=False)
        self.text.edit_reset()

class EditEnglishDetails(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("View English Details")
        self.option_add("*Font", 'TkDefaultFont')
        
        Label(self, text="English | Lang").grid(row=0, column=0)

        self.textScrollBar = Scrollbar(self)
        self.textScrollBar.grid(row=1, column=1, sticky="nsew", pady=10, padx=5)

        self.text = Text(self, yscrollcommand=self.textScrollBar.set, width=30, height=17)

        for word, translation in sorted(engDict.items()):
            if "(verb)" not in word:
                self.text.insert(END, "{0}|{1}\n".format(word, translation))

        self.textScrollBar.config(command=self.text.yview)
        
        self.text.grid(row=1, column=0, sticky=NSEW, pady=10, padx=5)
        
        self.resizable(width=False, height=False)
        self.bind("<Control-s>", self.saveFile)
        self.text.edit_reset()
        ttk.Button(self, text="Save", command=self.saveFile).grid(row=2, column=0, columnspan=2)

    def saveFile(self, event=None):
        toWrite = ""
        for line in engDict:
            if "(verb)" in line:
                toWrite += "{0} | {1}\n".format(line, engDict[line])
                print("{0} | {1}".format(line.replace("  ", " "), engDict[line].replace("  ", " ")))
        toWrite += self.text.get("0.0", END)
        with open("engFile.txt", "w") as engFile:
            engFile.write(self.toWrite.replace("  ", " "))
        print(self.text.get("0.0", "end-1c").replace("  ", " "))
            
        print("Saving to English File...")

class EditLangDetails(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("View English Details")
        self.option_add("*Font", 'TkDefaultFont')
        
        Label(self, text="Lang | English").grid(row=0, column=0)

        self.textScrollBar = Scrollbar(self)
        self.textScrollBar.grid(row=1, column=1, sticky="nsew", pady=10, padx=5)

        self.text = Text(self, yscrollcommand=self.textScrollBar.set, width=30, height=17)

        for word, translation in sorted(langDict.items()):
            if "(verb)" not in word:
                self.text.insert(END, "{0}|{1}\n".format(word, translation))

        self.textScrollBar.config(command=self.text.yview)
        
        self.text.grid(row=1, column=0, sticky=NSEW, pady=10, padx=5)
        
        self.resizable(width=False, height=False)
        self.bind("<Control-s>", self.saveFile)
        self.text.edit_reset()
        ttk.Button(self, text="Save", command=self.saveFile).grid(row=2, column=0, columnspan=2)

    def saveFile(self, event=None):
        toWrite = ""
        for line in langDict:
            if "(verb)" in line:
                toWrite += "{0} | {1}\n".format(line, langDict[line])
                print("{0} | {1}".format(line.replace("  ", " "), langDict[line].replace("  ", " ")))
        toWrite += self.text.get("0.0", END)
        with open("langFile.txt", "w") as langFile:
            langFile.write(self.toWrite.replace("  ", " "))
        print(self.text.get("0.0", "end-1c").replace("  ", " "))
        print("Saving to Lang File...")

class EditVerbDetails(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("View English Details")
        self.option_add("*Font", 'TkDefaultFont')
        
        Label(self, text="Verb(English) | Verb(Lang)").grid(row=0, column=0)

        self.textScrollBar = Scrollbar(self)
        self.textScrollBar.grid(row=1, column=1, sticky="nsew", pady=10, padx=5)

        self.text = Text(self, yscrollcommand=self.textScrollBar.set, width=30, height=17)

        for word, translation in sorted(engDict.items()):
            if "(verb)" in word:
                self.text.insert(END, "{0}|{1}\n".format(word.replace("(verb) ", ""), translation))

        self.textScrollBar.config(command=self.text.yview)
        
        self.text.grid(row=1, column=0, sticky=NSEW, pady=10, padx=5)
        
        self.resizable(width=False, height=False)
        self.bind("<Control-s>", self.saveFile)
        self.text.edit_reset()
        ttk.Button(self, text="Save", command=self.saveFile).grid(row=2, column=0, columnspan=2)

    def saveFile(self, event=None):
        self.engWrite()
        self.langWrite()

        print("Saving verbs to English and Lang Files...")

    def setVerbs(self):
        verbs = []
        for line in self.text.get("0.0", "end-1c").split("\n"):
            print(line)
            try:
                verb = line.split("|")
                verbs.append("(verb) {0} | {1}".format(verb[0], verb[1]))
            except: continue
            
        for verb in verbs:
            self.toWrite += verb.replace("   ", " ")+"\n"

    def engWrite(self):
        self.toWrite = ""
        self.setVerbs()
        for line in engDict:
            if "(verb)" not in line:
                self.toWrite += "{0} | {1}\n".format(line, engDict[line])
                
        with open("engFile.txt", "w") as engFile:
            engFile.write(self.toWrite.replace("  ", " "))

    def langWrite(self):
        self.toWrite = ""
        self.setVerbs()
        for line in langDict:
            if "(verb)" not in line:
                self.toWrite += "{0} | {1}\n".format(line, langDict[line])
                
        with open("langFile.txt", "w") as langFile:
            langFile.write(self.toWrite.replace("  ", " "))

class UsersDetailsViewPage(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("View User Details")
        self.option_add("*Font", 'TkDefaultFont')

        self.noteBook = ttk.Notebook(self)

        for i in range(len(users)):
            self.noteBook.add(self.getUserViewFrame(users[i]), text=users[i][2])
        self.noteBook.pack()
        
        self.resizable(width=False, height=False)

    def getUserViewFrame(self, user):
        frame = Frame(self)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        Label(frame, text="User's name:").grid(row=0, column=0, sticky=W)
        nameText = Text(frame, height=1, width=20)
        nameText.insert("1.0", user[2])
        nameText.config(state=DISABLED)
        nameText.grid(row=0, column=1, sticky=E)

        Label(frame, text="Username:").grid(row=1, column=0, sticky=W)
        usernameText = Text(frame, height=1, width=20)
        usernameText.insert("1.0", user[0])
        usernameText.config(state=DISABLED)
        usernameText.grid(row=1, column=1, sticky=E)

        Label(frame, text="Password:").grid(row=2, column=0, sticky=W)
        passwordText = Text(frame, height=1, width=20)
        passwordText.insert("1.0", user[1])
        passwordText.config(state=DISABLED)
        passwordText.grid(row=2, column=1, sticky=E)

        Label(frame, text="User Access:").grid(row=3, column=0, sticky=W)
        accessText = Text(frame, height=1, width=20)
        accessText.insert("1.0", user[3])
        accessText.config(state=DISABLED)
        accessText.grid(row=3, column=1, sticky=E)
        
        return frame

class UsersDetailsEditPage(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Edit User Details")
        self.option_add("*Font", 'TkDefaultFont')

##        self.noteBook = ttk.Notebook(self)

        self.framesArray = []

        for i in range(len(users)):
            self.framesArray.append(userEditFrame(self, user=users[i], text=users[i][2]))
##            self.noteBook.add(frames[i], text=users[i][2])
##        self.noteBook.pack()

        self.frames = {}
        for frame in self.framesArray:
            self.frames[frame] = frame
            frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew", padx=10, pady=5)

        self.options = StringVar(self, users[0][2])
        self.userOptionMenu = OptionMenu(self, self.options, users[0][2], *(user[2] for user in users[1:]), command=self.raise_frame)
        self.raise_frame()
        self.userOptionMenu.grid(row=4, column=0, columnspan=3, pady=5)            
        
        self.resizable(width=False, height=False)

    def raise_frame(self, event=None):
        for frame in self.frames:
            if frame.user[2] == self.options.get():
                print("Change frame to {0}.".format(self.options.get()))
                frame.tkraise()

class userEditFrame(LabelFrame):
    def __init__(self, parent, **kwargs):
        LabelFrame.__init__(self, parent, text=kwargs["text"], padx=5, pady=5)

        self.user = kwargs["user"]
        self.parent = parent

        Label(self, text="Username:").grid(row=0, column=0, sticky=W)
        self.usernameValue = StringVar(self, self.user[0])
        self.usernameEntry = Entry(self, textvariable=self.usernameValue)
        self.usernameEntry.grid(row=0, column=1, sticky=E)
        
        Label(self, text="Password:").grid(row=1, column=0, sticky=W)
        self.passwordValue = StringVar(self, self.user[1])
        self.passwordEntry = Entry(self, textvariable=self.passwordValue)
        self.passwordEntry.grid(row=1, column=1, sticky=E)
        
        Label(self, text="User's name:").grid(row=2, column=0, sticky=W)
        self.nameValue = StringVar(self, self.user[2])
        self.nameEntry = Entry(self, textvariable=self.nameValue)
        self.nameEntry.grid(row=2, column=1, sticky=E)

        Label(self, text="User Access:").grid(row=3, column=0, sticky=W)
        self.userTypeOptions = StringVar(self, self.user[3])
        self.userAccessDrop = ttk.OptionMenu(self, self.userTypeOptions, user[3], "User", "Admin")
        self.userAccessDrop.config(width=10)
        self.userAccessDrop.grid(row=3, column=1, sticky=E)
        
        self.bind("<Control-s>", self.save)
        self.saveButton = ttk.Button(self, text="Save", command=self.save)
        self.saveButton.grid(row=4, column=0)
        self.saveButton = ttk.Button(self, text="Delete", command=self.delete)
        self.saveButton.grid(row=4, column=1)

    def save(self, event=None):
        pass
##        if messagebox.askyesno("Save", "Do you really want to make these changes to {0}'s accout?".format(self.data[2])):
##            for frame in self.parent.frames:
##                if frame.data[2] == self.parent.options.get():
##                    print("Edit user {0}'s data.".format(self.parent.options.get()))
##                    
##                    usersToKeep = []
##                    for user in users:
##                        print(user)
##                        if user[2] != self.parent.options.get():
##                            print(user, "to be kept")
##                            usersToKeep.append(user)
##                        else:
##                            continue
##                        
##                    for i in range(len(users)):
##                        try:
##                            if users[i][2] == self.parent.options.get():
##                                users[i]
##
##                        except: print(users)
##
##                usersFile = open(os.getcwd()+"/loginDetails.txt", 'w')
##                for user in usersToKeep:
##                    print(user)
##                    usersFile.write("{0} | {1} | {2} | {3}\n".format(user[2], user[0], user[1], user[3]))
##                messagebox.askquestion("Save", "The changes have been made to {0}'s account".format(self.data[2]))
##            
##        self.parent.attributes('-topmost', 1)
##        self.parent.attributes('-topmost', 0)

    def delete(self):
        if messagebox.askyesno("Delete user", "Are you sure that you wish to delete the user {0}?".format(self.parent.options.get())):
            for frame in self.parent.frames:
                if frame.user[2] == self.parent.options.get():
                    print("Delete user {0}.".format(self.parent.options.get()))
                    
                usersToKeep = []
                for user in users:
                    print(user)
                    if user[2] != self.parent.options.get():
                        print(user, "to be kept")
                        usersToKeep.append(user)
                    else:
                        continue
                    
                for i in range(len(users)):
                    try:
                        if users[i][2] == self.parent.options.get():
                            users.pop(i)

                    except: print(users)

            usersFile = open(os.getcwd()+"/loginDetails.txt", 'w')
            for user in usersToKeep:
                print(user)
                usersFile.write("{0} | {1} | {2} | {3}\n".format(user[2], user[0], user[1], user[3]))

            usersFile.close()
        self.parent.attributes('-topmost', 1)
        self.parent.attributes('-topmost', 0)

class loginPage(Frame):
    def __init__(self, parent, controller):

        Frame.__init__(self, parent)

        self.controller = controller
        self.parent = parent
        
        self.controller.mainMenu.entryconfig("Log Out", state="disabled")
        self.controller.mainMenu.entryconfig("Reset", state="disabled")

        self.controller.geometry("300x110")

        self.wrongDataLabel = Label(self, text="Either you username or password\n\
is invalid. Try again.")

        self.loginFrame = Frame(self)
        self.loginFrame.pack(fill="y")
        self.loginFrame.grid_rowconfigure(0, weight=0)
        self.loginFrame.grid_columnconfigure(0, weight=0)

        self.usernameInp = StringVar()
        self.usernameLabel = Label(self.loginFrame, text="Username: ").grid(column=0, row=0)
        self.usernameEntry = Entry(self.loginFrame, textvariable=self.usernameInp)
        self.usernameEntry.grid(column=1, row=0)

        self.usernameEntry.focus()

        self.passwordInp = StringVar()
        self.passwordLabel = Label(self.loginFrame, text="Password: ").grid(column=0, row=1)
        self.passwordEntry = Entry(self.loginFrame, show="*", textvariable=self.passwordInp)
        self.passwordEntry.grid(column=1, row=1)

        self.passwordEntry.bind("<Return>", self.checkLoginDetails)
        self.usernameEntry.bind("<Return>", self.checkLoginDetails)

        self.loginButton = ttk.Button(self, text="Login", command=self.checkLoginDetails).pack(pady=5)

    def checkLoginDetails(self, event=None):
        for user in users:
            if (self.usernameInp.get() == user[0]) and (self.passwordInp.get() == user[1]):
                userVar = user
                print(user[2], "logged in as", user[3])
                self.usernameEntry.delete(0, END)
                self.passwordEntry.delete(0, END)
                self.usernameInp.set("")
                self.passwordInp.set("")

                self.controller.mainMenu.entryconfig("Log Out", state="normal")
                self.controller.mainMenu.entryconfig("Reset", state="normal")

                if user[3].replace(" ", "") == "Admin":
                    self.loginAdmin()

                self.controller.geometry("290x320")
                self.controller.show_frame(homePage)

                return

        self.wrongDataLabel.pack(padx=5, pady=5)
        self.controller.geometry("300x140")

    def loginAdmin(self):

        self.controller.filesMenu = Menu(self.controller.mainMenu, tearoff=0)
        self.controller.filesViewMenu = Menu(self.controller.filesMenu, tearoff=0)
        self.controller.filesEditMenu = Menu(self.controller.filesMenu, tearoff=0)
        self.controller.usersMenu = Menu(self.controller.mainMenu, tearoff=0)
        
        makeMenusItem(self.controller.mainMenu, {"File": self.controller.filesMenu,
                                                 "User": self.controller.usersMenu}, {})
        
        makeMenusItem(self.controller.filesMenu, {"View Files": self.controller.filesViewMenu,
                                                  "Edit Files": self.controller.filesEditMenu}, {})
        
        makeMenusItem(self.controller.filesViewMenu, {}, {"View English File": DisplayEnglishDetails,
                                                          "View Lang Files": DisplayLangDetails,
                                                          "View Verbs": DisplayVerbDetails})
        
        makeMenusItem(self.controller.filesEditMenu, {}, {"Edit English File": EditEnglishDetails,
                                                          "Edit Lang Files": EditLangDetails,
                                                          "Edit Verbs": EditVerbDetails})

        makeMenusItem(self.controller.usersMenu, {}, {"Add User Data": addUserDataPage,
                                                      "View User Data": UsersDetailsViewPage,
                                                      "Edit User Data": UsersDetailsEditPage})

        generateMenuBar(self.controller, self.controller.mainMenu)
        
class homePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.noteBook = ttk.Notebook(self)
        self.noteBook.add(searchPage(self, self.controller), text="Search")
        self.noteBook.add(listPage(self, self.controller), text="List")
        self.noteBook.add(addPage(self, self.controller), text="Add")
        self.noteBook.pack()

class searchPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller
        
        self.language = engDict
        self.searchType = "normal"

        self.entryFrame = Frame(self)
        self.entryFrame.pack(padx=5, pady=5)
        self.entryFrame.grid_rowconfigure(0, weight=0)
        self.entryFrame.grid_columnconfigure(0, weight=0)

        resultsFrame = Frame(self)
        resultsFrame.pack(padx=5, pady=5)
        resultsFrame.grid_rowconfigure(0, weight=0)
        resultsFrame.grid_columnconfigure(0, weight=0)

        resultsScrollBar = Scrollbar(resultsFrame)
        resultsScrollBar.grid(row=2, column=1, sticky="nsew")

        self.resultsText = Text(resultsFrame, yscrollcommand=resultsScrollBar.set, width=35, height=10)
        self.resultsText.grid(row=2, column=0, padx=5, sticky="W")

        resultsScrollBar.config(command=self.resultsText.yview)

        searchLabel = Label(self.entryFrame, text="Enter text here:").grid(row=0, column=0)
        self.searchVar = StringVar()
        searchEntry = Entry(self.entryFrame, textvariable=self.searchVar)
        searchEntry.grid(column=1, row=0, padx=5)
        clearButton = ttk.Button(self.entryFrame, text="Clear", command=self.clearFrame).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        searchEntry.bind("<Return>", self.searchDict)

        languageSelFrame = Frame(self)
        languageSelFrame.pack(padx=5, pady=5)
        languageSelFrame.grid_rowconfigure(0, weight=0)
        languageSelFrame.grid_columnconfigure(0, weight=0)

        engLanuageButton = ttk.Button(languageSelFrame, text="English", command=lambda: self.setLanguage(engDict, "normal")).grid(column=0, row=0)
        langLanuageButton = ttk.Button(languageSelFrame, text="Lang", command=lambda: self.setLanguage(langDict, "normal")).grid(column=2, row=0)
        verbLanuageButton = ttk.Button(languageSelFrame, text="Verb", command=lambda: self.setLanguage(engDict, "verb")).grid(column=1, row=0)

        self.resultsText.config(state=DISABLED)
        self.resultsText.edit_reset()

    def setLanguage(self, language, searchType):
        self.language = language
        self.searchType = searchType
        self.searchDict()

    def searchDict(self, event=None):
        results = []
        if self.searchType == "verb":
            for x in self.language:
                if "(verb)" in x:
                    if (self.searchVar.get().lower() in x.lower()):
                        results.append("{0}|{1}\n".format(x.replace("(verb) ", ""), self.language[x]))

        else:
            for x in self.language:
                if "(verb)" in x:
                   continue

                if (self.searchVar.get().lower() in x.lower()):
                    results.append("{0}|{1}\n".format(x, self.language[x]))

        self.results = results
        self.resultsText.config(state=NORMAL)

        self.resultsText.delete("1.0", "end")
        for result in self.results:
            self.resultsText.insert("end", result)

        self.resultsText.config(state=DISABLED)
        self.resultsText.edit_reset()

    def clearFrame(self):
        self.resultsText.config(state=NORMAL)
        self.resultsText.delete('1.0', "end")
        self.resultsText.config(state=DISABLED)
        self.resultsText.edit_reset()

class addPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.entryFrame = Frame(self)
        self.entryFrame.pack(padx=5, pady=5)
        self.entryFrame.grid_rowconfigure(0, weight=0)
        self.entryFrame.grid_columnconfigure(0, weight=0)

        self.engWordVar = StringVar()
        self.langWordVar = StringVar()

        self.engWordEntryLabel = Label(self.entryFrame, text="English Word", relief=FLAT).grid(column=0, row=0, padx=5, pady=5)
        self.engWordEntry = Entry(self.entryFrame, textvariable=self.engWordVar, relief=FLAT).grid(column=1, row=0, padx=5, pady=5)

        self.langWordEntryLabel = Label(self.entryFrame, text="Lang Word", relief=FLAT).grid(column=0, row=1, padx=5, pady=5)
        self.langWordEntry = Entry(self.entryFrame, textvariable=self.langWordVar, relief=FLAT).grid(column=1, row=1, padx=5, pady=5)

        self.addButton = ttk.Button(self, text="Add", command=self.addWords).pack(padx=5, pady=5)
        self.addVerb = ttk.Button(self, text="Add Verb", command=self.addVerbs).pack(padx=5, pady=5)
        
    def addWords(self):
        f = open(dicts[0].addFile, 'a')
        f.write("{0} | {1}".format(self.engWordVar.get(), self.langWordVar.get()).replace("  ", " "))
        f.close()
        for file in [dicts[0]]:
            file.addToDicts(dicts)

        messagebox.showinfo("Added", "\"{0} | {1}\" has been added to the dictionary".format(self.engWordVar.get(), self.langWordVar.get()))

        updateDicts()
        
    def addVerbs(self):
        f = open(dicts[0].addFile, 'a')
        f.write("(verb) {0} | {1}".format(self.engWordVar.get(), self.langWordVar.get()).replace("  ", " "))
        f.close()
        for file in [dicts[0]]:
            file.addToDicts(dicts)

        messagebox.showinfo("Added", "\"{0} | {1}\" has been added to the dictionary".format(self.engWordVar.get(), self.langWordVar.get()))

        updateDicts()

class listPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.notebook = ttk.Notebook(self)
        self.notebook.add(EngList(self.controller, self), text="English")
        self.notebook.add(LangList(self.controller, self), text="Lang")
        self.notebook.add(VerbList(self.controller, self), text="Verb")
        self.notebook.pack()

    def raiseFrame(self, frame):
        frame.tkraise()

class LangList(Frame):
    def __init__(self, controller, parent):
        Frame.__init__(self, parent)

        langListFrame = Frame(self)
        langListFrame.grid(column=0, row=0)
        langListFrame.grid_rowconfigure(0, weight=0)
        langListFrame.grid_columnconfigure(0, weight=0)

        langWordLabels = []

        for word in langDict:
            if word[:6] == "(verb)":
                continue
            langWordLabels.append("{0}| {1}\n".format(word, langDict[word][1:]))

        langScrollBar = Scrollbar(langListFrame, relief=FLAT)
        langScrollBar.grid(column=1, row=0, sticky="ns")

        langText = Text(langListFrame, yscrollcommand=langScrollBar.set, width=35, height=14, relief=FLAT)
        for i in langWordLabels:
            langText.insert("end", i)
        langText.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        langScrollBar.config(command=langText.yview)
        langText.config(state=DISABLED)
        langText.edit_reset()

class EngList(Frame):
    def __init__(self, controller, parent):
        Frame.__init__(self, parent)

        engListFrame = Frame(self)
        engListFrame.grid(column=0, row=0)
        engListFrame.grid_rowconfigure(0, weight=0)
        engListFrame.grid_columnconfigure(0, weight=0)

        engWordLabels = []

        for word in engDict:
            if word[:6] == "(verb)":
                continue
            engWordLabels.append("{0}| {1}\n".format(word, engDict[word][1:]))

        engScrollBar = Scrollbar(engListFrame, relief=FLAT)
        engScrollBar.grid(column=1, row=0, sticky="ns")

        engText = Text(engListFrame, yscrollcommand=engScrollBar.set, width=35, height=14, relief=FLAT)
        for i in engWordLabels:
            engText.insert("end", i)
        engText.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        engScrollBar.config(command=engText.yview)
        engText.config(state=DISABLED)
        engText.edit_reset()

class VerbList(Frame):
    def __init__(self, controller, parent):
        Frame.__init__(self, parent)

        verbListFrame = Frame(self, relief=FLAT)
        verbListFrame.grid(column=0, row=0)
        verbListFrame.grid_rowconfigure(0, weight=0)
        verbListFrame.grid_columnconfigure(0, weight=0)

        verbWordLabels = []

        for word in engDict:
            if "(verb)" in word:
                verbWordLabels.append("{0}| {1}\n".format(word.replace("(verb) ", ""), engDict[word][1:]))

        verbScrollBar = Scrollbar(verbListFrame, relief=FLAT)
        verbScrollBar.grid(column=1, row=0, sticky="ns")

        verbText = Text(verbListFrame, yscrollcommand=verbScrollBar.set, width=35, height=14, relief=FLAT)
        for i in verbWordLabels:
            verbText.insert("end", i)
        verbText.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        verbScrollBar.config(command=verbText)
        verbText.config(state=DISABLED)
        verbText.edit_reset()

def updateDicts():
    dicts = main()
    engDict = dicts[0].dictionary
    langDict = dicts[1].dictionary

    return dicts, langDict, engDict

def makeMenusItem(parent, cascades, commands):
    menus[parent] = {"cascades": cascades,
                     "commands": commands}

def generateMenuBar(master, menuBar):
    for menu in menus:
        currMenu = menus[menu]
        for addType, values in currMenu.items():
            if addType == "cascades":
                for label, extendMenu in values.items():
##                        print("Cascade:", label+"\n")
                    menu.add_cascade(label=label, menu=extendMenu)
                
            elif addType == "commands":
                try:
                    for label, command in values.items():
                        menu.add_command(label=label, command=command)
                        
                except AttributeError:
                    pass
        
    master.config(menu=menuBar)

    

dicts, langDict, engDict = updateDicts()
global userVar
global menus
menus = {}

detailsFile = open(os.getcwd()+"/loginDetails.txt", 'r')
detailsCsvFile = csv.reader(detailsFile, delimiter="|")

users = []

for record in detailsCsvFile:
    username = record[1].replace(" ", "")
    password = record[2].replace(" ", "")
    name = record[0]
    usertype = record[3].replace(" ", "")

    users.append([username, password, name, usertype])

for user in users:
    print("={0:=^16}+{0:=^17}+{0:=^16}+{0:=^11}=".format("="))
    print("|{0:^15} | {1:^15} | {2:^15}| {3:^10}|".format(user[0].replace(" ", ""), user[1].replace(" ", ""), user[2].replace(" ", ""), user[3].replace(" ", "")))
print("={0:=^16}+{0:=^17}+{0:=^16}+{0:=^11}=".format("="))

username = None
password = None
name = None
usertype = None

detailsFile.close()

app = langApp()
