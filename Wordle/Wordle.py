#First Python Project

import random
import sys

import nltk

from termcolor import colored

nltk.download('words')
from nltk.corpus import words


#Function that contains menu and instructions for the game
def print_menu():
    print("Let's Play Wordle!!!")
    print("Type a 5 letter word and hit enter!\n")


nltk.data.path.append("/work/words")
word_list = words.words()
words_five = {word for word in word_list if len(word) == 5}


def read_random_word():
    with open("words.txt") as f:
        words = f.read().splitlines()
    return random.choice(words).lower()


# Function to get a random 5-letter word (choose one method)
#def get_random_word():
# Option 1: Using NLTK
#return random.choice(words_five)

print_menu()
play_again = ""

while play_again != "q":

    #Test statement
    #print(word)
    word = read_random_word()

    for attempt in range(1, 7):

        #sets guess variable to input as well as converts all characters into lower case with the .lower() tag
        guess = input().lower()
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')

        #sets the range to be the anything between what the guess is and 5 
        for i in range(min(len(guess), 5)):

            #IF LETTER AND LOCATION ARE BOTH CORRECT
            #if the correct letter is in the correct spot then that letter will be printed green with the .colored(variable,color) tag
            if guess[i] == word[i]:

                print(colored(guess[i], 'black', 'on_green'), end="")

            #IF LETTER IS CORRECT BUT LOCATION IS NOT
            elif guess[i] in word:

                print(colored(guess[i], 'black', 'on_yellow'), end="")

            #IF LETTER IS WRONG
            else:

                print(guess[i], end="")

        print()

        #IF ANSWER IS CORRECT
        if guess == word:

            # prints final message if word is correct with the amount of attempts using the f string method with 'f'
            # at the beginning and {i} where the variable will be placed
            print(colored(f"YOU WON IN {attempt} GUESSES!\n", 'magenta'), end="")
            break

        elif attempt == 6:
            print(f"Sorry the word was {word}")

    play_again = input("Whould you like to play again? Type anything to continue, If not type q to exit")
