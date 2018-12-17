import random
import time
from datetime import timedelta
from wordbase import wordbase

# create a copy of the wordbase
words_in_progress = {}

# words to study in deep
words_to_study_in_deep = {} 

# start time 
def start_time():
	start = time.time()
	return start

# stop time 
def stop_time():
	end = time.time()
	return end

# calculate delta
def delta_time(start, end):
	delta = str(timedelta(seconds = int(end - start)))
	return delta

# check if there are "words to study in deep" in the beginning of the lesson
def check_words_to_study_in_deep_file():
	try:
		from study_in_deep import words_to_study_in_deep
		if bool(words_to_study_in_deep):
			check = input('Do you want to load the saved "words to study in deep" ? [Y/N] ')
			check = str(check.upper())
			if check == 'Y':
				words_in_progress = words_to_study_in_deep
			elif check == 'N':
				words_in_progress = select_level(wordbase)
			else:
				print('Please type \'Y\' or \'N\'!')
				check_words_to_study_in_deep_file()
			return words_in_progress
	except:
		return select_level(wordbase)

# select the level of the test
def select_level(wordbase):
	level = 0
	check = input('Until what lesson do you want to test your knowledge? Insert a number between 1 and ' + str(len(wordbase)) + '!')
	if check != None:
		try:
			level = int(check)
			if level < 1 or level > len(wordbase):
				print('You must insert a number between 1 and ' + str(len(wordbase)) + '!')
				select_level(wordbase)
		except ValueError:
		    print('You must insert a number between 1 and ' + str(len(wordbase)) + '!')
		    select_level(wordbase)
		# prepare the level of the new wordbase
		for l in range(1, level + 1):
			words_in_progress.update(wordbase['lesson_' + str(l)])
		return words_in_progress

# loop through the new dictionary of words
def loop_random_key(words_in_progress):
	if bool(words_in_progress):
		word = random.choice(list(words_in_progress))
		ask_value(word)
	else:
		stop_time()
		print('Congratulations! You have finished your training in ' + delta_time(start, stop_time()) +  '. Good job!')
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
			print('Please type \'Y\' or \'N\'!')
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
	else:
		with open('study_in_deep.py', 'w') as file:
			file.write('')

# save the "words to study in deep" into a file
def save_words_to_study_in_deep(words_to_study_in_deep):
	check = input('Do you want to save these words? [Y/N] ')
	if check != None:
		check = str(check.upper())
		if check == 'Y':
			with open('study_in_deep.py', 'w') as file:
				file.write('words_to_study_in_deep = ' + str(words_to_study_in_deep))
			print('You saved these words!', '\n')
		elif check == 'N':
			print('You did not saved these words!', '\n')
		else:
			print('Please type \'Y\' or \'N\'!')
			save_words_to_study_in_deep(words_to_study_in_deep)

# start here!
if __name__ == '__main__':
	print('\n')
	print('*' * 30, '\n')
	print('Test your chinese skills!')
	print('Take pencil and paper and write down the corrispondent pinyin / hanzi value.', '\n')
	print('*' * 30, '\n')
	words_in_progress = check_words_to_study_in_deep_file()
	start = start_time()
	loop_random_key(words_in_progress)