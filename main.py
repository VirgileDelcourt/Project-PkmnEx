from random import choice

from Scripts.Monster import Monster
from Scripts.Move import Move, moves
from Scripts.Types import Type
from Scripts.AttackTypes import Types

pap = Monster("Pap", {}, [moves["Leech"]()], [])
fet = Monster("Fet", {}, [moves["Smash"]()], [])

turn = 1
while pap.get("hp") > 0 and fet.get("hp") > 0:
    print("turn " + str(turn))
    choice(pap.moves).Use(pap, fet)
    choice(fet.moves).Use(fet, pap)
    print(" ")
    turn += 1
