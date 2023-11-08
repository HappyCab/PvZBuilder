import pygame
import os

TITLE = "PvZ Builder"
TILES_HORIZONTAL = 9
TILES_VERTICAL = 6
TILESIZE = 128
WINDOW_WIDTH = TILESIZE * TILES_HORIZONTAL
WINDOW_HEIGHT = TILESIZE * TILES_VERTICAL

class Tiles:
    def __init__(self, screen):
        self.screen = screen
        self.inner = []
        self.current_tile = None
        self._load_data()

    def _load_data(self):
        self.inner = []
        filepath = os.path.join("data", "lawn.txt")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        id = 0
        for count_i, myline in enumerate(mylines):
            temp_list = myline.split(";")
            temp_list = [i.strip() for i in temp_list if len(i.strip()) > 0]
            for count_j, elem in enumerate(temp_list):
                new_tile = Tile(id, count_j, count_i, elem)
                self.inner.append(new_tile)
                id+= 1

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("Error! No tiles to display")
        for elem in self.inner:
            self.screen.blit(elem.image, elem.rect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()
        

class Tile:
    def __init__(self, id, x, y, tileType):
        self.id = id
        self.x, self.y = int(x), int(y)
        self.tileType = tileType

        match tileType:
            case "g":
                if (self.x + self.y) % 2 == 0: filename = "grass01.png"
                else: filename = "grass02.png"
                
            case "w":
                if (self.x + self.y) % 2 == 0: filename = "water01.png"
                else: filename = "water02.png"
            case _:
                raise ValueError("Error! Tile Type: ", tileType)

        self.rect = pygame.Rect(self.x * TILESIZE, self.y * TILESIZE, TILESIZE, TILESIZE)
        image_path = os.path.join("data", "images", "tiles")
        self.image = pygame.image.load(os.path.join(image_path, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

    def debug_print(self):
        s = "id: {}, x: {}, y: {}, kind {}".format(self.id, self.x, self.y, self.tileType)
        print(s)

class Plant:
    def __init__(self, id, x, y, plantType):
        self.id = id
        self.x, self.y = int(x), int(y)
        self.myinc = .05
        self.plant_image = ""
        match plantType:
            case "m":
                self.plant_image = "melonpult.png"                
            case "w":
                self.plant_image = "winterpult.png"                
            case "g":
                self.plant_image = "gloomshroom.png"              
            case "c1":
                self.plant_image = "cannon1.png"              
            case "c2":
                self.plant_image = "cannon2.png"              
            case "u":
                self.plant_image = "umbrella.png"               
            case "s":
                self.plant_image = "spikerock.png"
            case _:
                s = "Sorry I don't recognize that: {}".format(plantType)
                raise ValueError(s)

        image_path = os.path.join("data", "images", "plants")
        self.image = pygame.image.load(os.path.join(image_path, self.plant_image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

    def debug_print(self):
        s = "id: {}, x: {}, y: {}".format(self.id, self.x, self.y)
        print(s)
        
        
class Plants:
    def __init__(self, surface):
        self.surface = surface
        self.inner = []
        self.current_plant = None

        id = 0
        filepath = os.path.join("data", "plant_map.txt")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        for count_i, line in enumerate(mylines):
            for count_j, elem in enumerate(line):
                if elem == "m":
                    new_plant = Plant(id, count_j, count_i, elem)
                    self.inner.append(new_plant)
                    id += 1

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("Error: There are no plants to display")
        for elem in self.inner:
            myrect = pygame.Rect(elem.x *TILESIZE, elem.y * TILESIZE, TILESIZE, TILESIZE)
            self.surface.blit(elem.image, myrect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(TITLE)
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.BG_COLOUR = (100, 255, 100)
        self.keep_looping = True

        self.tiles = Tiles(self.surface)
        self.plants = Plants(self.surface)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False

    def update(self):
        pass

    def draw(self):
        self.surface.fill(self.BG_COLOUR)
        self.tiles.draw(self.surface)
        self.plants.draw(self.surface)
        pygame.display.update()

    def main(self):
        while self.keep_looping:
            self.events()
            self.update()
            self.draw()

if __name__ == "__main__":
    mygame = Game()
    mygame.main()
