import random
import re


MAX_ERRORS = 8


def play_game():
    all_phrases = import_phrases()
    while True:
        curr_phrases = [random.choice(all_phrases)]
        guessed_letters = []
        errors = 0
        won = False
        display_board(curr_phrases[0], guessed_letters)
        while errors < MAX_ERRORS and not won:
            guess = prompt_guess()
            if guess not in guessed_letters:
                curr_phrases, correct = check_guess(curr_phrases, guess)
                guessed_letters.append(guess)
                if not correct:
                    errors += 1
                    if errors >= MAX_ERRORS:
                        print("Game over!")
                        print(f"The word was: {curr_phrases[0]}")
                        break
            if not display_board(curr_phrases[0], guessed_letters):
                won = True
                print("You win!")


def check_guess(curr_phrases, guess):
    return (curr_phrases, guess in list(curr_phrases[0]))


def display_board(phrase, guessed):
    phrase = phrase.replace('_', ' ')
    wrong_guesses = [letter for letter in guessed if letter not in list(phrase)]
    chars = list(phrase)
    display = []
    missing = False
    for char in chars:
        if char in guessed or re.match('[^A-Za-z]', char):
            display.append(char)
        else:
            missing = True
            display.append('_')
    print(f"{''.join(display)}   Wrong: {''.join(wrong_guesses)}")
    return missing


def prompt_guess():
    guess = ''
    while not guess or len(guess) != 1:
        guess = input("Guess: ")
    return guess


def import_phrases():
    phrases = []
    handle = open("words.txt", "r")
    while line := handle.readline():
        phrases.append(line.strip())
    return phrases


if __name__ == "__main__":
    play_game()
