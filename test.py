import board
import player

player1 = player.Player("jack", 5)
player2 = player.Player("john", 5)
myboard = board.Board(player1, player2)
print(myboard.determine_attacker())
