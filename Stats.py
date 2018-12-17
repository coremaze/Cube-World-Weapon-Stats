#Main ID enums
NONE = 0
USEABLE_ITEMS = 1
FORMULAS = 2
WEAPONS = 3
CHEST = 4
HANDS = 5
FEET = 6
SHOULDER = 7
NECK = 8
RING = 9
BLOCK = 10
ITEMS = 11
COINS = 12
ORES = 13
LEFTOVERS = 14
BEAK = 15
PAINTINGS = 16
VASE = 17
CANDLES = 18
PETS = 19
PETFOOD = 20
SPECIAL_ACCESSORIES = 21
SPECIALS = 23
LIGHT = 24
CUBES = 25

#Material ID enums
NONE = 0
IRON = 1
WOOD = 2
OBSIDIAN = 5
BONE = 7
COPPER = 10
GOLD = 11
SILVER = 12
EMERALD = 13
SAPPHIRE = 14
RUBY = 15
DIAMOND = 16
SANDSTONE = 17
SAURIAN = 18
PARROT = 19
MAMMOTH = 20
PLANT = 21
ICE1 = 22
LICHT = 23
GLASS = 24
SILK = 25
LINEN = 26
COTTON = 27
FIRE = 128
UNHOLY = 129
ICE2 = 130
WIND = 131

#Weapon ID enums
Sword = 0
Axe = 1
Mace = 2
Dagger = 3
Fist = 4
Longsword = 5
Bow = 6
Crossbow = 7
Boomerang = 8
Arrow = 9
Staff = 10
Wand = 11
Bracelet = 12
Shield = 13
Arrows = 14
Greatsword = 15
Greataxe = 16
Greatmace = 17
Fork = 18
Pickaxe = 19
Torch = 20

#Usable Items ID enums
Cookie = 0
LifePotion = 1
CactusPotion = 2
ManaPotion = 3
GinsengSoup = 4
SnowberryMash = 5
MushroomSpit = 6
Bomb = 7
PineappleSlice = 8
PumpkinMuffin = 9

def SomeCurve(n, m):
    x = 2 ** (((1.0 - (1.0 / (((n - 1.0) * 0.05) + 1.0))) * 3.0))
    y = 2 ** (m * 0.25)
    return x*y

def SomeCurve2(n, m):
    return SomeCurve(n, m) / 8

class Item:
    def __init__(self, mainID, subID, mod, attributes, material, number_of_spirits, level, rarity):
        self.mainID = mainID
        self.subID = subID
        self.mod = mod
        self.attributes = attributes
        self.material = material
        self.number_of_spirits = number_of_spirits
        self.level = level
        self.rarity = rarity

    #"Mod" and "Attribute" have previously been treated as separate variables, but really, they're the same variable.
    def ModAndAttributes(self):
        return (self.attributes << 16) + self.mod

    def PrintSummary(self):
        print(f'''Tempo: {(self.GetTempoStat()*100):.1f}%
HP: {self.GetHPStat():.1f}
RESI: {self.GetResiStat():.1f}
REG: {self.GetRegStat():.1f}
DMG: {self.GetDMGStat():.1f}
CRIT: {(self.GetCritStat()*100):.1f}%
ARMOR: {self.GetArmorStat():.1f}''')
    
    def GetHPStat(self):
        if self.mainID not in (WEAPONS, CHEST, SHOULDER, HANDS, FEET):
            return 0
        
        if self.mainID == CHEST:
            chest_multiplier = 1.0
        else:
            chest_multiplier = 0.5

        attribute_multiplier = (8 * self.ModAndAttributes() % 0x15) / 20
        material_multiplier = 2 - attribute_multiplier
        
        if self.material == IRON:
            material_multiplier += 1
        elif self.material == LINEN:
            material_multiplier += 0.5
        elif self.material == COTTON:
            material_multiplier += 0.75
            
        level_multiplier = SomeCurve(self.number_of_spirits * 0.1 + self.level, self.rarity)
        
        return level_multiplier * 5.0 * chest_multiplier * material_multiplier

    def GetTempoStat(self):
        if self.mainID not in (NECK, RING, WEAPONS, CHEST, SHOULDER, HANDS, FEET):
            return 0
        
        weaponType_multiplier = 0.1
        if self.mainID == WEAPONS:
            if self.subID in (Greatsword, Greataxe, Greatmace,
                              Longsword, Staff, Wand,
                              Fork, Boomerang, Bow,
                              Crossbow):
                weaponType_multiplier = 0.2
                
        elif self.mainID == CHEST:
            weaponType_multiplier = 0.2
                

        attribute_multiplier = (self.ModAndAttributes() % 0x15) / 20
        
        if self.material == SILVER:
            attribute_multiplier += 1

        level_multiplier = SomeCurve2(self.level, self.rarity)

        result = level_multiplier * weaponType_multiplier * attribute_multiplier
        
        if result < 0.001:
            return 0
        else:
            return result

    def GetResiStat(self):
        if self.mainID not in (CHEST, SHOULDER, HANDS, FEET):
            return 0
        chest_multiplier = 0.5
        if self.mainID == CHEST:
            chest_multiplier = 1

        if self.material in (IRON, PARROT):
            chest_multiplier *= 0.85
        elif self.material in (LINEN, COTTON):
            chest_multiplier *= 0.75

        return SomeCurve(self.number_of_spirits * 0.1 + self.level, self.rarity) * chest_multiplier

    def GetRegStat(self):
        if self.mainID not in (WEAPONS, CHEST, SHOULDER, HANDS, FEET):
            return 0
        
        if self.mainID == CHEST:
            chest_multiplier = 0.2
        else:
            chest_multiplier = 0.1

        attribute_multiplier = (8 * self.ModAndAttributes() % 0x15) / 20

        if self.material == LINEN:
            attribute_multiplier += 0.5
        elif self.material == COTTON:
            attribute_multiplier += 1

        level_multiplier = SomeCurve(self.number_of_spirits * 0.1 + self.level, self.rarity)
        return level_multiplier * chest_multiplier * attribute_multiplier

    def GetDMGStat(self):
        if self.mainID != WEAPONS:
            return 0
        spirit_multiplier = self.number_of_spirits * 0.1

        if self.subID in (Dagger, Fist):
            return SomeCurve(self.level + spirit_multiplier, self.rarity) * 2
        elif self.subID == Longsword:
            return SomeCurve(self.level + spirit_multiplier, self.rarity) * 4
        elif self.subID == Shield:
            return SomeCurve(self.level + spirit_multiplier, self.rarity) * 2
        elif self.subID in (Greatsword, Greataxe, Greatmace,
                            Longsword, Staff, Wand,
                            Fork, Boomerang, Bow,
                            Crossbow):
            return SomeCurve(self.level + spirit_multiplier, self.rarity) * 8
        else:
            return SomeCurve(self.level + spirit_multiplier, self.rarity) * 4
            
    def GetCritStat(self):
        if self.mainID not in (NECK, RING, WEAPONS, CHEST, SHOULDER, HANDS, FEET):
            return 0
        multiplier = 0.05
        if self.mainID == WEAPONS:
            if self.subID in (Greatsword, Greataxe, Greatmace,
                              Longsword, Staff, Wand,
                              Fork, Boomerang, Bow,
                              Crossbow):
                multiplier = 0.1
        elif self.mainID == CHEST:
            multiplier = 0.1

        attribute_multiplier =  attribute_multiplier = (self.ModAndAttributes() % 0x15) / 20
        material_multiplier = 1 - attribute_multiplier
        if self.material == GOLD:
            material_multiplier += 1
        level_multiplier = SomeCurve2(self.level, self.rarity)
        result = level_multiplier * multiplier * material_multiplier
        if result < 0.001:
            return 0
        else:
            return result

    def GetArmorStat(self):
        if self.mainID not in (CHEST, SHOULDER, HANDS, FEET):
            return 0

        if self.mainID == CHEST:
            multiplier = 1
        else:
            multiplier = 0.5

        if self.material == SAURIAN:
            multiplier *= 0.8
        elif self.material in (PARROT, LINEN, COTTON):
            multiplier *= 0.85
        elif self.material in (LICHT, SILK):
            multiplier *= 0.75
            
        return SomeCurve(self.number_of_spirits * 0.1 + self.level, self.rarity) * multiplier

    def GetHealingStat(self):
        if self.mainID != USEABLE_ITEMS:
            return 0

        if self.subID in (LifePotion, CactusPotion):
            return SomeCurve(self.level, self.rarity) * 200
        elif self.subID in (GinsengSoup, SnowberryMash, MushroomSpit):
            return SomeCurve(self.level, self.rarity) * 200
        elif self.subID in (PineappleSlice, PumpkinMuffin):
            return SomeCurve(self.level, self.rarity) * 100
        else:
            return 0


##item = Item(
##    mainID = WEAPONS,
##    subID = Greatmace,
##    mod = 5,
##    attributes = 9,
##    material = WOOD,
##    number_of_spirits = 0,
##    level = 33,
##    rarity = 7
##    )
##    
##item = Item(
##    mainID = HANDS,
##    subID = 0,
##    mod = 0,
##    attributes = 9,
##    material = PARROT,
##    number_of_spirits = 0,
##    level = 3,
##    rarity = 0
##    )
##
##item.PrintSummary()


#test
##from random import randint
##mainID = randint(0,11)
##subID = randint(0,20)
##mod = randint(0, 20)
##attributes = randint(0, 20)
##material = randint(0,27)
##level = randint(0, 200)
##rarity = randint(0, 7)
##print('\nTEST')
##print(f'main id {mainID}')
##print(f'sub id {subID}')
##print(f'mod {mod}')
##print(f'attributes {attributes}')
##print(f'material {material}')
##print(f'level {level}')
##print(f'rarity {rarity}\n')
##
##testitem = Item(
##    mainID = mainID,
##    subID = subID,
##    mod = mod,
##    attributes = attributes,
##    material = material,
##    number_of_spirits = 2,
##    level = level,
##    rarity = rarity
##    )
##testitem.PrintSummary()

##max_DMG = 0
##best_weapon = None
##for mod in range(0, 100):
##    for attributes in range(0, 25):
##        for material in range(0, 30):
##            for rarity in range(0, 5):
##                
##                item = Item(
##                    mainID = WEAPONS,
##                    subID = Greatmace,
##                    mod = mod,
##                    attributes = attributes,
##                    material = material,
##                    number_of_spirits = 0,
##                    level = 3,
##                    rarity = rarity
##                    )
##                dmg = item.GetCritStat()
##                if dmg > max_DMG:
##                    max_DMG = dmg
##                    best_weapon = item
##
##                
##
##best_weapon.PrintSummary()


##item = Item(
##    mainID = USEABLE_ITEMS,
##    subID = LifePotion,
##    mod = 0,
##    attributes = 0,
##    material = 0,
##    number_of_spirits = 0,
##    level = 3,
##    rarity = 0
##    )
##
##print(item.GetHealingStat())       

