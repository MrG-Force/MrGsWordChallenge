SCRABBLE_LETTER_VALUES_SP = {
	'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'l': 1, 'm': 3,
	'n': 1, 'ñ': 8, 'o': 1, 'p': 3, 'q': 5, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'x': 8, 'y': 4,
	'z': 10, '_': 0
}


# remove words that contain letters not included in the dictionary keys

def loadWords(word_list_name):
	"""
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    word_list_name: a string with the name of the file to open
    """
	wordList = []
	try:
		inFile = open(word_list_name, 'r')
	except FileNotFoundError:
		print('Cannot open', word_list_name + ":", FileNotFoundError)
		return None
	else:
		print("Loading word list from file...")
		# wordList: list of strings
		for line in inFile:
			wordList.append(line.strip().lower())
		print("  ", len(wordList), "words loaded.")
		return wordList


def find_spec_chars(words_list):
	"""
    Args:
        words_list: a list with words

    Returns:
        A dictionary:
            Keys -> strings: special characters (e.g. letters with diaeresis, accent marks or non alphabetic
            characters) found in the list.
            Values -> list: a list of indexes where the special characters are found within the words_list
    """
	spec_chars = {}
	chars = set("abcdefghijklmnñopqrstuvwxyz")
	for i in range(len(words_list)):
		if set(words_list[i]) - chars:
			for char in (set(words_list[i]) - chars):
				if char in spec_chars.keys():
					spec_chars[char].append(i)
				else:
					spec_chars[char] = spec_chars.get(char, [i])
	return spec_chars


def keep_only_if_in_dict(wordsList, wordsDict):
	words = wordsList[:]
	to_remove = []
	for word in words:
		for char in word:
			if char not in wordsDict.keys():
				to_remove.append(word)
	for word in to_remove:
		if word in words:
			words.remove(word)
	return words


def list_to_file(words_list):
	file_name = input('Enter name for the new file (e.g. "listfile.txt"): ')
	with open(file_name, 'w') as file_handle:
		for list_item in words_list:
			file_handle.write('%s\n' % list_item)
	print(file_name, "successfully created.")


def replace_spec_chars(dictionary, words):
	"""
    Args:
        dictionary: keys -> special characters(strings):
                    values -> indices of words in the list_of_words where the character appears
        words: a list of words containing special characters

    Returns:
        words_list: the given list with the special characters removed
    """
	words_list = words[:]
	changes = 0
	print("Characters to replace are: ", end="")
	for key in dictionary:
		print("'" + key + "'", end=" ")
	print()
	# get the character to replace from the dictionary key
	for key in dictionary:
		print('Enter a replacement character for', "'" + key + "'", end=": ")
		rplcmnt = input()
		for indx in dictionary.get(key):
			words_list[indx] = words_list[indx].replace(key, rplcmnt)
			changes += 1
	print(changes, "replacements made")
	return words_list


def update_words_list_file(word, words_list, file_name):
	with open(file_name, 'w') as file_handle:
		for list_item in words_list:
			if list_item != word:
				file_handle.write('%s\n' % list_item)


original = loadWords("animales.txt")
print(original)
update_words_list_file("koala", original, "animales.txt")
updtd = loadWords("animales.txt")
print(updtd)