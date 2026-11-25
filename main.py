#This is a Spyfall in the terminal for Folktale.
#It probably took longer than it needed to and is still kinda finnicky...
#But at least it works**

import random, time, threading

# ANSI CODES - ONLY WORKS IN TERMINAL OR TERMINAL EMULATOR
CURSOR_UP = "\033[1F"
CURSOR_DOWN = "\033[1E"
ERASE_LINE = "\033[2K"

CLEAR_SCREEN = "\033[H\033[J" #didn't really wanna clear the whole thing, but it's the easier way atp
# it only scrolls in Pycharm, but should work correctly on hackclub's "pyterm"

#this doesn't really need a function anymore but i guess we can keep it
def clearLines(count):
    print((CURSOR_UP+ERASE_LINE)*count,end='')

def revealPlayerRole(playerIndexNumber):
    if playerNames[playerIndexNumber] == spy:
        print("You are the spy. Try to pretend to be a regular player and figure out the location without revealing that you are the spy. Guess the location before  the time runs out, or before you get voted out.")
    else:
        print("You are a regular player, ask questions to try to find out who the spy is without revealing the location to them. Form a majority consensus in the group to vote them out before the time runs out, or before they correctly guess the location.")
    input("\nPress Enter to erase this message. Then call the next player. After the last player gets their role, make sure the screen is visible to everyone. You all will be reminded of the gameplay and then prompted to start the stopwatch. After that, hitting enter prompts a confirmation to end the game, REVEALING the spy and location.\n")
    print(CLEAR_SCREEN)
    for _i in range(playerIndexNumber+1): #loop so they can see who already received role in the output after we clear the whole screen
        print(f'Player {_i+1}, "{playerNames[_i]}", has successfully received their role.')

def timer(): #technically a stopwatch
    timeElapsed = 0
    print()
    while not gameEndConfirmation:
        if not activeDialog:
            time.sleep(1)
            timeElapsed += 1
            print(CLEAR_SCREEN)
            print('Hitting enter now will prompt a confirmation to end the game, revealing the spy and the location. ' )
            print(f"{str(int(timeElapsed / 60))}:{timeElapsed % 60}")

            '''
            print(CURSOR_UP + CURSOR_UP + ERASE_LINE, end="") # double cursor up places the timer 2 lines above our input line as to not override the dialog text
            print(f"{str(int(timeElapsed / 60))}:{timeElapsed % 60}"+CURSOR_DOWN) #print function moves cursor on top of our dialog text, so cursor down once, then we move cursor down once more so its on an empty line
            '''
            '''
        else:
            
            print(CURSOR_UP  + ERASE_LINE, end="")
            print(f"{str(int(timeElapsed / 60))}:{timeElapsed%60}")
            '''

def inputListener():
    global gameEndConfirmation, activeDialog, gameEndInput
    while not gameEndConfirmation:
        input()

        activeDialog = True #so that the timer doesn't override our confirmation dialog,
        time.sleep(1)

        print(CLEAR_SCREEN)
        print('STOPWATCH PAUSED')
        gameEndInput = input(activeDialogMessage).lower()

        if gameEndInput == "yes" or gameEndInput == "y":
            gameEndConfirmation = True
            print(gameOverRevealMessage)

        activeDialog = False

# This could probably be improved with some features / different options, but I could also work on this forever and never finish it
locations=['Hospital', 'Cafe', 'Cinema', 'Hotel', 'Factory', 'Restaurant', 'Park', 'School', 'College', 'Grocery Store', 'Power Plant', 'Theatre', 'Stadium', 'Library']
location=random.choice(locations)

print("\nHello and welcome to Spyfall in the terminal.")
playerCount=int(input("How many players are playing?\n"))
print()

playerNames=[]
for i in range(playerCount):
    playerNames.append(input(f"Player {i+1}, enter your name: "))
    print(f'Welcome to Spyfall, "{playerNames[i]}"!')
    print()

spy=random.choice(playerNames)
#
print()
for i in range(len(playerNames)):
    print(f'\nPlayer {i+1}, Type in your name, "{playerNames[i]}", to reveal your role. Ensure no one else can see the screen:')
    nameTypeConfirmation=input("")
    while nameTypeConfirmation!=playerNames[i]:
        clearLines(1)
        nameTypeConfirmation=input(f'Type your name, "{playerNames[i]}": ')
    revealPlayerRole(i)

print("\nGameplay: If a majority agree that a person is the spy, they can agree to vote them out at any time. If they were the spy, players win, if they were not, then the spy wins. At any time, the spy can reveal their role and guess the location. If they guess the location correctly, they win, otherwise, they lose.")
print("Hit enter to start a stopwatch, decide the time control as a group:")
input()

activeDialogMessage="Are you sure you want to end the game? (Y/N) Yes or no?\n"
gameOverRevealMessage = f'The spy was "{spy}", and the location was "{location}".'

#define global variables:
gameEndConfirmation = False
activeDialog = False
gameEndInput=""

# multiple threads = we can listen for user input while updating timer at the same time.
timerThread = threading.Thread(target=timer)
inputListenerThread = threading.Thread(target=inputListener)
timerThread.start()
inputListenerThread.start()
