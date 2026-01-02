from settings import *

def get_status(self):
    # idle status
    if self.direction.x == 0 and self.direction.y == 0:
        if not 'idle' in self.status and not 'attack' in self.status:
            self.status = self.status + '_idle'

    if self.attacking:
        self.direction.x = 0
        self.direction.y = 0
        if not 'attack' in self.status:
            if 'idle' in self.status:
                self.status = self.status.replace('_idle','_attack')
            else:
                self.status = self.status + '_attack'
    else:
        if 'attack' in self.status:
            self.status = self.status.replace('_attack','')


def get_full_weapon_damage(self):
    base_damage = self.stats['attack']
    weapon_damage = weapon_data[self.weapon]['damage']
    return base_damage + weapon_damage

def get_full_magic_damage(self):
    base_damage = self.stats['magic']
    spell_damage = magic_data[self.magic]['strength']
    return base_damage + spell_damage

def get_value_by_index(self,index):
    return list(self.stats.values())[index]

def get_cost_by_index(self,index):
    return list(self.upgrade_cost.values())[index]