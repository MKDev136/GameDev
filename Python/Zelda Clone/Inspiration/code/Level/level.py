import pygame 
from settings import *
from Graphics.tile import Tile
from Entities.Player.player import Player
from debug import debug
from support import *
from random import choice, randint
from Attacks.Weapon.weapon import Weapon
from Graphics.ui import UI
from Entities.Enemy.enemy import Enemy
from Graphics.particles import AnimationPlayer
from Attacks.Magic.magic import MagicPlayer
from Attacks.Upgrade.upgrade import Upgrade

from Level.YSort.YSortCameraGroup import YSortCameraGroup

class Level:
    def __init__(self):

        # get the display surface 
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        self.timer = pygame.time.get_ticks()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        
        self.layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv'),
            'entities': import_csv_layout('./map/map_Entities.csv')
        }
        self.graphics = {
            'grass': import_folder('./graphics/Grass'),
            'objects': import_folder('./graphics/objects')
        }

        # sprite setup
        self.create_map()

        # user interface 
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):

        for style,layout in self.layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(self.graphics['grass'])
                            Tile(
                                (x,y),
                                [self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
                                'grass',
                                random_grass_image)
                        if style == 'object':
                            surf = self.graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name ='raccoon'
                                else: monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.topleft
                            offset = pygame.math.Vector2(0,75)
                            
                            # particles
                            for _ in range(randint(3,6)):
                                self.animation_player.create_grass_particles(target_sprite.rect.center - offset, [self.visible_sprites])
                            
                            # remove old grass
                            target_sprite.kill()
                            
                            # spawn new grass immediately
                            # random_grass_image = choice(self.graphics['grass'])
                            rupees = Tile(
                                pos,
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'details',  # becomes a "details" tile for EXP
                                pygame.image.load("./graphics/tilemap/exp.png")
                            )
                            # store hit time for delayed EXP
                            rupees.hit_time = pygame.time.get_ticks()
                            rupees.exp_given = False
                            
                        elif target_sprite.sprite_type == "details":
                            if hasattr(target_sprite, "hit_time") and not target_sprite.exp_given:
                                current_time = pygame.time.get_ticks()
                                if current_time - target_sprite.hit_time >= 1000:  # 1 second delay
                                    self.player.exp += 1000
                                    target_sprite.exp_given = True
                                    target_sprite.kill()  # remove after giving EXP
                            
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def add_exp(self,amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused 

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()