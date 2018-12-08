import random
from wordbase import wordbase

# create a copy of the wordbase
words_in_progress = {}

# words to study in deep
words_to_study_in_deep = {} 

# count the lessons available
def lessons_available(wordbase):
	return len(wordbase)

# select the level of the test
def select_level(wordbase):
	check = input('Select your level! Insert a number between 1 and ' + str(lessons_available(wordbase)) + '!')
	if check != None:
		try:
   			level = int(check)
	   		if level < 1 or level > lessons_available(wordbase):
	   			print('You must insert a number between 1 and ' + str(lessons_available(wordbase)) + '!')
	   			select_level(wordbase)
		except ValueError:
		    print('You must insert a number between 1 and ' + str(lessons_available(wordbase)) + '!')
		    select_level(wordbase)
		prepare_wordbase(level)

# prepare the new wordbase
def prepare_wordbase(level):
	for l in range(1, level + 1):
		words_in_progress.update(wordbase['lesson_' + str(l)])
	return words_in_progress

# loop through the new dictionary of words
def loop_random_key(words_in_progress):
	if bool(words_in_progress):
		word = random.choice(list(words_in_progress))
		ask_value(word)
	else:
		print('Congratulations! You have finished you wordbase. Good job!')
		check_words_to_study_in_deep(words_to_study_in_deep)
		
# ask te user the pinyin and the hanzi
def ask_value(word):
	print('What\'s the Pinyin and the hanzi for "' + str(word) + '" ?')
	answer = input('Press any key to know the result or "exit" to quit the training.')
	if answer != None and answer != "exit":
		print('The pinyin and the hanzi for "' + str(word) + '" are ' + str(words_in_progress[word]) + '\n')
		check_value(word)
		loop_random_key(words_in_progress)
	else:
		exit(0)

# check value
def check_value(word):
	check = input('Was it correct? [Y/N] ')
	if check != None:
		check = str(check.upper())
		if check == 'Y':
			print('Nice shot!', '\n')
			remove_key(word)
		elif check == 'N':
			print('Don\'t worry, you\'ll do better next time.', '\n')
			add_words_to_study_in_deep(word)
			remove_key(word)
		else:
			print('Please type \'Y\' or \'N\' to check your answer!')
			check_value(word)

# remove from new dictionary a word already asked
def remove_key(word):
	del words_in_progress[word]

# add word to the "words to study in deep" dictionary
def add_words_to_study_in_deep(word):
	words_to_study_in_deep[word] = words_in_progress[word]

# check if there are "words to study in deep" in the end of the lesson
def check_words_to_study_in_deep(words_to_study_in_deep):
	if bool(words_to_study_in_deep):
		print('Take some time to study in deep the following words: ', '\n')
		for w in words_to_study_in_deep:
			print(w, ': ', words_to_study_in_deep[w])
		save_words_to_study_in_deep(words_to_study_in_deep)

# save the "words to study in deep" into a file
def save_words_to_study_in_deep(words_to_study_in_deep):
	check = input('Do you want to save these words? [Y/N] ')
	if check != None:
		check = str(check.upper())
		if check == 'Y':
			file = open('study_in_deep.py', 'w')
			file.write(str(words_to_study_in_deep))
			file.close()
			print('File saved!', '\n')
		elif check == 'N':
			print('File not saved!', '\n')
		else:
			print('Please type \'Y\' or \'N\'!')
			save_words_to_study_in_deep(words_to_study_in_deep)

# check if there are "words to study in deep" in the beginning of the lesson
def check_words_to_study_in_deep_file(words_to_study_in_deep):
	pass

# start here!
if __name__ == '__main__':
	print('*' * 30, '\n')
	print('Test your chinese skills!')
	print('Take pencil and paper and write down the corrispondent pinyin / hanzi value.', '\n')
	print('*' * 30, '\n')
	# check_words_to_study_in_deep_file(words_to_study_in_deep)
	# if yes, words_to_study_in_deep = file
	# if no , select_level(wordbase)
	select_level(wordbase)
	loop_random_key(words_in_progress)