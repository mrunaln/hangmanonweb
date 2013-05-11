#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import string
import random


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)
wordlist = ""
secretWord = ""
WORDLIST_FILENAME = "words.txt"

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_front(self, template):
        self.render(template)
        


class MainHandler(Handler):
    def get(self):
        """Initialize loadWords()"""
        global WORDLIST_FILENAME
        global wordlist
        inFile = open(WORDLIST_FILENAME, 'r', 0)
        line = inFile.readline()
        wordlist = string.split(line)
        #return wordlist
        self.render_front("index.html")

class ProcessInputHandler(Handler):
    def get(self):
        pass
    
    def post(self):
        pass
    
    
class InitializeGameHandler(Handler):
    def get(self):
        """
        Check request parameters
        Send response "Welcome to Hangman"
        
        secretWord = chooseWord(wordlist).lower()
        hangman(secretWord)
        """
        global secretWord
        secretWord = random.choice(wordlist)
        
    
    def post(self):
        pass    

app = webapp2.WSGIApplication([('/home', MainHandler),
                               ('/input', ProcessInputHandler),
                               ('/initialize', InitializeGameHandler)],
                              debug=True)



#Hangman Code
def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    count = 0
    for d in lettersGuessed:
        if secretWord.find(d) != -1:
            count += 1
    if count == len(secretWord):
        return True
    else:
        return False


def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    arr = list(secretWord)
    ans = []
    l = len(secretWord)
    while l > 0:
     ans.append('_ ')
     l -= 1 
    idx = -1
    for d in arr:
        if d in lettersGuessed:
            idx = arr.index(d)
            arr[idx] = '-1'
            ans[idx] = d
    
    return ''.join(ans)



def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    guessed = list(lettersGuessed)
    allletters = list(string.ascii_lowercase)
    
    filtered = []
    for c in allletters:
        if c not in guessed:
            filtered.append(c)
    return ''.join(filtered)

    

def hangman(secretWord):
    print "I am thinking of a word that is " + str(len(secretWord)) + " letters long."
    mistakesMade = 0
    guesses = 8
    lettersGuessed = ""
    returnedValues = []

    previousValue = ""
    currentValue = ""
    
    while( mistakesMade < guesses ):
        print "-------------"
        print "You have " + str(guesses - mistakesMade) + " guesses left."
        availableLetters = getAvailableLetters(lettersGuessed)
        print "Available Letters: " + availableLetters
        guess = raw_input("Please guess a letter: ")
        guessInLowerCase = guess.lower()
        if guessInLowerCase not in lettersGuessed:
            lettersGuessed += guessInLowerCase
        if guessInLowerCase not in availableLetters:
            print "Oops! You've already guessed that letter: " + currentValue
        else:
            currentValue = getGuessedWord(secretWord, lettersGuessed)
            if currentValue == previousValue:
                if guessInLowerCase not in lettersGuessed:
                    lettersGuessed += guessInLowerCase
                print "Oops! That letter is not in my word: " + previousValue
                mistakesMade += 1
            else:
                previousValue = currentValue
                if mistakesMade == 0:
                    firstCheck = ""
                    for i in range(0, len(secretWord)):
                        firstCheck += "_ "
                    if currentValue == firstCheck:
                        #if guessInLowerCase not in lettersGuessed:
                        #    lettersGuessed += guessInLowerCase
                        print "Oops! That letter is not in my word: " + currentValue
                        mistakesMade += 1
                    else:
                        print "Good guess: " + currentValue
                        # add code to make change in lettersGuessed when multiple entries are present
                        
                        count = secretWord.count(guessInLowerCase)
                        count -= 1 # bcuz once upar ho chuka hai
                        while count:
                            lettersGuessed += guessInLowerCase
                            count -= 1
                        #print lettersGuessed
                        
                else:
                    print "Good guess: " + currentValue
                    # add code to make change in lettersGuessed when multiple entries are present
                    
                    count = secretWord.count(guessInLowerCase)
                    count -= 1 # bcuz once upar ho chuka hai
                    while count:
                            lettersGuessed += guessInLowerCase
                            count -= 1
                    #print lettersGuessed
                    
        #print "Letters Guessed: " + lettersGuessed
        if isWordGuessed(secretWord, lettersGuessed):
            print "Congratulations, you won!"
            break

    if mistakesMade == guesses:
        print "Sorry, you ran out of guesses. The word was "  + secretWord + "."
