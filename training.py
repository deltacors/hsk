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
			check = input('Vuoi caricare il dizionario delle parole da ripassare? [y/n] ')
			check = str(check.upper())
			if check == 'Y':
				words_in_progress = words_to_study_in_deep
			elif check == 'N':
				words_in_progress = select_level(wordbase)
			else:
				print('Digita \'Y\' o \'N\'!')
				check_words_to_study_in_deep_file()
			return words_in_progress
	except:
		return select_level(wordbase)

# select the level of the test
def select_level(wordbase):
	level = 0
	check = input('Fino a che lezione vuoi testare le tue skills? Inserisci un numero tra 1 e ' + str(len(wordbase)) + '!')
	if check != None:
		try:
			level = int(check)
			if level < 1 or level > len(wordbase):
				print('Devi inserire un numero tra 1 e ' + str(len(wordbase)) + '!')
				select_level(wordbase)
		except ValueError:
		    print('Devi inserire un numero tra 1 e ' + str(len(wordbase)) + '!')
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
		print('Congratulazioni! Hai finito il tuo training in ' + delta_time(start, stop_time()) +  '. Ottimo lavoro!')
		check_words_to_study_in_deep(words_to_study_in_deep)
		
# ask te user the pinyin and the hanzi
def ask_value(word):
	print('Scrivi il pinyin e l\'hanzi che corrispondono alla parola ' + str(word) + '" ?')
	answer = input('Premi un qualsiasi tasto per vedere la soluzione o "exit" per uscire.')
	if answer != None and answer != "exit":
		print('Il risultato per "' + str(word) + '" é ' + str(words_in_progress[word]) + '\n')
		check_value(word)
		loop_random_key(words_in_progress)
	else:
		exit(0)

# check value
def check_value(word):
	check = input('Corretto? [y/n] ')
	if check != None:
		check = str(check.upper())
		if check == 'Y':
			print('Ottimo!', '\n')
			remove_key(word)
		elif check == 'N':
			print('Non preoccuparti, farai meglio il prossimo tentativo.', '\n')
			add_words_to_study_in_deep(word)
			remove_key(word)
		else:
			print('Digita \'Y\' o \'N\'!')
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
		print('Prenditi del tempo per ripassare le seguenti parole: ', '\n')
		for w in words_to_study_in_deep:
			print(w, ': ', words_to_study_in_deep[w])
		save_words_to_study_in_deep(words_to_study_in_deep)
	else:
		with open('study_in_deep.py', 'w') as file:
			file.write('')

# save the "words to study in deep" into a file
def save_words_to_study_in_deep(words_to_study_in_deep):
	check = input('Vuoi salvare queste parole? [y/n] ')
	if check != None:
		check = str(check.upper())
		if check == 'Y':
			with open('study_in_deep.py', 'w') as file:
				file.write('words_to_study_in_deep = ' + str(words_to_study_in_deep))
			print('Hai salvato le parole da approfondire!', '\n')
		elif check == 'N':
			print('Non hai salvato le parole.', '\n')
		else:
			print('Digita \'Y\' o \'N\'!')
			save_words_to_study_in_deep(words_to_study_in_deep)

# start here!
if __name__ == '__main__':
	print('\n')
	print('*' * 30, '\n')
	print('Testa le tue conoscenze della lingua cinese!')
	print('Prendi carta e penna e scrivi il pinyin e l\'hanzi che corrispondono alla parola in italiano.', '\n')
	print('*' * 30, '\n')
	words_in_progress = check_words_to_study_in_deep_file()
	start = start_time()
	loop_random_key(words_in_progress)