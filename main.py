import pygame, darkdetect, numpy as np, time
from tkinter import*
from tkinter import messagebox
from win32api import GetMonitorInfo, MonitorFromPoint

pygame.mixer.init()
pygame.mixer.music.load("assets\\e.mp3")

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
playing = True
def playSound():
    global play
    if play and playing:
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()
        play = False

def avoidLongPress():
    global play
    play = True

def detectKeyPress(e):
    global time0
    key = e.keysym
    if key == "Return" and not started:
        time0 = time.time()
        startGame()
    if key == "Escape":resetGame()
    playSound()
    if started:checkWords(key)

def detectKeyRelease(e):avoidLongPress()

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
#App contents from here

cEasy = IntVar()
cMedium = IntVar()
cMedium.set(value=1)
cHard = IntVar()

def getWords(num=40):
    if cEasy.get():wordFile = "easy"
    elif cMedium.get():wordFile = "medium"
    else:wordFile = "hard"
    with open(f"assets\\{wordFile}","r") as wf:#word file
        wordsList = wf.readlines()
    allWords = []
    for i in wordsList:
        allWords.append(i[:-1])
    words = np.random.choice(allWords, num)
    return words


wpmChecking = False
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
time0 = None
typingDelay = None
timeList = []

def checkWords(key):
    global letterIndex, mistakes, typed, cWIndex, typingDelay, time0
    if letterIndex > len(pCwords)-1:
        if wpmChecking:showWPM()
        return
    else:
        if cWIndex > 40:textField.see("end")
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
            time1 = time.time()
            typingDelay = time1 - time0
            time0 = time.time()
            timeList.append(typingDelay)
            typed += 1
            updateInformaation()
            letterIndex += 1
            showMistake()

def showWPM():
    noOfWoTyped = len(cWords[:cWIndex])
    noOfChar = len(" ".join(cWords[:cWIndex]))
    if noOfWoTyped == 0 or noOfChar == 0:
        wpmLabel.config(text=f"WPM: 1")
        return
    avgWordNo = round(noOfChar / noOfWoTyped)
    WPM = round((noOfChar / avgWordNo) * 1.5)
    wpmLabel.config(text=f"WPM: {WPM}")

def showMistake():
    print("Total mistakes:",mistakes)
    print("Total words:", len(cWords))
    print("Total letters:", len(pCwords))
    print("Total time:",sum(timeList))

def updateInformaation():
    global finished
    if not mistakes:
        tyingAccuracy.config(text=f"Accuracy: 100.00 %")
    else:    
        accuracyPercentage = round(100 - ((mistakes/typed)*100), 2)
        tyingAccuracy.config(text=f"Accuracy: {accuracyPercentage} %")
    plainWords = " ".join(cWords)
    currentWord.config(text=f"Current Word: {cWords[cWIndex]}")
    try:nextWord.config(text=f"Next Word: {cWords[cWIndex+1]}")
    except:nextWord.config(text=f"Next Word: ...")
    try:
        nL = plainWords[letterIndex+1]
        if nL == " ":nL = "space"
        nextLetter.config(text=f"Next Character: {nL}")
    except:
        finished = True
        nextLetter.config(text=f"Next Character: ...")

finished = True
seconds = 0
minutes = 0
def startTimer():
    global seconds, started, minutes, loading
    if finished:return
    if wpmChecking and minutes == 1:
        started = False
        showWPM()
        return
    if seconds > 59:
        seconds = 0
        minutes += 1
    timerLabel.config(text=f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}")
    app.after(1000, startTimer)
    seconds += 1

def startGame():
    global started, cWords, pCwords, time0, finished
    finished = False
    time0 = time.time()
    startTimer()
    if wpmChecking:
        wpmLabel.config(text=f"WPM: ...")
    if randomW.get():customWords.config(state=DISABLED)
    else:randomWords.config(state=DISABLED)
    if cWpm.get():freeTyping.config(state=DISABLED)
    else:wpmTest.config(state=DISABLED)
    if randomW.get():
        cWords = getWords(numberOfWords.get())
        pCwords = " ".join(cWords)
        print("Lenggth of words",len(pCwords))
    else:
        cText = textField.get(1.0, "end")
        if len(cText) >= 2:
            if "." in cText:cText = cText.replace(".","")
            if "," in cText:cText = cText.replace(",","")
            ccWords = cText.split(" ")
            cWords = []
            wCount = 0
            for k in ccWords:
                if wCount > 60:break
                if "\n" in k:cWords.append(k[:-1])
                else:cWords.append(k)
                wCount += 1
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
    except:currentWord.config(text=f"Current Word: ...")
    try:nextWord.config(text=f"Next Word: {cWords[0+1]}")
    except:nextWord.config(text=f"Next Word: ...")
    try:nextLetter.config(text=f"Next Character: {cWords[0][0]}")
    except:nextLetter.config(text=f"Next Character: ...")

def resetGame():
    global started, cWords, pCwords, letterIndex, mistakes, typed, mistakesList, cWIndex, time0, timeList, typingDelay, finished, seconds, minutes, wpmChecking
    if cWpm.get():wpmChecking = True
    else:wpmChecking = False
    seconds = 0
    minutes = 0
    finished = True
    timerLabel.config(text="00:00")
    time0 = None
    typingDelay = None
    timeList = []
    if randomW.get():customWords.config(state=NORMAL)
    else:randomWords.config(state=NORMAL)
    if cWpm.get():freeTyping.config(state=NORMAL)
    else:wpmTest.config(state=NORMAL)
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
    currentWord.config(text="Current Word: ...")
    nextWord.config(text="Next Word: ...")
    nextLetter.config(text="Next Character: ...")
    tyingAccuracy.config(text="Accuracy: ...")
    wpmLabel.config(text="WPM: ...")

def chooseRandomWords():
    customWords.config(state=NORMAL)
    customW.set(0)
    textField.delete("1.0", "end")
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

currentWord = Label(infoFrame, text=f"Current Word: ...", font=("arial",18),background="#404040", foreground=lightColor)
currentWord.place(relx=0.00, rely=0.50, anchor=W)

nextLetter = Label(infoFrame, text=f"Next Character: ...", font=("arial",18),background="#404040", foreground=lightColor)
nextLetter.place(relx=0.30, rely=0.50, anchor=W)

nextWord = Label(infoFrame, text=f"Next Word: ...", font=("arial",18),background="#404040", foreground=lightColor)
nextWord.place(relx=0.70, rely=0.50, anchor=E)

tyingAccuracy = Label(infoFrame, text="Accuracy: ...", font=("arial",18),background="#404040", foreground=lightColor)
tyingAccuracy.place(relx=1.00, rely=0.50, anchor=E)

settingsFrame = LabelFrame(app, bd=0,)
settingsFrame.place(x=10, y=round(windowHeight-(windowHeight/4))-10, width=windowWidth-20, height=round(windowHeight/4))

wordsSetting = LabelFrame(settingsFrame,background="#404040",bd=2,font=("arial",12),foreground="white")
wordsSetting.place(relx=0.00,rely=0.00,anchor=NW,height=round(windowHeight/4),width=round(screenWidth/3))

randomWords = Checkbutton(wordsSetting, text="Play with random words", font=("arial", 18), anchor="w", command=chooseRandomWords, variable=randomW, state=DISABLED)
randomWords.place(relx=0.50, rely=0.06, anchor=N, width=round(screenWidth/3)-40)

customWords = Checkbutton(wordsSetting, text="Play with your words", font=("arial", 18), anchor="w", command=chooseCustomWords, variable=customW)
customWords.place(relx=0.50, rely=0.50, anchor=CENTER, width=round(screenWidth/3)-40)

wordsLimit = Scale(wordsSetting, from_=1, to=70, orient="horizontal", variable=numberOfWords)
wordsLimit.place(relx=0.50, rely=0.94, anchor=S, width=round(screenWidth/3)-40)

typeMode = LabelFrame(settingsFrame,background="#404040",bd=2,font=("arial",12),foreground="white")
typeMode.place(relx=0.333333,rely=0.00,anchor=NW,height=round(windowHeight/4),width=round(screenWidth/3))

freeTyp = IntVar()
freeTyp.set(value=1)
cWpm = IntVar()
cWpm.set(value=0)

def enableFreeTyping():
    global wpmChecking
    wpmChecking = False
    wpmTest.config(state=NORMAL)
    freeTyping.config(state=DISABLED)
    cWpm.set(value=0)
    if randomW.get():customWords.config(state=NORMAL)
    wordsLimit.config(state=NORMAL)


def enableCheckWpm():
    global wpmChecking
    wpmChecking = True
    wpmTest.config(state=DISABLED)
    freeTyping.config(state=NORMAL)
    freeTyp.set(value=0)
    if customW.get():
        customW.set(0)
        randomW.set(1)
        chooseRandomWords()
    numberOfWords.set(70)
    wordsLimit.config(state=DISABLED)
    customWords.config(state=DISABLED)

freeTyping = Checkbutton(typeMode, text="Free typing", font=("arial", 18), anchor="w", variable=freeTyp,command=enableFreeTyping, state=DISABLED)
freeTyping.place(relx=0.50, rely=0.06, anchor=N, width=round(screenWidth/3)-40)

wpmTest = Checkbutton(typeMode, text="Check WPM", font=("arial", 18), anchor="w", variable=cWpm,command=enableCheckWpm)
wpmTest.place(relx=0.50, rely=0.50, anchor=CENTER, width=round(screenWidth/3)-40)

kpSound = IntVar()
kpSound.set(value=1)

def keypressSound():
    global playing
    if playing:playing = False
    else:playing = True

keyPress = Checkbutton(typeMode, text="Keypress sound", font=("arial", 18), anchor="w", command=keypressSound, variable=kpSound)
keyPress.place(relx=0.50, rely=0.94, anchor=S, width=round(screenWidth/3)-40)

controlsFrame = LabelFrame(settingsFrame,background="#404040",bd=2,font=("arial",12),foreground="white")
controlsFrame.place(relx=0.666666,rely=0.00,anchor=NW,height=round(windowHeight/4),width=round(screenWidth/3))

wpmLabel = Label(controlsFrame, text="WPM: ...", background="#404040",font=("arial",30),foreground="white")
wpmLabel.place(relx=0.10,rely=0.08,anchor=NW)

timerLabel = Label(controlsFrame, text="00:00", background="#404040",font=("arial",30),foreground="white")
timerLabel.place(relx=0.90,rely=0.08,anchor=NE)

def chooseEasy():
    easyWords.config(state=DISABLED)
    mediumWords.config(state=NORMAL)
    hardWords.config(state=NORMAL)
    cMedium.set(value=0)
    cHard.set(value=0)

def chooseMedium():
    easyWords.config(state=NORMAL)
    mediumWords.config(state=DISABLED)
    hardWords.config(state=NORMAL)
    cEasy.set(value=0)
    cHard.set(value=0)

def chooseHard():
    easyWords.config(state=NORMAL)
    mediumWords.config(state=NORMAL)
    hardWords.config(state=DISABLED)
    cEasy.set(value=0)
    cMedium.set(value=0)

easyWords = Checkbutton(controlsFrame, text="Easy", font=("arial", 10), anchor="w", width=10, command=chooseEasy, variable=cEasy)
easyWords.place(relx=0.10,rely=0.50,anchor=W)

mediumWords = Checkbutton(controlsFrame, text="Medium", font=("arial", 10), anchor="w", width=10, command=chooseMedium, variable=cMedium, state=DISABLED)
mediumWords.place(relx=0.50,rely=0.50,anchor=CENTER)

hardWords = Checkbutton(controlsFrame, text="Hard", font=("arial", 10), anchor="w", width=10, command=chooseHard, variable=cHard)
hardWords.place(relx=0.90,rely=0.50,anchor=E)

startButton = Button(controlsFrame, text="Start", command=startGame, bd=0, font=("arial", 15), width=10)
startButton.place(relx=0.10,rely=0.92,anchor=SW)

resetButton = Button(controlsFrame, text="Reset", command=resetGame, bd=0, font=("arial", 15), width=10)
resetButton.place(relx=0.50,rely=0.92,anchor=S)

def showHelp():
    helpText = """This app/game is made for those who wnat to improve their typing skills.It has a very simple User interface and easy controls.\n\nLet's start with window control.\nClick on top of the title bar (green area) to drag and move window.\nDouble click on title bar to reset it's position.\n\nWords settings.\nPlay with random words: This setting brings some random words according to the slide bar.\nPlay with your words:You can enter your words to practice. You can enter sentences, phrases or anything you like, it's upto you. But only less than 70 words are allowed. Any special characters (like , . / \ [ $ & ...]) are not allowed for now. It will be available in near future. Remember to put some easy and shorter words otherwise it may be difficult for you to type.\nSlider:This slider is used to choose the number of random words you want to practice.\n\nTyping Settings\nFree typing:This mode allows you to type freely without any time limit.\nCheck WPM: You can check WPM (words per minute) by selecting this mode. This mode is only available for random words and not for custom words because user can enter very short words and show off their fake typing skills. For the fair play, Check WPM is only available for random words.\nKeypress sound: AS the title suggests, you can enable or diaable keypress sound.\n\nControls:\nYou can view WPM stats and timer here.\nYou can choose the difficulty level of words you want to practice.\nEasy:You will get words with less than or equal to four characters in this mode.\nMedium:You will get words with less than or equal to eight characters in this mode.\nHard:You will get words with more than eight characters in this mode.\nStart game: You can click on Start button or press Enter key.\nReset game: You can click on Reset button or press Esc key."""
    messagebox.showinfo("Documentation", helpText)

helpButton = Button(controlsFrame, text="Docs", command=showHelp, bd=0, font=("arial", 15), width=10)
helpButton.place(relx=0.90,rely=0.92,anchor=SE)

app.mainloop()
#This much :)