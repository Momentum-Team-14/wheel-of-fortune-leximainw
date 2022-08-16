from getpass import getpass
import colorama
import evil_ai
import random
import re


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIFFICULTY_PROMPT = True
MAX_ERRORS = 8


def play_game():
    """Main game loop - display the board, prompt the user, and track state."""
    colorama.init()
    all_phrases = import_phrases()
    while True:
        mode = ""
        min_len = 0
        max_len = 999
        if DIFFICULTY_PROMPT:
            difficulty = prompt_difficulty()
            if type(difficulty) is list:
                curr_phrases = difficulty
                max_len = 0
            else:
                mode, min_len, max_len = difficulty
        if max_len:
            curr_phrases = [x for x in all_phrases if min_len <= len(x) <= max_len]
            curr_phrases = [random.choice(curr_phrases)]
            if mode == "evil":
                curr_len = len(curr_phrases[0])
                curr_phrases = [x for x in all_phrases if len(x) == curr_len]
        guessed_letters = []
        guessed_phrases = []
        errors = 0
        won = False
        display_board(curr_phrases[0], guessed_letters, guessed_phrases)
        while errors < MAX_ERRORS and not won:
            guess = prompt_guess()
            if len(guess) == 1:
                if guess not in guessed_letters:
                    if mode == "evil":
                        curr_phrases = evil_ai.matches(format_phrase, curr_phrases, guessed_letters, guess)[0]
                    correct = check_guess(curr_phrases[0], guess)
                    guessed_letters.append(guess)
                    if not correct:
                        errors += 1
                        if errors >= MAX_ERRORS:
                            print(colorama.Fore.RED + "Game over!" + colorama.Style.RESET_ALL)
                            print(f"The word was: {random.choice(curr_phrases)}")
                            break
                else:
                    print(f"You've already guessed {guess}!")
            else:
                if guess not in guessed_phrases:
                    if mode == "evil" and len(curr_phrases) > 1:
                        curr_phrases = [x for x in curr_phrases if x.lower() != guess]
                    if guess.startswith("/"):
                        if guess == "/cheat":
                            if len(curr_phrases) == 1:
                                print(curr_phrases[0])
                            else:
                                best = len(curr_phrases)
                                best_char = "?"
                                for char in ALPHABET.lower():
                                    if char in guessed_letters:
                                        continue
                                    subphrases = evil_ai.matches(format_phrase, curr_phrases, guessed_letters, char)[0]
                                    if len(subphrases) < best:
                                        best = len(subphrases)
                                        best_char = char
                                    print(f"{char}: {len(subphrases)}")
                                print(f"Best choice: {best_char}: {best}")
                        elif guess == "/count":
                            print(len(curr_phrases))
                        elif guess == "/list":
                            print(curr_phrases)
                        else:
                            print(f"unknown command {guess}")
                    elif guess in [x.lower() for x in curr_phrases]:
                        for x in list(guess):
                            guessed_letters.append(x)
                        won = True
                    else:
                        guessed_phrases.append(guess)
                        errors += 1
                else:
                    print(f"You've already guessed {guess}!")
            if not display_board(curr_phrases[0], guessed_letters, guessed_phrases):
                won = True
            else:
                remain = MAX_ERRORS - errors
                print(f"You have {remain} guess{'' if remain == 1 else 'es'} left!")
        if won:
            print(colorama.Fore.GREEN + "You win!" + colorama.Style.RESET_ALL)
        if not str_to_bool(input("Play again? ")):
            return


def check_guess(phrase, guess):
    """Check if the phrase contains the guess."""
    return guess in list(phrase.lower())


def display_board(phrase, guessed, guessed_phrases):
    """Print the current game state."""
    wrong_guesses = [letter for letter in guessed if letter not in list(phrase.lower())]
    display, complete = format_phrase(phrase, guessed)
    print(f"{colorama.Style.BRIGHT + colorama.Fore.WHITE}{display}", end="")
    if len(wrong_guesses) or len(guessed_phrases):
        print(f"   {colorama.Style.DIM + colorama.Fore.WHITE}Wrong: "
            + f"{colorama.Style.NORMAL + colorama.Fore.RED}{''.join(wrong_guesses)}", end="")
    if len(guessed_phrases):
        for guessed_phrase in guessed_phrases:
            print(f"\n   {guessed_phrase}", end="")
    print(colorama.Style.RESET_ALL)
    return not complete


def format_phrase(phrase, guessed):
    """Format the phrase based on what the user has guessed so far."""
    phrase = phrase.replace("_", " ")
    display = []
    complete = True
    for char in list(phrase):
        if char.lower() in guessed or re.match("[^A-Za-z]", char):
            display.append(char)
        else:
            complete = False
            display.append("_")
    return ("".join(display), complete)


def import_phrases():
    """Read in every line as a distinct phrase."""
    phrases = []
    handle = open("words.txt", "r")
    while line := handle.readline():
        phrases.append(line.strip())
    return phrases


def prompt_difficulty():
    """Prompt the user for what difficulty they would like to play at."""
    min_len = 0
    max_len = 999
    print("Do you want to play an easy, normal, or hard round?")
    while True:
        mode = input("Difficulty: ").lower()
        if mode == "any":
            pass
        elif mode == "custom":
            return [getpass("Phrase: ")]
        elif mode == "easy":
            min_len = 4
            max_len = 6
        elif mode == "normal" or mode == "medium":
            min_len = 6
            max_len = 8
        elif mode == "hard":
            min_len = 8
        elif mode == "evil":
            print("Do you want to play an easy, normal, hard, or brutal evil round?")
            while True:
                mode = input("Evilness: ").lower()
                if mode == "any":
                    pass
                elif mode == "easy":
                    min_len = 10
                elif mode == "normal":
                    min_len = 8
                    max_len = 9
                elif mode == "hard":
                    min_len = 6
                    max_len = 7
                    pass
                elif mode == "brutal":
                    max_len = 5
                else:
                    continue
                break
            mode = "evil"
        else:
            continue
        break
    return (mode, min_len, max_len)


def prompt_guess():
    """Prompt the user to guess a letter (or the entire phrase)."""
    guess = ""
    while not guess or (len(guess) == 1 and not re.match("[A-Za-z]", guess)):
        guess = input("Guess: ")
    return guess.lower()


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
