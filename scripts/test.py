import board
import player
import hero

hero.parse_hero_powers()
for key in hero.HeroPower.hero_power_dict.keys():
    print(hero.HeroPower.hero_power_dict[key])

