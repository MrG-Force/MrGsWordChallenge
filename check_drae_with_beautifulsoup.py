import requests
import re
from bs4 import BeautifulSoup


def check_drae(word):
	print("The goblins are checking this word with the supreme authorities. This may take some time.\n")
	url = f"https://dle.rae.es/{word}"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	result = str(soup.find(string=re.compile("no está en el Diccionario")))
	if result == "None":
		print(f"'{word}' is a word in Spanish")
		return True
	else:
		print(f"'{word}' is not a word in Spanish")
		return False
