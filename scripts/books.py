import pygame as pg
import random

BOOK_COORDS_LIST = [(1359,640), (368, 1152), (53, 1152), (187, 1856), (690,1728), 
                    (2101,1712), (1883, 1456), (2560,1657), (3438, 1872), 
                    (3150, 1408),(3384,848), (2848,768), (2825,552), (2436,512), (2800,284)]

class Book(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.image.load("assets/Collectables/book.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)

class BookManager:
    def __init__(self, num_books):
        self.book_coords = random.sample(BOOK_COORDS_LIST, num_books)
        self.books = pg.sprite.Group()
        self.collected_books = [False] * num_books
        self.total_collected_books = 0

        for coord in self.book_coords:
            self.books.add(Book(coord))

    def update(self, player_rect, offset):
        for i, book in enumerate(self.books):
            if not self.collected_books[i]:
                adjusted_book_rect = book.rect.move(-offset[0], -offset[1])
                if player_rect.colliderect(adjusted_book_rect):
                    self.collected_books[i] = True
                    self.total_collected_books += 1
                    book.kill()

    def draw(self, screen, offset):
        for book in self.books:
            adjusted_rect = book.rect.move(-offset[0], -offset[1])
            screen.blit(book.image, adjusted_rect)
