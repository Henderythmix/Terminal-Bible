import json, requests
import os

os.system("clear")
print("Welcome to Terminal Bible\n\n")

book = ""
chapter = ""
readingverse = False

help = """usage: [command] {params}

help                          - Shows this screen
exit                          - Exits the program
clear                         - Clears the screen
read {book} {chapter}         - Loads the book and chapter to read
hightlight/hl {verse} {color} - Highlights the verse in a terminal color*
clean {book} {chapter}        - Cleans all highlighting in the requested chapter (use this if you can not load your requested chapter properly)

*The color can be any number from 0-7 (0 being remove highlighting). Please use the a reference on the internet for terminal colors
"""

### FUNCTIONS ###

# More Aesthetic Purposes, converts numbers into superscript
def superscriptNumber(number):
    stringmode = str(number)
    vconvert = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    v = ""
    for n in range(len(stringmode)):
            v += vconvert[int(stringmode[n])]

    return v

# Loads The bible based on the book and chapter
def LoadBible(b, c):
    os.system("clear")
    storydata = requests.get(f"https://bible-api.com/{b}{c}?translation=kjv")
    story = json.loads(storydata.text)
    
    global readingverse

    if storydata.ok:
        readingverse = True
        try:
            notes = open(f"{b.lower()}{c}.txt", "r")
        except:
            InitChapterData(b, c)
            notes = open(f"{b.lower()}{c}.txt", "r")

    
        notedata = notes.read()

        print(f"\x1b[01m{book.upper()} {chapter} - KJV\x1b[00m\n")

        for i in story["verses"]:
            if notedata[i["verse"]-1] == "0":
                print(f"{superscriptNumber(i['verse'])}{i['text']}")
            else:
                print(f"\x1b[4{notedata[i['verse']-1]}m\x1b[30m{superscriptNumber(i['verse'])}{i['text']}\x1b[0m")

        notes.close()
    else:
        readingverse = False
        print("ERROR: Page Does not Exist")

# Initialize Highlighting Data
def InitChapterData(b, c):
    f = open(f"{b.lower()}{c}.txt", "w")
    storydata = requests.get(f"https://bible-api.com/{b}{c}?translation=kjv")
    story = json.loads(storydata.text)

    f.write("0"*len(story["verses"]))
    f.close()

# Highlighting
def Highlight(b, ch, v, col):
    f = open(f"{b.lower()}{ch}.txt", "r")
    lines = list(f.read())
    f.close()

    lines[int(v)-1] = col

    f = open(f"{b.lower()}{ch}.txt", "w")
    f.write("".join(lines))
    f.close()

### MAIN LOOP ###
while True:
    action = input("> ")
    keys = action.split()

    if keys[0] == "read":
        if len(keys) == 3:
            book = keys[1]
            chapter = keys[2]
            LoadBible(book, chapter)
        else:
            print("please follow the command arguments properly")
    elif keys[0] == "clean":
        if len(keys) == 3:
            InitChapterData(keys[1], keys[2])
            print(f"Highlighting of {keys[1].upper()} {keys[2]} has been cleaned successfully")
    elif keys[0] == "highlight" or keys[0] == "hl":
        if readingverse == True:
            if len(keys) == 3:
                Highlight(book, chapter, keys[1], keys[2])
                LoadBible(book, chapter)
        else:
            print("Please make sure you're reading a chapter first before using this command")
    elif action == "exit":
        break
    elif action == "help":
        print(help)
    elif action == "clear":
        os.system("clear")
    else:
        print("Invalid command. Type \"help\" for a list of commands")
