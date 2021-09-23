import classes

match = classes.Game()
match.setup()


def guidelines():
    """
    Author: Parmenion Charistos
    Class: Learning Theories
    Date: September 2021
    Description: Scrabble Simulator


    PROJECT STRUCTURE


        CLASSES & METHODS:

        Sack: Objects of this class represent the sack of letters in a typical game of Scrabble.

            get_letters(self, n):
                Gets n letters from the pouch randomly, updates the pouch status by removing the chosen
                letters and returns them in the form of a list.

            put_back_letters(self, hand):
                Returns all the letters contained in the hand parameter to the pouch.

            reroll(self, hand):
                Calls the put_back_letters() method and then draws a new hand from the pouch randomly.

        Player: The parent class for all players of the game, either Human or AI (bot).
            This class passes down its __init__ and __repr__ methods to its children.

        Human: Objects of this class represent the Human player.
            This class just overrides the parent's __repr__ method.

        Computer: Objects of this class represent the AI player (bot).

            play(self, hand, mode):
                Implements the gameplay on the side of the Computer. Based on the current hand
                of the AI Player and the selected mode, the respective scenario is executed,
                effectively playing a full turn.

        Game: A Game object holds all the information for a match of Scrabble and acts as the control class in the MVC model
        architecture.

            setup(self):
                Sets up the game based on the user's inputs, whilst providing the according menus.
                Gives options for starting a game, seeing the local game history, changing game modes
                and this amazing help guide.

            run(self):
                Starts a game of Scrabble, with the activated mode selected during the setup.
                Executes all actions for a smooth gameplay, whilst retrieving important information
                from the game files.

            end(self):
                Saves the game's stats on the respective game file.


        FUNCTIONS:

        check(word, hand):
            Checks if the word given consists of the letters included in the hand argument.
            If not, returns false, otherwise, returns the result of teh validate function.

        validate(word):
            Checks if the word given exists in the game's dictionary.
            If not, returns false, otherwise, calculates and returns the score.

        linebreak():
            Formatting function for greater readability.
            Prints lots of dashes in a line.

        superscript():
            Formatting function for greater readability.
            Helps transform the points of each letter to a superscript for fancy gameplay.

        guidelines():
            Contains all the author's notes on the program, from project structure to gameplay instructions.


        DATA STRUCTURE USED FOR WORDLIST

            A dictionary was used for maximum efficiency.
            The words acted as keys and their respective sum of points, based on standard Scrabble rules,
            acted as the respective values for the pair.
            This structure allowed for fast execution times when running the algorithms for the AI player.


        IMPLEMENTED SCENARIO FOR PLAY METHOD:

            The first suggested scenario was implemented, consisting of the following modes:
                Min Letters: Form permutations from lower to higher number of letters and play the first word found.
                Max Letters: Reverse Min Letters (higher to lower number of letters)
                Smart: Form all permutations and propose the word with the maximum score.


        IMPORTANT NOTES:
            The game is follows the classic Scrabble rules.
            for the game to be fully functional, initially (first-time execution) the game files should consist of the following:
                The greek7.txt file should not be altered by any mean, as it normally contains a pool of 7-letter words.
                The game_history_stats.json file should contain just an empty list declaration --> []
                The last_session_mode.json file should contain just the following string --> "1"
    """
