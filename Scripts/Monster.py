from Scripts.AttackTypes import Types


class Monster:
    def __init__(self, name: str, stats: dict, move: list, types: list):
        self.name = name
        self.level = 1
        self.exp = 0
        self.__hurt = 0
        self.__stats = stats
        self.init_stats()
        if len(move) > 4:
            move = move[:4]
        self.moves = move
        self.types = {t.__name__: t for t in types}

    def __repr__(self):
        return self.name

    def init_stats(self):
        if "accuracy" not in self.__stats:
            self.__stats["accuracy"] = 0
        if "maxhp" not in self.__stats:
            self.__stats["maxhp"] = 50
        if "attack" not in self.__stats:
            self.__stats["attack"] = 10
        if "special attack" not in self.__stats:
            self.__stats["special attack"] = 10
        if "defence" not in self.__stats:
            self.__stats["defence"] = 5
        if "special defence" not in self.__stats:
            self.__stats["special defence"] = 5
        if "speed" not in self.__stats:
            self.__stats["speed"] = 10

    def get(self, *args):
        try:
            ans = []
            for i in args:
                if i == "hp":
                    ans.append(self.get("maxhp") - self.get("hurt"))
                elif i == "hurt":
                    ans.append(self.__hurt)
                else:
                    ans.append(self.__stats[i])
            if len(ans) == 1:
                return ans[0]
            return ans
        except KeyError:
            raise KeyError("tried to get a non-existant stat")

    def damage(self, damage, _type):
        damage = int(damage)
        if damage < 0:
            damage = 0
        self.__hurt += damage
        if self.get("hp") < 0:
            self.__hurt = self.get("maxhp")
        print(self.name + " took " + str(damage) + " damage (" + str(self.get("hp")) + " hp remaining)")
        if self.get("hp") <= 0:
            self.kill()
        return damage

    def kill(self):
        print(self.name + " died")
        self.__hurt = self.get("maxhp")
        del self

    def heal(self, heal):
        heal = int(heal)
        self.__hurt -= int(heal)
        if self.__hurt < 0:
            self.__hurt = 0
        print(self.name + " recovered " + str(heal) + " hp (" + str(self.get("hp")) + " hp remaining)")
