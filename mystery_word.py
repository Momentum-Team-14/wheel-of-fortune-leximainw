import random


def play_game():
    all_phrases = import_phrases()
    while True:
        curr_phrases = [random.choice(all_phrases)]
        print(curr_phrases[0])


def import_phrases():
    phrases = []
    handle = open("words.txt", "r")
    while line := handle.readline():
        phrases.append(line.strip())
    return phrases


if __name__ == "__main__":
    play_game()
