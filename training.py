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
		print('Testa le tue conoscenze della lingua cinese! \nPrendi carta e penna e scrivi il pinyin e l\'hanzi che corrispondono alla parola in italiano.\n')
		print('Durante il test premi un qualsiasi tasto per vedere la parola richiesta.')
		print('Puoi uscire in qualsiasi momento digitando CTRL + C.\n')
		print('*' * 30, '\n')

	def goodbye(self, delta):
		print('*' * 30, '\n')
		print('Congratulazioni! Hai finito il tuo training in ' + str(delta))
		print('Il tuo risultato è ' + str(correct) + ' risposte esatte su un totale di ' + str(words) + ' parole.')
		print('La tua percentuale di successo è del ' + str(stat) + ' %', '\n')
		print('*' * 30, '\n')

	def exit_message(self):
		print('\n')
		print('[*] Test interrotto! 再见', '\n')
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
				check = input('[+] Inserisci il livello minimo da cui partire: ')
				if check != None:
					try:
						check = int(check)
						if check < 1:
							print('[-] Il livello minimo non può essere inferiore a 1.', '\n')
						elif check > self.check_levels():
							print('[-] Il numero inserito supera le lezioni disponibili.', '\n')
						else:
							return check
					except:
			 		 	print('[-] Inserisci un valore numerico.', '\n')	
		except KeyboardInterrupt:
			self.exit_message()

	def select_max_level(self, min_level):
		try:
			while True:
				check = input('[+] Inserisci il livello massimo fino a cui vuoi arrivare: ')
				if check != None:
					try:
						check = int(check)
						if check < min_level:
							print('[-] Il livello massimo deve essere superiore al livello minimo.', '\n')
						elif check > self.check_levels():
							print('[-] Il numero inserito supera le lezioni disponibili.', '\n')
						else:
							return check
					except:
			 		 	print('[-] Inserisci un valore numerico.', '\n')	
		except KeyboardInterrupt:
			self.exit_message()

	def prepare_training_wordbase(self, min_level, max_level):
		for l in range(min_level, max_level + 1):
			training_wordbase.update(wordbase['lesson_' + str(l)])
		return training_wordbase

	def loop_training_wordbase(self, training_wordbase):
		return random.choice(list(training_wordbase))

	def ask_word(self, word):
		try:
			check = input('[+] Scrivi il pinyin e l\'hanzi che corrispondono alla parola "' + str(word) + '".')
			if check != None:
				print('[*] Il risultato per "' + str(word) + '" é ' + str(training_wordbase[word]) + '\n')
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
		print('[*] Prenditi del tempo per ripassare le seguenti parole: ', '\n')
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
		print('[*] Ci sono ' + str(t.check_levels()) + ' lezioni disponibili!', '\n')
		# select levels
		min_level = t.select_min_level()
		max_level = t.select_max_level(min_level)
		print()
		print('[*] Hai selezionato livello minimo: ' + str(min_level) + ' e livello massimo: '+ str(max_level), '\n')
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
		if t.asker('[+] Hai risposto correttamente? [y/n]'):
			print('[*] Ottimo!', '\n')
		else:
			print('[*] Non preoccuparti, farai meglio il prossimo tentativo.', '\n')
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
			if t.asker('[+] Vuoi salvare queste parole? [y/n]'):
				file.write('revision_wordbase = ' + str(revision_wordbase))
				print('[*] Hai salvato le parole da approfondire, buono studio!')
			else:
				file.write('')
			file.close()