import inspect
import sys
from random import randint
from Scripts.AttackTypes import Types


class Move:
    def __init__(self, name, desc, _pow, acc, _type, require, effect):
        self.name = name
        self.description = desc
        self.power = _pow
        self.accuracy = acc
        if type(_type) != type(Types.Physical):
            raise TypeError("tried to assign a non-type to a move's type")
        self.type = _type
        self.require = require
        self.effect = effect

    def Check(self, user, target):
        for c in self.require:
            if not c(user, target):
                return False
        return True

    def Use(self, user, target):
        if not (user.get("hp") > 0 and target.get("hp") > 0):
            raise RuntimeError("someone tried to use a move while hp < 0 or used it on someone with hp < 0")
        elif not self.Check(user, target):
            raise RuntimeError("Tried to use an unusable move")
        else:
            if self.power > 0 and randint(0, 100) > self.accuracy + user.get("accuracy"):
                print(self.name + " missed")
                return False
            else:
                print(user.name + " succesfully used " + self.name + " on " + target.name)
                if self.type == Types.Physical:
                    damage = target.damage(((self.power / 100) - (target.get("defence") / 100)) * user.get("attack"), self.type)
                elif self.type == Types.Special:
                    damage = target.damage(((self.power / 100) - (target.get("special defence") / 100)) * user.get("special attack"), self.type)
                else:
                    damage = target.damage((self.power / 100), self.type)
                for e in self.effect:
                    e(user, target, damage)
                return True


class Smash(Move):
    def __init__(self):
        super().__init__("Smash", "Weak attack.", 30, 95, Types.Physical, [], [])


class Leech(Move):
    def __init__(self):
        super().__init__("Leech", "User heal 50% of damage dealt.", 50, 100, Types.Physical,
                         [], [lambda user, target, damage: user.heal(damage / 2)])


class Execute(Move):
    def __init__(self):
        super().__init__("Execute", "Instantly kill target if target.hp <= 10%.", 0, 100, Types.Status,
                         [lambda user, target: target.get("hp") > target.get("maxhp") / 10],
                         [lambda user, target, damage: target.kill()])


def get_all_moves():
    _moves = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
    return {m[0]: m[1] for m in _moves if m[1] != Move}


moves = get_all_moves()
