"""
@author Kevin Nguyen 2025
"""

def crit_value(crit_rate, crit_dmg):
    """Returns crit value integer"""
    return (crit_rate * 2) + crit_dmg

# Run Tests
print(crit_value(10, 20))


