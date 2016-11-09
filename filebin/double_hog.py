import random

players = []

def double_hog():
    try:
        print("======== DOUBLE HOG ========")
        print()
        get_players()
        main_loop()
    except (KeyboardInterrupt, EOFError):
        print()
        print()
        print("Goodbye.")

def get_players():
    """Get the players' names and add them to the list."""
    # Get how many players
    while True:
        try:
            player_count = int(input("How many players? "))
        except ValueError:
            print("Enter a number.")
            continue
        if player_count < 2:
            print("Not enough players.")
        elif player_count > 4:
            print("Too many players.")
        else:
            break
    # Get the players' names
    for dummy in range(player_count):
        name = input("Enter a name: ")
        players.append(Player(name))
    print()
    return players

def main_loop():
    """Play until somebody wins."""
    try:
        while True:
            for player in players:
                player.turn()
    except GameEnded as ex:
        print()
        print("======== %s wins! ========" % ex.player.name)
        # Sort players by score in descending order
        players.sort(key=lambda player: player.score, reverse=True)
        # Say player names and scores
        for player in players:
            player.announce()

class GameEnded(Exception):
    """Raised when the game ends."""
    def __init__(self, player):
        super().__init__()
        self.player = player

class Player:
    """Represents a player."""
    def __init__(self, name):
        self.name = name
        self.score = 0
    def announce(self):
        """Say their name and score."""
        print("Player: %s\t\tScore: %d" % (self.name, self.score))
    def change_score(self, dice1, dice2):
        """Change their score according to the dice."""
        if single_1(dice1, dice2):
            self.score -= dice1 + dice2
        elif dice1 == 1 and dice2 == 1:
            self.score += 25
        elif dice1 == dice2:
            self.score += (dice1 + dice2) * 2
        else:
            self.score += dice1 + dice2
    def turn(self):
        """Take a turn."""
        self.announce()
        while True:
            roll_dice = input("Roll dice? (y/n) ").lower()
            if roll_dice == 'y':
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)
                print("Dice 1: %d\t\tDice 2: %d" % (dice1, dice2))
                # Change their score
                self.change_score(dice1, dice2)
                # If their score is >= 100 they won
                if self.score >= 100:
                    raise GameEnded(self)
                # If they rolled a single one their turn ends
                if single_1(dice1, dice2):
                    break
            elif roll_dice == 'n':
                break
            else:
                print("Enter 'y' or 'n'.")
        print("Your score is %d" % self.score)

def single_1(dice1, dice2):
    """Return if dice1 or dice2 is 1 but not both."""
    return (dice1 == 1 and dice2 != 1) or (dice1 != 1 and dice2 == 1)

double_hog()
