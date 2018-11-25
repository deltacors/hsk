import random
from wordbase import words

# create a copy to test your skills
words_in_progress = dict(words)  

# loop through the new dictionary of words
def loop_random_key(words_in_progress):
	if bool(words_in_progress):
		word = random.choice(list(words_in_progress))
		ask_value(word)
	else:
		print('Congratulations! You have finished you wordbase.')

# ask te user the pinyin and the hanzi
def ask_value(word):
	print('What\'s the Pinyin and the hanzi for "' + str(word) + '" ?')
	answer = input('Press any key to know the result or "exit" to quit...')
	if answer != None and answer != "exit":
		print('The pinyin and the hanzi for "' + str(word) + '" are ' + str(words_in_progress[word]) + '\n')
		remove_key(word)
		loop_random_key(words_in_progress)
	else:
		exit(0)

# remove from new dictionary a word already asked
def remove_key(word):
	del words_in_progress[word]

# start here!
if __name__ == '__main__':
	print('*' * 30, '\n')
	print('Test your chinese skils!')
	print('Take pencil and paper and write down the corrispondent pinyin / hanzi value.', '\n')
	print('*' * 30, '\n')
	loop_random_key(words_in_progress)