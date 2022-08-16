DEFAULT_DEPTH = 3


def matches(format, curr_phrases, guesses_left, guessed, guess=None,
            depth=DEFAULT_DEPTH, alpha=float("-inf"), beta=float("inf"),
            transpositions=None):
    """matches() - evaluate the game state using minimax."""
    """Find the best possible outcome, and return it and its score."""

    # create a new transposition table if none exists
    if transpositions == None:
        transpositions = {}

    # merge all the letters that the user will have guessed after this guess
    guesses = guessed[:]
    if guess != None:
        guesses.append(guess)

    # out of depth, or node is a leaf!
    # evaluate the current node and return
    if depth <= 0 or guesses_left <= 0 or len(curr_phrases) == 1:
        return evaluate(curr_phrases, guesses, guesses_left)

    # create the key for the current game state
    key = (format(curr_phrases[0], guessed)[0], frozenset(guesses), depth, guess == None)

    # if the key is in the transposition table, return immediately
    if key in transpositions:
        return transpositions[key]

    # if there's no current guess, match based on player behavior
    if guess == None:
        result = matches_player(format, curr_phrases, guesses_left, guessed,
                                depth, alpha, beta, transpositions)

    # otherwise, match based on AI behavior
    else:
        result = matches_ai(format, curr_phrases, guesses_left, guesses,
                            guess, depth, alpha, beta, transpositions)

    transpositions[key] = result
    return result


def matches_ai(format, curr_phrases, guesses_left, guesses, guess, depth, alpha, beta, transpositions):
    categories = categorize(format, curr_phrases, guesses)
    best = []
    best_score = 0
    for _, value in categories.items():
        inner_guesses_left = guesses_left
        if guess not in list(value[0]):
            inner_guesses_left -= 1
        _, score = matches(format, value, inner_guesses_left, guesses, depth=depth, alpha=alpha, beta=beta, transpositions=transpositions)
        # depth reward
        score += 1
        # max - evil match wants the best score
        if not len(best) or score > best_score:
            best_score = score
            best = value
        if score >= beta:   # beta cutoff
            break
        alpha = max(alpha, score)
    return (best, best_score)


def matches_player(format, curr_phrases, guesses_left, guessed, depth, alpha, beta, transpositions):
    test_guesses = [x for x in "etaoinshrdlcumwfgypbvkjxqz" if x not in guessed]
    best = []
    best_score = float("inf")
    for guess in test_guesses:
        results, score = matches(format, curr_phrases, guesses_left, guessed, guess, depth=depth-1, alpha=alpha, beta=beta, transpositions=transpositions)
        # min - player wants the worst score
        if not len(best) or score < best_score:
            best_score = score
            best = results
        if score <= alpha:   # alpha cutoff
            break
        beta = min(beta, score)
    return (best, best_score)


def categorize(format, phrases, guesses):
    """Categorize phrases based on what information they reveal for the current guesses."""
    categories = {}
    for phrase in phrases:
        display, _ = format(phrase, guesses)
        if display not in categories:
            categories[display] = []
        categories[display].append(phrase)
    return categories


def evaluate(phrases, guess, tries):
    if tries == 0:
        value = (phrases, 16777216)
    elif len(phrases) == 1:
        if guess in list(phrases[0]):
            value = (phrases, -16777216)
        else:
            value = (phrases, 1 / tries)
    else:
        value = (phrases, len(phrases) / tries)
    #print(value)
    return value
