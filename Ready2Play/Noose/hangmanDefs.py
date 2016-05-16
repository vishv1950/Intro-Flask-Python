from flask import request, render_template
from random import randint
import string 
from Noose import hangman

@hangman.route("/hangman",methods=["GET"])
def startHangman():
    """Start the game of hangman directly or through key New."""
    
    secrets =["BHARAT", "ENGLAND", "INDIA", "PAKISTAN", "NEPAL", "BHUTAN", "UN",
              "FRANCE", "CHINA"]
    secretWord = secrets[randint(0,len(secrets)-1)]

    guesses = ""
    penalty = 0

    win, secret = show_guessed_part_of_secret(secretWord, guesses)
    feedback = "YOUR GAME IS LOST"[:penalty]

    return render_template("hangman.html", secret=secret,
                           guesses=guesses, secretWord=secretWord,
                           feedback=feedback)
    

def show_guessed_part_of_secret(secretWord, guesses):
    """Transforms secretWord string into a string for showing correct guesses.

    Correctly guessed letters are shown. Other are shown as _.
    Spaces are used to make the display easy to read."""

    lst = []
    win = True
    
    for l in reversed(secretWord):
        if l in guesses:
            lst.insert(0,l)
        else:
            lst.insert(0,"_")
            win = False
            
    rslt = (win, " ".join(lst))

    return rslt
            
            
@hangman.route("/hangman", methods=["POST"])
def continueHangman():
    """Plays one step in an continuing game of hangman."""

    letter = request.form["letter"]
    if letter=="New":
        return startHangman()

    penalty = len(request.form["feedback"])
    pastGuesses = request.form["guesses"]
    secretWord = request.form["secretWord"]
    
    guesses = pastGuesses+letter

    if letter in secretWord:
        pass
    else:
        if letter in "ABEIMNOPRSTU":
            penalty += 2
        else:
            penalty += 1

    win, secret = show_guessed_part_of_secret(secretWord, guesses)
    if win:
        feedback = "YOU WON THE GAME"
        guesses = string.ascii_uppercase
    elif penalty < 17:
        feedback = "YOUR GAME IS LOST"[:penalty]
    else:
        feedback = "YOUR GAME IS LOST"
        guesses = string.ascii_uppercase

    return render_template("hangman.html", secret=secret,
                           guesses=guesses, secretWord=secretWord,
                           feedback=feedback)

