import random
import sys
import time
from datetime import timedelta
from wordbase import wordbase
try:
	from revision import revision_wordbase
	revision = True
except:
	revision = False

class Training():

	def __init__(self, training_wordbase):
		self.training_wordbase = training_wordbase

	def hello(self):
		print('\n')
		print('*' * 30, '\n')
		print('Test your chinese knowlegde!\nBring pen and paper and write down the corrispondent pinyin and hanzi.\n')
		print('During the test press any key to see the result.')
		print('You can exit from the test anytime pressing CTRL + C.\n')
		print('*' * 30, '\n')

	def goodbye(self, delta):
		print('*' * 30, '\n')
		print('Congratulations! You have finished the training in ' + str(delta))
		print('Your result is ' + str(correct) + ' correct answers out of a total of ' + str(words) + ' words.')
		print('Your success percentage is ' + str(stat) + ' %', '\n')
		print('*' * 30, '\n')

	def exit_message(self):
		print('\n')
		print('[*] Test interrupted! 再见', '\n')
		sys.exit(0)

	def get_time(self):
		return time.time()

	def delta_time(self, start, end):
		return str(timedelta(seconds = int(end - start)))

	def percentage(self, correct, words):
		return float("%0.2f" % (correct * 100 / words))

	def asker(self, question):
		try:
			answer = 0
			check = input(question)
			if check != None:
				check = check.lower()
				if check == 'y':
					answer = True
				elif check == 'n':
					answer = False
				else:
					answer = self.asker(question)
				return answer
		except KeyboardInterrupt:
			self.exit_message()

	def check_levels(self):
		return len(wordbase)

	def select_min_level(self):
		try:
			while True:
				check = input('[+] Select the minimum level: ')
				if check != None:
					try:
						check = int(check)
						if check < 1:
							print('[-] The minimum level must be at least 1.', '\n')
						elif check > self.check_levels():
							print('[-] The number exceeds the total number of levels.', '\n')
						else:
							return check
					except:
			 		 	print('[-] Insert a numeric value.', '\n')	
		except KeyboardInterrupt:
			self.exit_message()

	def select_max_level(self, min_level):
		try:
			while True:
				check = input('[+] Select the maximum level: ')
				if check != None:
					try:
						check = int(check)
						if check < min_level:
							print('[-] The maximum level must be greater of equal than the minimum level.', '\n')
						elif check > self.check_levels():
							print('[-] The number exceeds the total number of levels..', '\n')
						else:
							return check
					except:
			 		 	print('[-] Insert a numeric value.', '\n')	
		except KeyboardInterrupt:
			self.exit_message()

	def prepare_training_wordbase(self, min_level, max_level):
		for l in range(min_level, max_level + 1):
			training_wordbase.update(wordbase['HSK_' + str(l)])
		return training_wordbase

	def loop_training_wordbase(self, training_wordbase):
		return random.choice(list(training_wordbase))

	def ask_word(self, word):
		try:
			check = input('[+] Write down the pinyin and the hanzi for the word "' + str(word) + '".')
			if check != None:
				print('[*] The result for "' + str(word) + '" is ' + str(training_wordbase[word]) + '\n')
		except KeyboardInterrupt:
			self.exit_message()

	def add_to_revision(self, word):
		revision_wordbase[word] = training_wordbase[word]

	def remove_word(self, word):
		del training_wordbase[word]

	def reset_revision(self):
		revision_wordbase = {}
		return revision_wordbase

	def review_revision(self, revision_wordbase):
		print('[*] Take your time and revise the following words: ', '\n')
		for w in revision_wordbase:
			print(w, ': ' + revision_wordbase[w])
		print('')


# start here!
if __name__ == '__main__':

	training_wordbase = {}

	# init and greetings
	t = Training(training_wordbase)
	t.hello()
	# check and ask for revision
	if not revision or not t.asker('[+] Vuoi caricare il dizionario delle parole da ripassare? [y/n]'):
		print('[*] There are ' + str(t.check_levels()) + ' levels available!', '\n')
		# select levels
		min_level = t.select_min_level()
		max_level = t.select_max_level(min_level)
		print()
		print('[*] The selected minimum level is: ' + str(min_level) + ' and the maximum is: '+ str(max_level), '\n')
		training_wordbase = t.prepare_training_wordbase(min_level, max_level)
	else:
		training_wordbase = revision_wordbase
	# init revision wordbase
	revision_wordbase = t.reset_revision()
	# get initial number of words
	words = len(training_wordbase)
	# start time
	start_time = t.get_time()
	# loop until the wordbase is populated
	while bool(training_wordbase):
		# extract a random word
		word = t.loop_training_wordbase(training_wordbase)
		# ask the pinyin and hanzi
		answer = t.ask_word(word)
		# check if the aswer was right
		if t.asker('[+] Was it correct? [y/n]'):
			print('[*] Great!', '\n')
		else:
			print('[*] Don\'t worry, you\'ll do better next time.', '\n')
			t.add_to_revision(word)
		# remove word from training wordbase
		t.remove_word(word)
	else:
		# stop time
		stop_time = t.get_time()
		# calculate delta
		delta = t.delta_time(start_time, stop_time)
		# statistics
		correct = words - len(revision_wordbase)
		stat = t.percentage(correct, words)
		# the test is finished
		t.goodbye(delta)
		# if you made some mistakes
		if bool(revision_wordbase):
			t.review_revision(revision_wordbase)
			# open file
			file = open('revision.py', 'w')
			if t.asker('[+] Do you want to save these words? [y/n]'):
				file.write('revision_wordbase = ' + str(revision_wordbase))
				print('[*] You saved the words to revise, happy study!')
			else:
				file.write('')
			file.close()
