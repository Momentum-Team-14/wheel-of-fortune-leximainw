DEFAULT_DEPTH = 3


def matches(format, curr_phrases, guessed, guess=None, depth=DEFAULT_DEPTH,
            alpha=float("-inf"), beta=float("inf"), transpositions=None):
    if depth <= 0:
        if len(curr_phrases) == 1:
            return (curr_phrases, float("-inf"))
        return (curr_phrases, len(curr_phrases))
    if transpositions == None:
        transpositions = {}
    guesses = guessed[:]
    if guess != None:
        guesses.append(guess)
    key = (format(curr_phrases[0], guessed)[0], frozenset(guesses), depth, guess == None)
    if key in transpositions:
        return transpositions[key]
    if guess == None:
        test_guesses = [x for x in "etaoinshrdlcumwfgypbvkjxqz" if x not in guessed]
        best = []
        best_score = float("inf")
        for guess in test_guesses:
            results, score = matches(format, curr_phrases, guessed, guess, depth=depth, alpha=alpha, beta=beta, transpositions=transpositions)
            # min - player wants the worst score
            if not len(best) or score < best_score:
                best_score = score
                best = results
            if score <= alpha:   # alpha cutoff
                break
            beta = min(beta, score)
        transpositions[key] = (best, best_score)
        return (best, best_score)
    else:
        categories = categorize(curr_phrases)
        best = []
        best_score = 0
        for _, value in categories.items():
            results = []
            curr_depth = depth
            while not len(results):
                curr_depth -= 1
                results, score = matches(format, value, guesses, depth=curr_depth, alpha=alpha, beta=beta, transpositions=transpositions)
            if guess not in list(results[0]):
                score += len(value) * 1.07
            # max - evil match wants the best score
            if not len(best) or score > best_score:
                best_score = score
                best = value
            if score >= beta:   # beta cutoff
                break
            alpha = max(alpha, score)
        transpositions[key] = (best, best_score)
        return (best, best_score)


def categorize(phrases, guesses):
    """Categorize phrases based on what information they reveal for the current guesses."""
    categories = {}
    for phrase in phrases:
        display, _ = format(phrase, guesses)
        if display not in categories:
            categories[display] = []
        categories[display].append(phrase)
    return categories
