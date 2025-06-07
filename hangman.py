import threading

VALID_LETTERS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

class hangman(threading.Thread):
    def __init__(self, guess, guess_queue, hang_lock, global_queue, user):
        super().__init__()
        self.guess = word(guess)
        self.guesses = 6
        self.queue = guess_queue
        self.lock = hang_lock
        self.game = True
        self.gq = global_queue
        self.user = user

    def run(self):
        acquired = self.lock.acquire(blocking=False)
        self.queue.put(None)
        empty_queue = 1
        while empty_queue != None:
            empty_queue = self.queue.get()
        if acquired:
            self.gq.put((f"{self.guess.return_word()}\n GUESSES:{self.guesses}", "++HANGMAN++"))
            while self.game:
                letter = self.queue.get()
                correct = self.guess.guess_let(letter)
                if correct == False:
                    self.guesses -= 1
                if self.guess.check_win() == True:
                    self.gq.put((f"CONGRATS YOU GUESSED:\n{self.guess.return_word()}\nWITH {6 - self.guesses} WRONG GUESSES", "++HANGMAN++"))
                    self.game = False

                elif self.guesses == 0:
                    self.gq.put((f"The Word Was:\n{self.guess.get_word()}", "++HANGMAN++"))
                    self.game = False
                else:
                    self.gq.put((f"{self.guess.return_word()}\n GUESSES:{self.guesses}", "++HANGMAN++"))
            self.gq.put(("GAME OVER", "++HANGMAN++"))
            self.lock.release()
        else:
            self.gq.put(("Game Already in Progress", "HANGMAN", self.user))

class word():
    def __init__(self, word):
        self.word = []
        for let in word:
            self.word.append(letter(let, VALID_LETTERS))
    
    def return_word(self):
        word_string = ""
        for letter in self.word:
            word_string += letter.return_let() + " "
        return word_string
    
    def get_word(self):
        word_string = ""
        for letter in self.word:
            word_string += letter.get_let()
        return word_string
    
    def guess_let(self,let):
        worked = False
        if let.upper() in VALID_LETTERS:
            for letter in self.word:
                if let.upper() == letter.get_let():
                    worked = letter.unhide()
            return worked
        return True
    
    def check_win(self):
        won = True
        for let in self.word:
            hid = let.return_status()
            if hid:
                won = False
        return won
        
    
class letter():
    def __init__(self, let, valid_letters=VALID_LETTERS):
        self.let = let.upper()
        if self.let in valid_letters:
            self.hidden = True
        else:
            self.hidden = False

    def return_status(self):
        return self.hidden
    
    def return_let(self):
        if self.hidden:
            return '_'
        else:
            return self.let
    
    def get_let(self):
        return self.let

    def unhide(self):
        if self.hidden:
            self.hidden = False
            return True
        else:
            return False

    def hide(self):
        if self.hidden == False:
            self.hidden = True
            return True
        else:
            return False
        
def main():
    my_word = word("Hello")
    print(my_word.return_word())
    my_word.guess_let('l')
    my_word.guess_let('o')
    my_word.guess_let('p')
    print(my_word.check_win())
    print(my_word.return_word())
    my_word.guess_let('e')
    my_word.guess_let('h')
    print(my_word.return_word())
    print(my_word.check_win())


if __name__ == "__main__":
    main()