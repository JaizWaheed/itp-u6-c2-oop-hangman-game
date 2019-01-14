from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=False, miss=False):
        if hit and miss:
            raise InvalidGuessAttempt()
        self.letter = letter
        self.hit = hit
        self.miss = miss   
        
    def is_hit(self):
        return self.hit
    
    def is_miss(self):
        return self.miss

class GuessWord(object):
    def __init__(self, word):
        if word is '':
            raise InvalidWordException()
        self.answer = word.lower()
        self.masked = len(word) * '*'
        
    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException()
        letter = letter.lower()
        if letter in self.answer:
            attempt = GuessAttempt(letter, hit=True)
            word_letters = list(self.answer)
            masked_letters = list(self.masked)
            for x,y in enumerate(word_letters):
                if y == letter:
                    masked_letters[x] = y
            self.masked = ''.join(masked_letters)
        if letter not in self.answer:
            attempt = GuessAttempt(letter, miss=True)
        return attempt
        
        
class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.word_list = word_list
        selected_word = self.select_random_word(self.word_list)
        self.word = GuessWord(selected_word.lower())
        self.previous_guesses = [] 
        
    @classmethod
    def select_random_word(cls, word_list):
        if word_list == []:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
    
    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException()
        letter = letter.lower()
        attempt = self.word.perform_attempt(letter)
        self.previous_guesses.append(letter)
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()
            
        if self.is_won():
            raise GameWonException()
            
        return attempt
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
        
