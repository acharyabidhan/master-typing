import pygame, darkdetect, numpy as np
from tkinter import*
from win32api import GetMonitorInfo, MonitorFromPoint
pygame.mixer.init()
pygame.mixer.music.load("Typing Test\\assets\\e.mp3")
app = Tk()
darKColor = "#202020"
lightColor = "white"
currentColor = None
sysTheme = darkdetect.isDark()
match sysTheme:
    case True:currentColor = darKColor
    case False:currentColor = lightColor
    case _:currentColor = darKColor
appTitle = "Master Typing -Test your typing skills here v1.0"
app.resizable(0,0)
app.overrideredirect(1)
app.config(background=currentColor)
monitorInfo = GetMonitorInfo(MonitorFromPoint((0,0)))
screenSize = monitorInfo.get("Monitor")
taskarHeight = monitorInfo.get("Work")
screenWidth = screenSize[2]
screenHeight = screenSize[3]
windowWidth = screenSize[2]
windowHeight = screenSize[3] - (screenSize[3] - taskarHeight[3])
app.geometry(f"{windowWidth}x{windowHeight}+0+0")
offsetx = 0
offsety = 0
def dragWindow(event):
    pointerX = app.winfo_pointerx() - app.offsetx
    pointerY = app.winfo_pointery() - app.offsety
    app.geometry(f"+{pointerX}+{pointerY}")
def primaryClick(event):
    app.offsetx = event.x
    app.offsety = event.y
play = True
def playSound():
    global play
    if play:
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()
        play = False
def avoidLongPress():
    global play
    play = True
def detectKeyPress(e):
    key = e.keysym
    if key == "Down":
        ypos = round(screenHeight/2)
        app.geometry(f"{windowWidth}x{windowHeight}+0+{ypos}")
    playSound()
    if started:
        checkWords(key)
def detectKeyRelease(e):
    avoidLongPress()
toolbarColor = "green"
toolbarFrame = Frame(app, background=toolbarColor, bd=0)
toolbarFrame.place(x=0, y=0, width=windowWidth, height=screenHeight-(screenHeight-20))
titleLabel = Label(toolbarFrame, text=appTitle, background=toolbarColor, foreground="white")
titleLabel.place(relx=0.00,rely=0.50, anchor=W)
def closeHighlight(e):closeButton.config(background="red",foreground="white")
def closeDefault(e):closeButton.config(background=toolbarColor,foreground="red")
def closeWindow():
    app.destroy()
closeButton = Button(toolbarFrame, text="❌", width=2, background=toolbarColor, foreground="red", bd=0, activebackground="red",activeforeground="white",command=closeWindow)
closeButton.place(relx=1.00, rely=0.50, anchor=E, height=screenHeight-(screenHeight-20))
def minHighlight(e):minButton.config(background="white",foreground="black")
def minDefault(e):minButton.config(background=toolbarColor,foreground="white")
def minimizeWindow():
    app.withdraw()
    app.overrideredirect(False)
    app.iconify()
minButton = Button(toolbarFrame, text="➖", width=2, background=toolbarColor, foreground="white", bd=0, activebackground="white",activeforeground="black",command=minimizeWindow)
minButton.place(relx=0.98, rely=0.50, anchor=E, height=screenHeight-(screenHeight-20))
app.bind("<KeyPress>", detectKeyPress)
app.bind("<KeyRelease>", detectKeyRelease)
toolbarFrame.bind('<B1-Motion>', dragWindow)
toolbarFrame.bind('<Button-1>', primaryClick)
closeButton.bind("<Enter>",closeHighlight)
closeButton.bind("<Leave>",closeDefault)
minButton.bind("<Enter>",minHighlight)
minButton.bind("<Leave>",minDefault)
def resetWindowPos(e):app.geometry(f"{windowWidth}x{windowHeight}+0+0")
toolbarFrame.bind('<Double-Button-1>', resetWindowPos)
app.protocol('WM_DELETE_WINDOW', closeWindow)
def check_map(event):
    if str(event) == "<Map event>":
        app.overrideredirect(1)
app.bind('<Map>', check_map)
app.bind('<Unmap>', check_map)
app.attributes('-topmost',True)
#App contents from here
######################


def getWords(num=40):
    with open("Typing Test\\assets\\words","r") as wf:
        wordsList = wf.readlines()
    allWords = []
    for i in wordsList:
        allWords.append(i[:-1])
    words = np.random.choice(allWords, num)
    return words


randomW = IntVar(value=1)
customW = IntVar()
numberOfWords = IntVar()
numberOfWords.set(value=10)
cWords = getWords(numberOfWords.get())
letterIndex = 0
mistakes = 0
typed = 0
mistakesList = []
cWIndex = 0
pCwords = " ".join(cWords)
started = False


def checkWords(key):
    global letterIndex, mistakes, typed, cWIndex
    if letterIndex > len(pCwords)-1:
        return
    else:
        if key == "space":
            key = " "
        if len(key) == 1:
            if ord(key) == ord(pCwords[letterIndex]):
                textField.tag_config("a", foreground="#00ff55")
                textField.tag_add("a", f"1.{letterIndex}", f"1.{letterIndex+1}")
                if key == " ":cWIndex += 1
            else:
                mistakes += 1
                mistakesList.append(f"{pCwords[letterIndex]}:{key}")
                textField.tag_config("b", foreground="red")
                textField.tag_add("b", f"1.{letterIndex}", f"1.{letterIndex+1}")
                if pCwords[letterIndex] == " " and key != " ":cWIndex += 1                   
            typed += 1
            updateInformaation()
            letterIndex += 1
            showMistake()


def showMistake():
    print("Letter mistakes:",mistakes)
    print(mistakesList)


def updateInformaation():
    if not mistakes:
        tyingAccuracy.config(text=f"Accuracy: 100.00 %")
    else:    
        accuracyPercentage = round(100 - ((mistakes/typed)*100), 2)
        tyingAccuracy.config(text=f"Accuracy: {accuracyPercentage} %")
    plainWords = " ".join(cWords)

    currentWord.config(text=f"Current Word: {cWords[cWIndex]}")
    try:nextWord.config(text=f"Next Word: {cWords[cWIndex+1]}")
    except:nextWord.config(text=f"Next Word: N/A")
    try:
        nL = plainWords[letterIndex+1]
        if nL == " ":nL = "space"
        nextLetter.config(text=f"Next Character: {nL}")
    except:nextLetter.config(text=f"Next Character: N/A")


def startGame():
    global started, cWords, pCwords
    if randomW.get():customWords.config(state=DISABLED)
    else:randomWords.config(state=DISABLED)
    if randomW.get():
        cWords = getWords(numberOfWords.get())
        pCwords = " ".join(cWords)
    else:
        cText = textField.get(1.0, "end")
        if len(cText) >= 2:
            if "." in cText:cText = cText.replace(".","")
            ccWords = cText.split(" ")
            cWords = []
            for k in ccWords:
                if "\n" in k:cWords.append(k[:-1])
                else:cWords.append(k)
            pCwords = " ".join(cWords)
        else:
            cWords = ["Enter", "your", "words", "here"]
            pCwords = " ".join(cWords)
    started = True
    startButton.config(state=DISABLED)
    textField.config(state=NORMAL)
    textField.delete("1.0", "end")
    textField.insert(INSERT, pCwords)
    textField.config(state=DISABLED)
    try:currentWord.config(text=f"Current Word: {cWords[0]}")
    except:currentWord.config(text=f"Current Word: N/A")
    try:nextWord.config(text=f"Next Word: {cWords[0+1]}")
    except:nextWord.config(text=f"Next Word: N/A")
    try:nextLetter.config(text=f"Next Character: {cWords[0][0]}")
    except:nextLetter.config(text=f"Next Character: N/A")


def resetGame():
    global started, cWords, pCwords, letterIndex, mistakes, typed, mistakesList, cWIndex
    if randomW.get():customWords.config(state=NORMAL)
    else:randomWords.config(state=NORMAL)
    started = False
    cWords = getWords(numberOfWords.get())
    pCwords = " ".join(cWords)
    letterIndex = 0
    mistakes = 0
    typed = 0
    mistakesList = []
    cWIndex = 0
    startButton.config(state=NORMAL)
    textField.config(state=NORMAL)
    textField.delete("1.0", "end")
    currentWord.config(text="Current Word: N/A")
    nextWord.config(text="Next Word: N/A")
    nextLetter.config(text="Next Character: N/A")
    tyingAccuracy.config(text="Accuracy: N/A")


def chooseRandomWords():
    customWords.config(state=NORMAL)
    customW.set(0)
    textField.delete("1.0", "end")
    textField.insert(INSERT, "Press enter or start button to get random words")
    textField.config(state=DISABLED)
    randomWords.config(state=DISABLED)
    wordsLimit.config(state=NORMAL)


def chooseCustomWords():
    randomWords.config(state=NORMAL)
    randomW.set(0)
    textField.config(state=NORMAL)
    textField.delete("1.0", "end")
    textField.insert(INSERT, "Enter your words here")
    customWords.config(state=DISABLED)
    wordsLimit.config(state=DISABLED)


textField = Text(app, font=("arial",20), background="#404040", bd=0, foreground="white", spacing1=2, spacing2=4, state=DISABLED)
textField.place(x=10, y=screenHeight-(screenHeight-20)+10, width=screenWidth-20, height=round(screenHeight/4))


infoFrame = Frame(app, background="#404040")
infoFrame.place(x=10, y=round(screenHeight/4)+40, width=screenWidth-20, height=round(screenHeight/18))


currentWord = Label(infoFrame, text=f"Current Word: N/A", font=("arial",18),background="#404040", foreground=lightColor)
currentWord.place(relx=0.00, rely=0.50, anchor=W)


nextLetter = Label(infoFrame, text=f"Next Character: N/A", font=("arial",18),background="#404040", foreground=lightColor)
nextLetter.place(relx=0.30, rely=0.50, anchor=W)


nextWord = Label(infoFrame, text=f"Next Word: N/A", font=("arial",18),background="#404040", foreground=lightColor)
nextWord.place(relx=0.70, rely=0.50, anchor=E)


tyingAccuracy = Label(infoFrame, text="Accuracy: N/A", font=("arial",18),background="#404040", foreground=lightColor)
tyingAccuracy.place(relx=1.00, rely=0.50, anchor=E)


settingsFrame = LabelFrame(app, bd=0,)
settingsFrame.place(x=10, y=round(windowHeight-(windowHeight/4))-10, width=windowWidth-20, height=round(windowHeight/4))


#Words settings
wordsSetting = LabelFrame(settingsFrame, text="Words Settings", labelanchor="n",background="#404040",bd=4,font=("arial",12),foreground="white")
wordsSetting.place(relx=0.00,rely=0.00,anchor=NW,height=round(windowHeight/4),width=round(screenWidth/3))


randomWords = Checkbutton(wordsSetting, text="Practice random words", font=("arial", 18), anchor="w", command=chooseRandomWords, variable=randomW, state=DISABLED)
randomWords.place(relx=0.50, rely=0.06, anchor=N, width=round(screenWidth/3)-40)


customWords = Checkbutton(wordsSetting, text="Practice custom words", font=("arial", 18), anchor="w", command=chooseCustomWords, variable=customW)
customWords.place(relx=0.50, rely=0.50, anchor=CENTER, width=round(screenWidth/3)-40)


wordsLimit = Scale(wordsSetting, from_=1, to=60, orient="horizontal", variable=numberOfWords)
wordsLimit.place(relx=0.50, rely=0.94, anchor=S, width=round(screenWidth/3)-40)


#Typing mode settings
typeMode = LabelFrame(settingsFrame, text="Typing Settings", labelanchor="n",background="#404040",bd=4,font=("arial",12),foreground="white")
typeMode.place(relx=0.333333,rely=0.00,anchor=NW,height=round(windowHeight/4),width=round(screenWidth/3))


#Controls and timing settings
controlsFrame = LabelFrame(settingsFrame, text="Controls", labelanchor="n",background="#404040",bd=4,font=("arial",12),foreground="white")
controlsFrame.place(relx=0.666666,rely=0.00,anchor=NW,height=round(windowHeight/4),width=round(screenWidth/3))


timerLabel = Label(controlsFrame, text="00:00", background="#404040",font=("arial",40),foreground="white")
timerLabel.place(relx=0.50,rely=0.10,anchor=N)


startButton = Button(controlsFrame, text="Start", command=startGame, bd=0, font=("arial", 15), width=10)
startButton.place(relx=0.20,rely=0.90,anchor=SW)


resetButton = Button(controlsFrame, text="Reset", command=resetGame, bd=0, font=("arial", 15), width=10)
resetButton.place(relx=0.80,rely=0.90,anchor=SE)


######################
app.mainloop()
#This much :)