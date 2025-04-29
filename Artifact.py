"""
@author Kevin Nguyen 2025
"""

"""
Artifact To-Do List:
--------------------
- When calling Artifact class, create random artifact roll
- To simplify the class, focus on crit value only 
- 5 slots: circlet, goblet, sands, flower, feather
- Artifact can start with 3 or 4 sub stats
- Can be leveled to a maximum of 20
- Possible crit rate rolls = [2.7, 3.1, 3.5, 3.9]
- Possible crit damage rolls = [5.4, 6.2, 7.0, 7,2]
- Sands: HP% = 26.68%, ATK% = 26.66%, DEF% = 26.66%, Energy Recharge% = 10%, Elemental Mastery = 10%
- Goblet of Eonothem:  HP% = 19.25%, ATK% = 19.25%, DEF% = 19%, ELE DMG bonus% = 5% * 8, Elemental Mastery = 2.5%
- Circlet of Logos: HP% = 22%, ATK% = 22%, DEF% = 22%, CRIT RATE% = 10%, CRIT DMG% = 10%, Healing Bonus% = 10%, Elemental Mastery = 4%
- Equal Chance to get any artifact, 20% each
- Possbile substats = Critical Rate, Critical Damage, Energy Recharge, Elemental Mastery, Attack Percentage, Flat Attack, HP Percentage, Flat HP
   ,Defense Percentage, Flat Defense
- Exp for lvl 4: 16,300
- Exp for lvl 8: 44,725
- Exp for lvl 16: 153,300
- Exp for lvl 20 max: 270,475
"""

import numpy as np
import math 

class Artifact:

    SLOTS = ['Circlet', 'Goblet', 'Sands', 'Feather', 'Flower']
    CIRCLET_MAIN = ['HP%', 'ATK%', 'DEF%', 'CRIT Rate%', 'CRIT DMG%', 'HB%', 'EM']
    CIRCLET_PROB = [0.22, 0.22, 0.22, 0.10, 0.10, 0.10, 0.04]
    GOBLET_MAIN = ['HP%', 'ATK%', 'DEF%', 'PyroDMG%', 'HydroDMG%', 'CryoDMG%', 'ElectroDMG%', 'GeoDMG%', 'AnemoDMG%', 'DendroDMG%', 'PhysicalDMG%', 'EM']
    GOBLET_PROB = [0.1925, 0.1925, 0.19, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.025]
    SANDS_MAIN = ['HP%', 'ATK%', 'DEF%', 'ER%', 'EM']
    SANDS_PROB = [0.2668, 0.2666, 0.2666, 0.10, 0.10]
    SUB_STATS_WEIGHTS = {'HP':6, 'HP%':4, 'DEF':6, 'DEF%':4, 'ATK':6, 'ATK%':4, 'ER%':4, 'EM':4, 'CRIT Rate%':3, 'CRIT DMG%':3}
    SUB_STATS_VALUES = {'HP':[209.12, 239.00, 268.88, 298.75], 
                        'HP%':[4.08,4.66,5.25,5.83], 
                        'DEF':[16.20, 18.52, 20.83, 23.15], 
                        'DEF%':[5.10,5.83,6.56,7.29], 
                        'ATK':[13.62, 15.56, 17.51, 19.45], 
                        'ATK%':[4.08,4.66,5.25,5.83], 
                        'ER%':[4.53, 5.18, 5.83, 6.48], 
                        'EM':[16.32, 18.65, 20.98, 23.31], 
                        'CRIT Rate%':[2.72, 3.11, 3.50, 3.89], 
                        'CRIT DMG%':[5.44, 6.22, 6.99, 7.77]}
    


    def __init__(self, slot=None, main_stat=None, sub_stats = {}, level=0, exp=0):

        if slot not in self.SLOTS:
            self.slot = np.random.choice(self.SLOTS)
        else: 
            self.slot = slot
        if self.slot == 'Circlet':
            if main_stat not in self.CIRCLET_MAIN:
                self.main_stat = np.random.choice(self.CIRCLET_MAIN, p=self.CIRCLET_PROB)
            else:
                self.main_stat = main_stat
        if self.slot == 'Goblet':
            if main_stat not in self.GOBLET_MAIN:
                self.main_stat = np.random.choice(self.GOBLET_MAIN, p=self.GOBLET_PROB)
            else:
                self.main_stat = main_stat
        if self.slot == 'Sands': 
            if main_stat not in self.SANDS_MAIN:
                self.main_stat = np.random.choice(self.SANDS_MAIN, p=self.SANDS_PROB)
            else:
                self.main_stat = main_stat
        if self.slot == 'Feather':
            self.main_stat = 'HP'
        if self.slot == 'Flower':
            self.main_stat = 'ATK'

        if not sub_stats:
            _sub_weights = self.SUB_STATS_WEIGHTS.copy()
            sub_stats_num = int(np.random.choice([3, 4], p=[0.8, 0.2]))
            
            if self.main_stat in _sub_weights: del _sub_weights[self.main_stat] 
            sub_stats = {}
            sub_weights = _sub_weights.copy()


            for _ in range(0, sub_stats_num):
                sub_stat_names = list(sub_weights.keys())
                sub_stat_weights = list(sub_weights.values())
                selected = np.random.choice(sub_stat_names, p=np.array(sub_stat_weights) / sum(sub_stat_weights))
                sub_stats[selected] = np.random.choice(self.SUB_STATS_VALUES[selected])
                del sub_weights[selected]

        self.sub_stats = sub_stats
        self.level = level
        enhancements = self.sub_stats.copy()
        enhancements.update(dict.fromkeys(enhancements, 0))
        self.enhancements = enhancements
        self.exp = exp

    def total_exp(self):
        """Returns all exp in artifact as integer"""
        if self.level == 4:
            self.exp = 16,300
        if self. level == 8:
            self.exp = 44,725
        if self.level == 12:
            self.exp = 87,150
        if self.level == 16:
            self.exp = 153,300
        if self.level == 20:
            self.exp = 270,475


    def level_up(self):
        """Levels up artifact to the next affix upgrade (factor of 4)"""
        if self.level == 20:
            return
        self.level += 4
        _sub_weights = self.SUB_STATS_WEIGHTS.copy()
        if self.main_stat in _sub_weights: del _sub_weights[self.main_stat]
        
        if len(self.sub_stats) == 3:
            for key in self.sub_stats:
                if key in _sub_weights: del _sub_weights[key]
            sub_stat_names = list(_sub_weights.keys())
            sub_stat_weights = list(_sub_weights.values())
            selected = np.random.choice(sub_stat_names, p=np.array(sub_stat_weights) / sum(sub_stat_weights))
            self.sub_stats[selected] = np.random.choice(self.SUB_STATS_VALUES[selected])
            enhancements = self.sub_stats.copy()
            enhancements.update(dict.fromkeys(enhancements, 0))
            self.enhancements = enhancements
            self.level += 4
            return
        selected = np.random.choice(list(self.sub_stats.keys()))
        value = np.random.choice(self.SUB_STATS_VALUES[selected]) + self.sub_stats[selected]
        self.sub_stats[selected] = round(value, 2) 
        self.enhancements[selected] += 1
        self.total_exp()
        return
    
    def level_up_max(self):
        """Levels artifact to level 20"""
        for _ in range(0, 6):
            self.level_up()
        return
    
    def crit_value(self):
        """Returns crit value integer"""
        crit_rate = self.sub_stats.get('CRIT Rate%', 0)
        crit_dmg = self.sub_stats.get('CRIT DMG%', 0)
        return round((crit_rate * 2) + crit_dmg, 2)
        
    def __repr__(self):
        """Unambiguous representation for debugging."""
        return (f"Artifact(slot='{self.slot}', main_stat='{self.main_stat}', "
            f"sub_stats={self.sub_stats}, level={self.level})")

    def __str__(self):
        """User-friendly display of the artifact."""
        # Format main stat
        main_stat_display = f"{self.main_stat}"
        
        # Format substats
        substat_lines = []
        for stat, value in self.sub_stats.items():
            enhance_string=''
            enhance_number = self.enhancements[stat]
            if enhance_number != 0:
                enhance_string = (f"+{enhance_number}")
            substat_lines.append(f"  ▪ {stat}: {value} {enhance_string}")
        
        # Combine everything
        return (
            f"══════════════════════════════\n"
            f"✦ {self.slot} (Lv. {self.level}) (exp total: {self.exp})\n"
            f"✦ Main: {main_stat_display}\n"
            f"✦ Substats:\n" + "\n".join(substat_lines) +
            f"\n══════════════════════════════"
        )

class Transmuter(Artifact):
    def __init__(self, slot, main_stat, affix1, affix2):
        super().__init__(slot=slot, main_stat=main_stat)
        
        _sub_weights = self.SUB_STATS_WEIGHTS.copy()
        sub_stats_num = int(np.random.choice([3, 4], p=[0.8, 0.2]))  
        if self.main_stat in _sub_weights: del _sub_weights[self.main_stat] 
        sub_stats = {}
        sub_weights = _sub_weights.copy()
        sub_stats[affix1] = np.random.choice(self.SUB_STATS_VALUES[affix1])
        sub_stats[affix2] = np.random.choice(self.SUB_STATS_VALUES[affix2])
        del sub_weights[affix1]
        del sub_weights[affix2]

        for _ in range(2, sub_stats_num):
            sub_stat_names = list(sub_weights.keys())
            sub_stat_weights = list(sub_weights.values())
            selected = np.random.choice(sub_stat_names, p=np.array(sub_stat_weights) / sum(sub_stat_weights))
            sub_stats[selected] = np.random.choice(self.SUB_STATS_VALUES[selected])
            del sub_weights[selected]

        self.sub_stats = sub_stats
        enhancements = self.sub_stats.copy()
        enhancements.update(dict.fromkeys(enhancements, 0))
        self.enhancements = enhancements
        self.affixes = [affix1, affix2]
        
        self.guaranteed = 2

    def upgrades_left(self):
        """Returns number of upgrades left as an integer (based on level)"""
        return 5 - self.level/4

    def level_up(self):
        """Levels up artifact to the next affix upgrade (factor of 4)"""
        
        # Check if there are upgrades left, return if none are left
        if not self.upgrades_left():
            return
        
        _sub_weights = self.SUB_STATS_WEIGHTS.copy()
        if self.main_stat in _sub_weights: del _sub_weights[self.main_stat]
        
        # Add a random sub stat for 3 affix artifacts.
        if len(self.sub_stats) == 3:
            for key in self.sub_stats:
                if key in _sub_weights: del _sub_weights[key]
            sub_stat_names = list(_sub_weights.keys())
            sub_stat_weights = list(_sub_weights.values())
            selected = np.random.choice(sub_stat_names, p=np.array(sub_stat_weights) / sum(sub_stat_weights))
            self.sub_stats[selected] = np.random.choice(self.SUB_STATS_VALUES[selected])
            enhancements = self.sub_stats.copy()
            enhancements.update(dict.fromkeys(enhancements, 0))
            self.enhancements = enhancements
            self.level += 4
            return
        
        # Guarantees 2 choosen affixes
        if (self.upgrades_left() <= 2) and (self.guaranteed > 0):
            selected = np.random.choice(self.affixes)
            self.affixes.remove(selected)
            value = np.random.choice(self.SUB_STATS_VALUES[selected]) + self.sub_stats[selected]
            self.sub_stats[selected] = round(value, 2) 
            self.enhancements[selected] += 1
            self.level += 4
            self.guaranteed -= 1
            self.total_exp()
            return

        selected = np.random.choice(list(self.sub_stats.keys()))
        value = np.random.choice(self.SUB_STATS_VALUES[selected]) + self.sub_stats[selected]
        self.sub_stats[selected] = round(value, 2) 
        self.enhancements[selected] += 1
        self.level += 4
        self.total_exp()
        return





        
        

        

    




