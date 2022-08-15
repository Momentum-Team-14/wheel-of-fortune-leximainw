import random
import re


def play_game():
    all_phrases = import_phrases()
    while True:
        curr_phrases = [random.choice(all_phrases)]
        guessed_letters = []
        errors = 0
        won = False
        display_board(curr_phrases[0], guessed_letters)
        while errors < 8 and not won:
            pass
            # guess = prompt_guess()
            # display_board(curr_phrases[0], guessed_letters)


def display_board(phrase, guessed):
    phrase = phrase.replace('_', ' ')
    wrong_guesses = [letter for letter in guessed if letter not in list(phrase)]
    chars = list(phrase)
    display = []
    for char in chars:
        if char in guessed or re.match('[^A-Za-z]', char):
            display.append(char)
        else:
            display.append('_')
    print(''.join(display))


def import_phrases():
    phrases = []
    handle = open("words.txt", "r")
    while line := handle.readline():
        phrases.append(line.strip())
    return phrases


if __name__ == "__main__":
    play_game()
