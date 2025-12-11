# ============================================================
#                        IMPORTS
# ============================================================
from Enemy import *
import random


# ============================================================
#                           OGRE
# ============================================================
class Ogre(Enemy):

    def __init__(self, health_points=10, attack_damage=1):
        super().__init__(
            type_of_enemy="Ogre",
            health_points=health_points,
            attack_damage=attack_damage
        )


    # ========================================================
    #                           TALK
    # ========================================================
    def talk(self):
        print("Ogre is slamming hand all around")


    # ========================================================
    #                        SPECIAL ATTACK
    # ========================================================
    def special_attack(self):
        did_special_attack_work = random.random() < 0.20
        if did_special_attack_work:
            self.attack_damage += 4
            print("Ogre gets angry and increase attack by 4")
