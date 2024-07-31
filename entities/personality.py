class Personality:
    def __init__(self):
        self.min_val = -100
        self.max_val = 100
        self._charisma = 1
        self._greed = 1
        self._pride = 1
        self._envy = 1
        self._money_mod = 1
        self._charisma_mod = 1
        self._greed_mod = 1
        self._pride_mod = 1
        self._envy_mod = 1
        self._magic_skill_mod = 1

    def up_charisma(self):
        self._charisma += self._charisma_mod

    def act_of_generosity(self):
        self._greed -= 1
        if self._greed < self.min_val:
            self._greed = self.min_val

    def act_of_greed(self):
        self._greed += 1
        if self._greed > self.max_val:
            self._greed = self.max_val

    def act_of_pride(self):
        self._pride += self._pride_mod
        if self._pride > self.max_val:
            self._pride = self.max_val

    def act_of_humility(self):
        self._pride -= self._pride_mod
        if self._pride < self.min_val:
            self._pride = self.min_val

    def act_of_envy(self):
        self._envy += self._envy_mod
        if self._envy > self.max_val:
            self._envy = self.max_val

    def act_of_kindness(self):
        self._envy -= self._envy_mod
        if self._envy < self.min_val:
            self._envy = self.min_val


# Earn double amount of money from loot and quests
# All greed gains doubled
class WealthSeeker(Personality):
    def __init__(self):
        super().__init__()
        self._greed = 20
        self._greed_mod = 2
        self._money_mod = 2


# Earn double amount of charisma from lessons
# All envy gains doubled
class InfluenceSeeker(Personality):
    def __init__(self):
        super().__init__()
        self._envy = 20
        self._envy_mod = 2
        self._charisma_mod = 2


# Level up magic skill 20 percent faster
# All pride gains doubled
class PowerSeeker(Personality):
    def __init__(self):
        super().__init__()
        self._pride = 20
        self._pride_mod = 1.2
        self._magic_skill_mod = 2
