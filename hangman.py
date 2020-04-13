import sys
import random
import linecache
import webbrowser

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#finding all occurences of a word and logging the positions into a list
def find_all(s, c):
    i = s.find(c)
    while i != -1:
        yield i
        i = s.find(c, i + 1)

#english alphabet list with letters
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

#creating the GUI object
class HangManGUI(QWidget): 
    
    def __init__(self):
        super(HangManGUI, self).__init__()

        #variables and GUI object declarations
        self.buttonList = []
        self.lettersFound = []
        self.replacePos = []
        
        self.startButton = QPushButton('Start New Game', self)
        self.wordSearch = QPushButton('', self)
        self.wordSearch.setVisible(False)
        
        self.gameOver = False
        self.gameWin = False
        self.gameStart = False
        
        self.word = ''
        self.lettersToFind = []
        self.lives = 6
        
        #initializing GUI
        self.initUI()

    #drawing the GUI
    def paintEvent(self, event):
        #initial setup
        qp = QPainter()
        qp.begin(gui)
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(QFont('Decorative', 36))

        #drawing the stand
        qp.drawLine(225, 70, 225, 40)
        qp.drawLine(100, 40, 225, 40)
        qp.drawLine(100, 80, 135, 40)
        qp.drawLine(100, 40, 100, 300)

        #drawing letters
        for i in self.replacePos:
            qp.drawText(177 + (70 * i), 290, self.word[i].upper())

        #game changes if player guesses
        if self.gameWin == True:
            #writing the win message
            qp.setFont(QFont('Decorative', 20))
            qp.drawText(300, 180, "Congratulations, you found:")
            #disabling letter buttons
            for i in range (0, 26):
                self.buttonList[i].setEnabled(False)
            #making the word search button visible
            self.wordSearch.setText(self.word.upper())
            self.wordSearch.setVisible(True)
            self.wordSearch.setGeometry(600, 160, 100, 25)
            self.wordSearch.clicked.connect(lambda: self.clicked(1))
            #resetting the variable state for next game
            self.gameWin = False

        #drawing the lines for word length
        if self.word != '':
            for i in range(len(self.word)):
                qp.drawLine(170 + (i * 70), 300, 210 + (i * 70), 300)

        #game changes if player doesn't guess
        if self.gameOver == True:
            #writing the lose message
            qp.setFont(QFont('Decorative', 20))
            qp.drawText(300, 180, "Game over! The word was: ")
            #disabling letter buttons
            for i in range (0, 26):
                self.buttonList[i].setEnabled(False)
            #making the word search button visible
            self.wordSearch.setText(self.word.upper())
            self.wordSearch.setVisible(True)
            self.wordSearch.setGeometry(590, 160, 100, 25)
            self.wordSearch.clicked.connect(lambda: self.clicked(1))
            #resetting the variable state for next game
            self.gameOver = False

        #game changes when player starts a new game
        if self.gameStart == True:
            #getting a word from TXT file and checking its length
            while (1):
                self.word = linecache.getline('words_alpha.txt', random.randint(1,4000))
                self.word = self.word.replace("\n", "")
                self.lettersToFind = set(self.word)
                if len(self.word) > 3 and len(self.word) < 8:
                    break
            #enabling letter buttons
            for i in range (0, 26):
                self.buttonList[i].setEnabled(True)
            #drawing letters lines
            for i in range(len(self.word)):
                qp.drawLine(170 + (i * 70), 300, 210 + (i * 70), 300)
            #resetting the variable state
            self.gameStart = False

        #conditions for drawing each part of the hangman
        if (self.lives < 6):
            qp.drawEllipse(205, 70, 40, 40)

        if (self.lives < 5):
            qp.drawLine(225, 110, 225, 185)

        if (self.lives < 4):
            qp.drawLine(190, 115, 225, 140)

        if (self.lives < 3):
            qp.drawLine(260, 115, 225, 140)

        if (self.lives < 2):
            qp.drawLine(195, 225, 225, 188)

        if (self.lives < 1):
            qp.drawLine(255, 225, 225, 188)

        qp.end()

    #generating the UI
    def initUI(self):
        #generating the letter buttons
        self.generateLetterButtons()
        
        self.startButton.setGeometry(350, 70, 300, 35)
        self.startButton.clicked.connect(lambda: self.resetGame(1))

        #window setup
        self.setGeometry(100, 100, 750, 400)
        self.setWindowTitle('HangMan')
        self.show()

    #opening browser tab to search for word online
    def clicked(self, num):
        url = 'https://dictionary.cambridge.org/dictionary/english/' + str(self.word)
        webbrowser.open(url, new=2)

    #resetting game variables before a new word generation   
    def resetGame(self, num):
        self.lettersToFind = []
        self.lettersFound = []
        self.replacePos = []
        self.word = ''

        self.gameStart = True
        self.gameOver = False
        self.gameWin = False
        
        self.lives = 6
        self.wordSearch.setVisible(False)
        #UPDATE THE GAME STATE!
        self.update()

    #update game state when a letter is pressed
    def updateGame(self, num):
        letter = chr(97 + num)
        if letter not in self.word:
            self.lives -= 1
        else:
            self.replacePos += list(find_all(self.word, letter))
            self.lettersFound += letter

        #lose conditions
        if self.lives == 0:
            self.gameOver = True
        if self.lettersToFind == set(self.lettersFound):
            self.gameWin = True
        #print(self.word)

    #acitons when button clicked
    def buttonClick(self, num):
        self.buttonList[num].setEnabled(False)
        self.updateGame(num)
        self.update()

    #generating letter buttons in the bottom
    def generateLetterButtons(self):

        for num in range (0, 26):
            self.buttonList.append(QPushButton(alphabet[num], self))
            self.buttonList[num].move(10 + 81*(num%9), 320 + (20 * (num // 9)))
            self.buttonList[num].setEnabled(False)

        #these connections don't seem to work in the for loop
        self.buttonList[0].clicked.connect(lambda: self.buttonClick(0))
        self.buttonList[1].clicked.connect(lambda: self.buttonClick(1))
        self.buttonList[2].clicked.connect(lambda: self.buttonClick(2))
        self.buttonList[3].clicked.connect(lambda: self.buttonClick(3))
        self.buttonList[4].clicked.connect(lambda: self.buttonClick(4))
        self.buttonList[5].clicked.connect(lambda: self.buttonClick(5))
        self.buttonList[6].clicked.connect(lambda: self.buttonClick(6))
        self.buttonList[7].clicked.connect(lambda: self.buttonClick(7))
        self.buttonList[8].clicked.connect(lambda: self.buttonClick(8))
        self.buttonList[9].clicked.connect(lambda: self.buttonClick(9))
        self.buttonList[10].clicked.connect(lambda: self.buttonClick(10))
        self.buttonList[11].clicked.connect(lambda: self.buttonClick(11))
        self.buttonList[12].clicked.connect(lambda: self.buttonClick(12))
        self.buttonList[13].clicked.connect(lambda: self.buttonClick(13))
        self.buttonList[14].clicked.connect(lambda: self.buttonClick(14))
        self.buttonList[15].clicked.connect(lambda: self.buttonClick(15))
        self.buttonList[16].clicked.connect(lambda: self.buttonClick(16))
        self.buttonList[17].clicked.connect(lambda: self.buttonClick(17))
        self.buttonList[18].clicked.connect(lambda: self.buttonClick(18))
        self.buttonList[19].clicked.connect(lambda: self.buttonClick(19))
        self.buttonList[20].clicked.connect(lambda: self.buttonClick(20))
        self.buttonList[21].clicked.connect(lambda: self.buttonClick(21))
        self.buttonList[22].clicked.connect(lambda: self.buttonClick(22))
        self.buttonList[23].clicked.connect(lambda: self.buttonClick(23))
        self.buttonList[24].clicked.connect(lambda: self.buttonClick(24))
        self.buttonList[25].clicked.connect(lambda: self.buttonClick(25))

#initializing GUI instance and creating the game object        
app = QApplication(sys.argv)
gui = HangManGUI()
sys.exit(app.exec_())

