import random
import json
import sys
import itertools


class Sack:

    startup_pouch = {'Α': [12, 1], 'Β': [1, 8], 'Γ': [2, 4], 'Δ': [2, 4], 'Ε': [8, 1],
                     'Ζ': [1, 10], 'Η': [7, 1], 'Θ': [1, 10], 'Ι': [8, 1], 'Κ': [4, 2],
                     'Λ': [3, 3], 'Μ': [3, 3], 'Ν': [6, 1], 'Ξ': [1, 10], 'Ο': [9, 1],
                     'Π': [4, 2], 'Ρ': [5, 2], 'Σ': [7, 1], 'Τ': [8, 1], 'Υ': [4, 2],
                     'Φ': [1, 8], 'Χ': [1, 8], 'Ψ': [1, 10], 'Ω': [3, 3]}

    def __init__(self):
        self.pouch = Sack.startup_pouch.copy()
        self.letters_left = 102

    def get_letters(self, n):
        if self.letters_left - n < 0:
            return False

        hand = []
        items = list(self.pouch.items())

        for i in range(n):
            letter, info = random.choice(items)
            while info[0] == 0:
                letter, info = random.choice(items)

            hand.append(letter)
            self.letters_left -= 1
            self.pouch[letter][0] -= 1

        return hand

    def put_back_letters(self, hand):
        for letter in hand:
            self.pouch[letter][0] += 1
            self.letters_left += 1

    def reroll(self, hand):
        hand_copy = hand.copy()
        hand = self.get_letters(Game.hand_size)
        self.put_back_letters(hand_copy)
        return hand


class Player:

    def __init__(self):
        self.hand = []
        self.score = 0

    def __repr__(self):
        hand = ""
        for letter in self.hand:
            hand += letter + superscript(str(Sack.startup_pouch[letter][1])) + ", "
        hand = hand[:len(hand) - 2]
        return str(hand)


class Human(Player):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        hand_desc = super().__repr__()
        return 'Γράμματα Παίκτη: ' + hand_desc


class Computer(Player):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        hand_desc = super().__repr__()
        return 'Γράμματα Υπολογιστή: ' + hand_desc

    def play(self, hand, mode):
        hand = ''.join(hand)

        if mode == '1':
            for length in range(2, 8):
                wordset = list(itertools.permutations(hand, length))

                for word in wordset:
                    word = ''.join(word)
                    score, is_valid = validate(word)
                    if is_valid:
                        return word, score

            return False, 0
        elif mode == '2':
            for length in range(7, 1, -1):
                wordset = list(itertools.permutations(hand, length))

                for word in wordset:
                    word = ''.join(word)
                    score, is_valid = validate(word)
                    if is_valid:
                        return word, score

            return False, 0
        else:
            wordset = []
            for length in range(2, 8):
                wordset += itertools.permutations(hand, length)

            max_score = 0
            best_word = ''
            for word in wordset:
                word = ''.join(word)
                score = Game.dictionary.get(word, 0)

                if score > max_score:
                    max_score = score
                    best_word = word

            return best_word, max_score


class Game:

    options_strings = ['Παίξε', 'Ιστορικό', 'Ρυθμίσεις', 'Έξοδος']
    options_modes = ['Min Letters', 'Max Letters', 'Smart']
    options_codes = ['1', '2', '3', 'q']
    hand_size = 7

    try:
        with open('../res/greek7.txt', 'r', encoding='utf-8') as f:
            word_list = f.readlines()
        word_list = [x.strip() for x in word_list]
        dictionary = {}

        for word in word_list:
            score = 0
            for letter in word:
                score += Sack.startup_pouch[letter][1]
            dictionary[word] = score

    except FileNotFoundError:
        print('Δεν βρέθηκε το αρχείο greek7.txt')

    def __init__(self):
        with open('../res/game_history_stats.json', 'r') as readable:
            self.info = json.load(readable)
        with open('../res/last_session_mode.json', 'r') as also_readable:
            self.mode = json.load(also_readable)

        self.total_turns = 0
        self.sack = Sack()
        self.player = Human()
        self.AI = Computer()

    def __repr__(self):
        pass

    def setup(self):
        user_input = ''
        while user_input not in Game.options_codes:
            print('**************** SCRABBLE ****************')
            linebreak()
            for i in range(len(Game.options_strings)):
                print(f'{Game.options_codes[i]}. {Game.options_strings[i]}')
            linebreak()
            user_input = str(input())

        if user_input == 'q':
            linebreak()
            print('Τερματισμός!')
            linebreak()
            sys.exit()
        elif user_input == '1':
            self.run()
        elif user_input == '2':
            for summary in self.info:
                columns = str.split(summary, '|')
                print((columns[0] + '|' + '{:^24}' + '|' + columns[2]).format(columns[1]))
            input("\nEnter για επιστροφή στο αρχικό μενού..")
            linebreak()
            self.setup()
        else:
            mode_selected = ''
            while mode_selected not in Game.options_codes:
                linebreak()
                for i in range(len(Game.options_modes)):
                    if self.mode == Game.options_codes[i]:
                        print(f'{Game.options_codes[i]}. {Game.options_modes[i]} (επιλεγμένο)')
                    else:
                        print(f'{Game.options_codes[i]}. {Game.options_modes[i]}')
                linebreak()
                mode_selected = str(input())

            self.mode = mode_selected
            self.setup()

    def run(self):
        self.player.hand = self.sack.get_letters(Game.hand_size)
        self.AI.hand = self.sack.get_letters(Game.hand_size)

        player_turn = True
        sack_is_full = True
        bot_can_play = True
        player_can_play = True

        while sack_is_full and bot_can_play and player_can_play:
            linebreak()
            if player_turn:
                print('Σακουλάκι: ' + str(self.sack.letters_left) + ' γράμματα\n' + str(self.player))
                is_valid = False

                while not is_valid:
                    word = str(input('Παίξε: '))
                    word = word.strip()
                    linebreak()

                    if word == 'q':
                        player_can_play = False
                        break
                    elif word == 'p':
                        print('Πήγες πάσο!')
                        self.player.hand = self.sack.reroll(self.player.hand)
                        player_turn = False

                        if not self.player.hand:
                            sack_is_full = False
                        break

                    score, is_valid = check(word, self.player.hand)

                    if not is_valid:
                        if score == 0:
                            print('Η λέξη σου πρέπει να αποτελείται μόνο από τα διαθέσιμα γράμματά σου!')
                            linebreak()
                        else:
                            print('Δεν υπάρχει αυτή η λέξη!')
                            linebreak()
                    else:
                        self.player.score += score
                        player_turn = False
                        for letter in word:
                            self.player.hand.remove(letter)

                        print('Αποδεκτή Λέξη! Κέρδισες ' + str(score) + ' πόντους! Έχεις συνολικά ' + str(
                            self.player.score) + ' πόντους.')
                        input("Enter για συνέχεια..")
                        self.total_turns += 1

                        fill_up = self.sack.get_letters(Game.hand_size - len(self.player.hand))
                        if not fill_up:
                            sack_is_full = False
                            break

                        self.player.hand += fill_up
            else:
                print(str(self.AI))
                hand = []
                for i in range(len(self.AI.hand)):
                    hand.append(self.AI.hand[i][0])

                word, score = self.AI.play(hand, self.mode)
                if not word:
                    bot_can_play = False
                else:
                    self.AI.score += score
                    for letter in word:
                        self.AI.hand.remove(letter)

                    print("Ο Η/Υ βρήκε τη λέξη " + str(word) + ". Κέρδισε " + str(
                        score) + " πόντους! Έχει συνολικά " + str(self.AI.score) + " πόντους.")

                    fill_up = self.sack.get_letters(Game.hand_size - len(self.AI.hand))

                    if not fill_up:
                        sack_is_full = False

                    self.total_turns += 1
                    self.AI.hand += fill_up
                    player_turn = True

        if not sack_is_full:
            print('Τέλειωσαν τα γράμματα!')
        elif not player_can_play:
            print('Σταμάτησες το παιχνίδι!')
        else:
            print('Ο Η/Υ παραιτήθηκε!')

        linebreak()
        print('Τέλος Παρτίδας!')

        print('Παίκτης: ' + str(self.player.score) + ' - Η/Υ: ' + str(self.AI.score))
        if self.player.score > self.AI.score:
            print('Νίκησες!')
        elif self.player.score < self.AI.score:
            print('Έχασες!')
        else:
            print('Ισοπαλία!')

        self.end(self.total_turns, self.AI.score, self.player.score)
        linebreak()

        choice = ""

        while choice != "q" and choice != "p":
            print("q. Αρχικό Μενού\np. Ξαναπαίξε")
            linebreak()
            choice = str(input())

            if choice != "p":
                linebreak()

            match = Game()
            if choice == "q":
                match.setup()
            elif choice == "p":
                match.run()

    def end(self, turns, AI_score, player_score):
        game_summary = 'Κινήσεις: ' + str(turns) + " | Παίκτης: " + str(player_score) + " - H/Y: " + str(AI_score)
        if AI_score > player_score:
            game_summary += " | Ήττα"
        elif AI_score < player_score:
            game_summary += " | Νίκη"
        else:
            game_summary += " | Ισοπαλία"
        self.info.append(game_summary)

        with open('../res/game_history_stats.json', 'w') as writable:
            json.dump(self.info, writable)

        with open('../res/last_session_mode.json', 'w') as also_writable:
            json.dump(self.mode, also_writable)


def check(word, hand):
    hand_copy = hand.copy()

    n = 0
    for i in word:
        for j in range(len(hand_copy)):
            if i == hand_copy[j][0]:
                hand_copy.pop(j)
                n += 1
                break

    if n != len(word):
        return 0, False

    return validate(word)


def validate(word):
    verdict = Game.dictionary.get(word)
    if not verdict:
        return 1, False

    score = 0
    for letter in word:
        score += Sack.startup_pouch[letter][1]

    return score, True


def linebreak():
    print('------------------------------------------')


def superscript(word):
    original = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    substrings = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    result = word.maketrans(''.join(original), ''.join(substrings))
    return word.translate(result)
