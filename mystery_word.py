import random
import re


DIFFICULTY_PROMPT = True
MAX_ERRORS = 8


def play_game():
    all_phrases = import_phrases()
    while True:
        if DIFFICULTY_PROMPT:
            print("Do you want to play an easy, normal, or hard round?")
            while True:
                mode = input("Difficulty: ").lower()
                if mode == "any" or mode == "evil":
                    f = lambda _: True
                elif mode == "easy":
                    f = lambda x: 4 <= len(x) <= 6
                elif mode == "normal" or mode == "medium":
                    f = lambda x: 6 <= len(x) <= 8
                elif mode == "hard":
                    f = lambda x: len(x) >= 8
                else:
                    continue
                break
        else:
            f = lambda _: True
        curr_phrases = [x for x in all_phrases if f(x)]
        curr_phrases = [random.choice(curr_phrases)]
        if mode == "evil":
            curr_len = len(curr_phrases[0])
            curr_phrases = [x for x in all_phrases if len(x) == curr_len]
        guessed_letters = []
        errors = 0
        won = False
        display_board(curr_phrases[0], guessed_letters)
        while errors < MAX_ERRORS and not won:
            guess = prompt_guess()
            if guess not in guessed_letters:
                if mode == "evil":
                    curr_phrases = evil_matches(curr_phrases, guessed_letters, guess)
                correct = check_guess(curr_phrases[0], guess)
                guessed_letters.append(guess)
                if not correct:
                    errors += 1
                    if errors >= MAX_ERRORS:
                        print("Game over!")
                        print(f"The word was: {curr_phrases[0]}")
                        break
            else:
                print(f"You've already guessed {guess}!")
            if not display_board(curr_phrases[0], guessed_letters):
                won = True
                print("You win!")
            else:
                remain = MAX_ERRORS - errors
                print(f"You have {remain} guess{'' if remain == 1 else 'es'} left!")
        if not str_to_bool(input("Play again? ")):
            return


def check_guess(phrase, guess):
    return guess in list(phrase)


def display_board(phrase, guessed):
    wrong_guesses = [letter for letter in guessed if letter not in list(phrase)]
    display, complete = format_phrase(phrase, guessed)
    print(f"{display}   Wrong: {''.join(wrong_guesses)}")
    return not complete


def evil_matches(curr_phrases, guessed, guess):
    categories = {}
    guesses = guessed[:]
    guesses.append(guess)
    for phrase in curr_phrases:
        display, _ = format_phrase(phrase, guesses)
        if display not in categories:
            categories[display] = []
        categories[display].append(phrase)
    return max(categories.items(), key=lambda x: len(x[1]) + (0 if guess in list(x[1][0]) else 1))[1]


def format_phrase(phrase, guessed):
    phrase = phrase.replace("_", " ")
    display = []
    complete = True
    for char in list(phrase):
        if char in guessed or re.match("[^A-Za-z]", char):
            display.append(char)
        else:
            complete = False
            display.append("_")
    return ("".join(display), complete)


def prompt_guess():
    guess = ""
    while not guess or len(guess) != 1:
        guess = input("Guess: ")
    return guess


def import_phrases():
    phrases = []
    handle = open("words.txt", "r")
    while line := handle.readline():
        phrases.append(line.strip())
    return phrases


def str_to_bool(str):
    """Tries to convert a string to an appropriate boolean."""
    """["1", "True", "Yes", "true", "yes"] all yield True."""
    """["0", "False", "No", "false", "no"] all yield False."""
    """Other strings may yield unexpected results."""
    if len(str) == 0:
        return False
    return [
        False, True, True, False,
        True, False, False, True
    ][ord(str[0]) % 8]


if __name__ == "__main__":
    play_game()
