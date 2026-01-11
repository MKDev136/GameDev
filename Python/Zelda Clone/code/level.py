import pygame
from tile import Tile
from player import Player
from YSortCameraGroup import YSortCameraGroup
from support import import_csv_layout
from settings import TILESIZE

class Level:
    def __init__(self):
        # Display surface
        self.display = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Map layouts
        self.layouts = {
            'boundary': import_csv_layout("map/ZEDLA._Collisions.csv"),
            'ennemies': import_csv_layout("map/ZEDLA._Ennemies.csv"),
            'houses': import_csv_layout("map/ZEDLA._Houses.csv"),
            'npc': import_csv_layout("map/ZEDLA._NPC.csv"),
            'objects': import_csv_layout("map/ZEDLA._Objects.csv"),
            'player': import_csv_layout("map/ZEDLA._Player.csv"),
            'terrain': import_csv_layout("map/ZEDLA._Terrain.csv"),
        }

        # Create all map elements
        self.create_map()

    def create_map(self):
        for style, layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == "boundary":
                            Tile(
                                (x, y),
                                [self.obstacle_sprites],
                                "collision",
                                pygame.Surface((TILESIZE, TILESIZE)) 
                            ).image.fill((100, 100, 100))  # gray

                        elif style == "houses":
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "house",
                                pygame.image.load('./graphics/objects/05.png')
                            ).image.fill((200, 150, 50))  # brown

                        elif style == "objects":
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                pygame.image.load('./graphics/objects/01.png') 
                            ).image.fill((150, 50, 50))  # red

                        elif style == "npc":
                            Tile(
                                (x, y),
                                [self.visible_sprites],
                                "npc",
                                pygame.image.load('./graphics/monsters/raccoon/idle/0.png')
                            ).image.fill((50, 50, 200))  # blue

                        elif style == "ennemies":
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "enemy",
                                pygame.image.load('./graphics/monsters/bamboo/idle/0.png') 
                            )

                        elif style == "player":
                            # Spawn player
                            self.player = Player((x, y), [self.visible_sprites])

    def run(self):
        # Update and draw
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
