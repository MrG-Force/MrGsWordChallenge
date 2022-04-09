# THIS IS MR. G'S WORDS CHALLENGE GAME 1.0
import random
from time import sleep
from check_drae_with_beautifulsoup import check_drae

SCRABBLE_LETTER_VALUES_EN = {
	'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
	'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
SCRABBLE_LETTER_VALUES_SP = {
	'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'l': 1, 'm': 3,
	'n': 1, 'ñ': 8, 'o': 1, 'p': 3, 'q': 5, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'x': 8, 'y': 4,
	'z': 10, '_': 0
}

LETTER_BAG_EN = {
	'a': 9, 'b': 2, 'c': 2, 'd': 4, 'e': 12, 'f': 2, 'g': 3, 'h': 2, 'i': 9, 'j': 1, 'k': 1, 'l': 4, 'm': 2,
	'n': 6, 'o': 8, 'p': 2, 'q': 1, 'r': 6, 's': 4, 't': 6, 'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 1, 'z': 1,
	'_': 2
}
LETTER_BAG_SP = {
	'a': 12, 'b': 2, 'c': 5, 'd': 5, 'e': 12, 'f': 1, 'g': 2, 'h': 3, 'i': 6, 'j': 1, 'l': 5, 'm': 2,
	'n': 5, 'ñ': 1, 'o': 9, 'p': 2, 'q': 1, 'r': 5, 's': 6, 't': 4, 'u': 5, 'v': 1, 'x': 1, 'y': 1,
	'z': 1, '_': 2
}

WORDS_FILE_EN = "words.txt"
WORDS_FILE_SP = "palabras.txt"


def loadWords(lan):
	"""
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    lan: a single letter string (s for Spanish, e for English)
    """
	global inFile
	if lan == "e":
		inFile = open(WORDS_FILE_EN, 'r')
	# wordList: list of strings
	elif lan == "s":
		inFile = open(WORDS_FILE_SP, 'r')
	wordList = []
	print("Loading word list from file...")
	for line in inFile:
		wordList.append(line.strip().lower())
	print("  ", len(wordList), "words loaded.")
	print()
	return wordList


def update_words_list_file(word, words_list, file_name):
	""""""
	with open(file_name, 'w') as file_handle:
		for list_item in words_list:
			if list_item != word:
				file_handle.write('%s\n' % list_item)
	print(f'"{word}" has been removed from my vocabulary')


def greetings(func):
	def wrapper(*args, **kwargs):
		print()
		print("Welcome to Mr. G's Words Challenge.")
		print()
		func(*args, **kwargs)
		print()
		print("Thanks for playing")

	return wrapper


def set_language():
	while True:
		print("To play with a dictionary in Spanish enter S, for English enter E", end=": ")
		lan = input()
		if lan.lower() == "s":
			print()
			return "s"
		elif lan.lower() == "e":
			print()
			return "e"
		else:
			print("Invalid command, please try again.")
			print()


def get_hand_size():
	"""
    Does not take any argument. Asks for input from the user to define
    the size of the hand (number of letters) for the game.
    Returns: 5 <= int <=20
    """
	default = 7
	while True:
		print("The default number of letters per hand is 7, do you want to change it? ", end="Y/N")
		ch_hand_size = input(": ")
		print()
		if ch_hand_size.lower() == "y":
			while True:
				try:
					hand_size = int(input("Enter a new size as a number between 5 and 20: "))
					if 5 <= hand_size <= 20:
						return hand_size
					else:
						print("Must be a number >= 5 and <= 20. Please try again.")
				except ValueError:
					print("That is not a number. Please try again.")
					print()
		elif ch_hand_size.lower() == "n":
			return default
		else:
			print("It's a 'Y' or 'N' question, please try again.")


def get_letter_bag(lan):
	"""
    Args:
        lan: a single letter "e" for English, "s" for Spanish
    Returns:
        A list with all the letters(tiles) in the given language available to play
    """
	bag_list = []
	if lan == "e":
		for key in LETTER_BAG_EN:
			for i in range(LETTER_BAG_EN.get(key)):
				bag_list.append(key)
	elif lan == "s":
		for key in LETTER_BAG_SP:
			for i in range(LETTER_BAG_SP.get(key)):
				bag_list.append(key)
	print('Available letters in the bag:', len(bag_list))
	print()
	return bag_list


def deal_hand_user(n):
	"""
        Returns a random hand(list) containing n lowercase letters.
        Takes the letters from a list(bag_list) representing a bag
        of available letters and updates the list subtracting
        the letters dealt.
        Hands are represented as lists.

        n: int >= 0
        returns: list (strings --> letters)
        """
	hand = []
	if n <= len(bag_list):
		for i in range(n):
			letter = bag_list.pop(random.randrange(0, len(bag_list)))
			hand.append(letter)
		return hand
	else:
		for letter in bag_list:
			hand.append(letter)
		bag_list.clear()
		print("You took the last available letters in the bag.")
		return hand


def deal_hand_mr_g(n):
	"""
        Returns a random hand(list) containing n lowercase letters.
        Takes the letters from a list(bag_list) representing a bag
        of available letters and updates the list subtracting
        the letters dealt.
        Hands are represented as lists.

        n: int >= 0
        returns: list (strings --> letters)
        """
	hand = []
	if n <= len(bag_list):
		for i in range(n):
			letter = bag_list.pop(random.randrange(0, len(bag_list)))
			hand.append(letter)
		return hand
	else:
		for letter in bag_list:
			hand.append(letter)
		bag_list.clear()
		print(
			"Mr. G took the last available letters in the bag.")  # check this code prints even when bag lis was already emptied
		return hand


def isValidDiscard(letters, hand):
	"""
        Returns True if all letters are in the hand.
        And the length of letters is not bigger than the
        hand.
        Otherwise, returns False.

        Does not mutate hand or wordList.

        letters: string of letters to be discarded
        hand: list (string -> letters)

        """
	for letter in letters:
		if letters.count(letter) <= hand.count(letter):
			pass
		else:
			return False
	return len(letters) < len(hand)


def updateHand(hand, word):
	"""
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it.

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
	updated_hand = hand.copy()
	for letter in word:
		updated_hand.remove(letter)
	return updated_hand


def getWordScore(word, n, lan):
	"""
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES).

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
	score = 0
	bonus = 0
	if len(word) == n:
		bonus = 1
	for letter in word:
		if lan == "e":
			score += SCRABBLE_LETTER_VALUES_EN.get(letter)
		elif lan == "s":
			score += SCRABBLE_LETTER_VALUES_SP.get(letter)
	if bonus:
		return (score * n) + 50
	else:
		return score * len(word)


def isValidWord(word, hand, wordList):
	"""
    Returns:
        True: if word is in the wordList and is entirely composed of letters in the hand.
        Returns False otherwise.
        or
        string: if a wildcard '_' was played in the word

    Does not mutate hand or wordList.

    word: string
    hand: list (string -> letters)
    wordList: list of valid lowercase strings
    """
	for letter in word:
		if word.count(letter) > hand.count(letter):
			return False
	# Is there a wildcard in user's input?
	if '_' in word:
		while True:
			wildcard = input("Enter the value for '_' as a single letter: ")
			if len(wildcard) == 1 and wildcard.isalpha() and wildcard.islower():
				print()
				break
			else:
				print('Invalid input. Please try again')
				print()
		if word.replace("_", wildcard) in wordList:
			return word.replace("_", wildcard)
		else:
			return False
	else:
		return word in wordList


def isValidWord_MrG(word, hand, wordList):
	"""
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.

    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
	for letter in word:
		count = word.count(letter)
		if count <= hand.count(letter):
			pass
		else:
			return False
	return word in wordList


def displayHand(hand):
	"""
    Displays the letters currently in the hand.

    For example:
    >> displayHand(['d', 'v', 'e', 'a', 't', 'h', 'm'])
    Should print out something like:
       d  v  e  a  t  h  m
    The order of the letters is unimportant.

    hand: list (strings --> letters)
    """
	for letter in hand:
		print(letter, end="  ")  # print all on the same line
	print()  # print an empty line


def mr_g_choose_word(hand, wordList, n):
	"""
    Given a hand and a wordList, find the word that gives
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)

    returns: string or None
    """
	# Create a new variable to store the maximum score seen so far (initially 0)
	bestScore = 0
	# Create a new variable to store the best word seen so far (initially None)
	bestWord = None
	# For each word in the wordList
	for word in wordList:
		# If you can construct the word from your hand
		if isValidWord_MrG(word, hand, wordList):
			# find out how much making that word is worth
			score = getWordScore(word, n, lan)
			# If the score for that word is higher than your best score
			if score > bestScore:
				# update your best score, and best word accordingly
				bestScore = score
				bestWord = word
	# return the best word you found.
	return bestWord


def mr_g_choose_letter_if_wildcard(hand, wordList, n, lan):  # TO DO: fix docstring comment code
	"""
    Chooses a single letter to replace the underscore and chooses a valid word
    :param lan:
    :param hand: a list with n - 1 letters and an underscore
    :param wordList: a list of valid words
    :param n: the length of the hand
    :return: a valid wordword and the best letter to replace the underscore
    """
	# Create a variable to store the letter that gives the maximum score so far
	best_letter = str
	# Create a new variable to store the best word seen so far (initially None)
	bestWord = None
	# Create a new variable to store the maximum score seen so far (initially 0)
	bestScore = 0
	# For each letter in the game if spanish is the language
	bestHand = []
	if lan == "s":
		for letter in LETTER_BAG_SP.keys():
			hand = list("".join(hand).replace('_', letter))
			word = mr_g_choose_word(hand, wordList, n)
			score = getWordScore(word, n, lan)
			if score > bestScore:
				bestScore = score
				best_letter = letter
				bestWord = word
				bestHand = hand
		print("I am using the wild card '_' as the letter: ", best_letter)
		print("I will use it to form:", bestWord, end="\n")
		return bestHand
	# For each letter in the game if english is the language
	else:
		for letter in LETTER_BAG_EN.keys():
			hand = list("".join(hand).replace('_', letter))
			word = mr_g_choose_word(hand, wordList, n)
			score = getWordScore(word, n, lan)
			if score > bestScore:
				bestScore = score
				best_letter = letter
				bestWord = word
				bestHand = hand
		print("I am using the wild card '_' as the letter: ", best_letter)
		print("I wil use it to form:", bestWord, end="\n")
		return bestHand


def play_user_turn(hand, list_words, n, discards):
	avail_discards = discards
	turn_score = 0
	while True:
		print("Your turn:")
		print("Current Hand:", end=" ")
		displayHand(hand)
		print('Available letters in the bag :', len(bag_list))
		word = input('Enter a word, "#" to change your letters, or a "." to pass your turn: ')
		print()
		if word == ".":
			break
		elif word == "#":
			while True:
				if avail_discards:
					discard = input("Enter the letters you want to discard, you must keep at least 1 letter: ")
					print()
					if isValidDiscard(discard, hand):
						hand = updateHand(hand, discard)
						hand.extend(deal_hand_user(len(discard)))
						avail_discards -= 1
						if avail_discards == 0:
							print("You have no more discards available")
							print()
							break
						else:
							print("You have", avail_discards, "more changes available")
							print()
						break
					else:
						print("Cannot make that change, please check your selection and try again.")
						print()
				else:
					print("You cannot make more changes.")
					print()
					break
		else:
			valid_word = isValidWord(word, hand, list_words)
			if not valid_word:
				print('Invalid word, please try again.\n')
			else:
				if type(valid_word) is str:
					turn_score += getWordScore(word, n, lan)
					print("Your word is: ", valid_word)
					print('"' + valid_word + '" (' + str(len(valid_word)) + ' letters word) earned',
						  turn_score, '\n')
					hand = updateHand(hand, word)
					hand.extend(deal_hand_user(n - len(hand)))
					break
				else:
					turn_score += getWordScore(word, n, lan)
					print("Your word is: ", word)
					print('"' + word + '" (' + str(len(word)) + ' letters word) earned',
						  turn_score, '\n')
					hand = updateHand(hand, word)
					hand.extend(deal_hand_user(n - len(hand)))
					break
	return turn_score, hand, avail_discards


def play_mr_g_turn(hand, wordList, n):
	turn_score = 0
	while True:
		print("This is my turn:")
		print("Current Hand:", end=" ")
		displayHand(hand)
		print('Available letters in the bag :', len(bag_list))
		sleep(2.0)
		print()
		if "_" in hand:
			hand = mr_g_choose_letter_if_wildcard(hand, wordList, n, lan)
			word = mr_g_choose_word(hand, wordList, n)
		else:
			word = mr_g_choose_word(hand, wordList, n)
		if word is None:
			break
		else:
			if not isValidWord(word, hand, wordList):
				print('This is a terrible error! I need to check my own code!')
				break
			else:
				turn_score += getWordScore(word, n, lan)
				print('My word is: ' + word)
				print('"' + word + '" (' + str(len(word)) + ' letters word) earned',
					  turn_score, 'points.\n')
				sleep(1.5)
				challenge = input('Do you want to challenge the validity of my word? (Y/N): ')
				if challenge == "n":
					hand = updateHand(hand, word)
					hand.extend(deal_hand_mr_g(n - len(hand)))
					break
				elif challenge == "y":
					trial = check_drae(word)
					if trial:
						hand = updateHand(hand, word)
						hand.extend(deal_hand_mr_g(n - len(hand)))
						break
					else:
						print("Oh no! You were right. Okay, I will choose another word.")
						# go to file and erase the word not in drae
						update_words_list_file(word, wordList, WORDS_FILE_SP)
						# pop word from words list
						wordList.remove(word)
						# report the operation to user
						# try a different re loop
	return turn_score, hand


def play_user_final_turn(hand, list_words, n):
	print('No more letters available in the bag.')
	turn_score = 0
	neg_score = 0
	while True:
		print("Your final turn:")
		print("Current Hand:", end=" ")
		displayHand(hand)
		word = input('Enter a word, or a "." to pass: ')
		print()
		if word == ".":
			for letter in hand:
				neg_score += getWordScore(letter, n, lan)
			if len(hand) == n:
				print('Ouch! You have a full hand at the end of the match! That means 50 extra bad points.')
				neg_score += 50
			print(neg_score, 'penalization points for letters left in your hand will be deducted from total score.\n')
			break
		else:
			valid_word = isValidWord(word, hand, list_words)
			if not valid_word:
				print('Invalid word, please try again.\n')
			else:
				if type(valid_word) is str:
					turn_score += getWordScore(word, n, lan)
					print("Your word is: ", valid_word)
					print('"' + valid_word + '" (' + str(len(valid_word)) + ' letters word) earned',
						  turn_score, '\n')
					hand = updateHand(hand, word)
					if hand:
						for letter in hand:
							neg_score += getWordScore(letter, n, lan)
						print(neg_score,
							  'penalization points for letters left in your hand will be deducted from total score.\n')
						break
					else:
						turn_score += 50
						print('Amazing! You have no letters left in your hand. You earned 50 bonus points!\n')
						break
				else:
					turn_score += getWordScore(word, n, lan)
					print("Your word is: ", word)
					print('"' + word + '" (' + str(len(word)) + ' letters word) earned',
						  turn_score, '\n')
					hand = updateHand(hand, word)
					if hand:
						for letter in hand:
							neg_score += getWordScore(letter, n, lan)
						print(neg_score,
							  'penalization points for letters left in your hand will be deducted from total score.\n')
						break
					else:
						turn_score += 50
						print('Amazing! You have no letters left in your hand. You earned 50 bonus points!\n')
						break
	return turn_score - neg_score


def play_mr_g_final_turn(hand, wordList, n):
	print('No more letters available in the bag.')
	turn_score = 0
	neg_score = 0
	while True:
		print("My final turn:")
		print("Current Hand:", end=" ")
		displayHand(hand)
		word = mr_g_choose_word(hand, wordList, n)
		if word is None:
			for letter in hand:
				neg_score += getWordScore(letter, n, lan)
			if len(hand) == n:
				print('Ouch! I have a full hand at the end of the match! That means 50 extra bad points.')
				print('This is terrible! I need to check my own code!')
				neg_score += 50
			print(neg_score, 'penalization points for letters left in my hand will be deducted from total score.')
			print()
			break
		else:
			if not isValidWord(word, hand, wordList):
				print('This is a terrible error! I need to check my own code!')
				break
			else:
				turn_score += getWordScore(word, n, lan)
				print('My word is: ' + word)
				print('"' + word + '" (' + str(len(word)) + ' letters word) earned', turn_score, 'points.\n')
				hand = updateHand(hand, word)
				print()
				if hand:
					for letter in hand:
						neg_score += getWordScore(letter, n, lan)
					print(neg_score,
						  'penalization points for letters left in my hand will be deducted from total score.')
					print()
					break
				else:
					turn_score += 50
					print('Amazing! I have no letters left. I earned 50 bonus points!')
					print()
					break
	return turn_score - neg_score


@greetings
def play_words_challenge(list_words):  # game ending needs work. Option to play again
	global bag_list, HAND_SIZE
	while True:
		print()
		USER_SCORE, USER_HAND = 0, deal_hand_user(HAND_SIZE)
		DISCARDS = 3
		MR_G_SCORE, MR_G_HAND = 0, deal_hand_mr_g(HAND_SIZE)
		while bag_list:
			turn_user_score, USER_HAND, DISCARDS = play_user_turn(USER_HAND, list_words, HAND_SIZE, DISCARDS)
			USER_SCORE += turn_user_score
			print('Your total score is: ', USER_SCORE)
			print("______________________________\n")
			turn_mr_g_score, MR_G_HAND = play_mr_g_turn(MR_G_HAND, list_words, HAND_SIZE)
			MR_G_SCORE += turn_mr_g_score
			print("My total score is: ", MR_G_SCORE)
			print("______________________________\n")
		# loop ends when no more letters are available to deal
		# start last turn
		USER_SCORE += play_user_final_turn(USER_HAND, list_words, HAND_SIZE)
		MR_G_SCORE += play_mr_g_final_turn(MR_G_HAND, list_words, HAND_SIZE)
		if USER_SCORE > MR_G_SCORE:
			print('Congratulations! You won this match...\nYou will not be this lucky next time.')
			print('Your score: ' + str(USER_SCORE) + '.', 'Mr G score: ' + str(MR_G_SCORE))
			print()
		elif USER_SCORE < MR_G_SCORE:
			print("I won the match. No surprise here. Better luck next time.")
			print('Your score: ' + str(USER_SCORE) + '.', 'Mr G score: ' + str(MR_G_SCORE))
			print()
		else:
			print('What is this? A tie? This is revolting!')
			print('Your score: ' + str(USER_SCORE) + '.', 'Mr G score: ' + str(MR_G_SCORE))
			print()

		wanna_play = input("Enter 'S' to start a new game, or 'E' to exit: ")
		while True:
			if wanna_play.lower() == "s":
				lan = set_language()
				bag_list = get_letter_bag(lan)
				HAND_SIZE = get_hand_size()
				break
			elif wanna_play.lower() == "e":
				print()
				return print("Okay. Hasta la vista!")
			else:
				print("I did not quite get that. Please try again.")


if __name__ == '__main__':
	lan = set_language()
	wordList = loadWords(lan)
	bag_list = get_letter_bag(lan)
	HAND_SIZE = get_hand_size()
	play_words_challenge(wordList)
