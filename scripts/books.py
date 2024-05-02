import pygame as pg
import random

BOOK_COORDS_LIST = [(1359,640), (368, 1152), (53, 1152), (196, 1836), (686,1718), 
                    (2101,1712), (1883, 1456), (2560,1657), (3436, 1858), 
                    (3152, 1398),(3395,830), (2848,768), (2825,552), (2436,512), (2800,284)]

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

    def update(self, player_rect):
        for book in self.books:
            if player_rect.colliderect(book.rect):
                book_index = self.book_coords.index(book.rect.center)
                if not self.collected_books[book_index]:
                    self.collected_books[book_index] = True
                    self.total_collected_books += 1
                    book.kill()

    def draw(self, screen, offset):
        for book in self.books:
            adjusted_rect = book.rect.move(-offset[0], -offset[1])
            screen.blit(book.image, adjusted_rect)

    def reset(self):
        self.books.empty()
        self.total_collected_books = 0
        books_to_spawn = 8
        self.collected_books = [False] * len(self.book_coords)
        self.book_coords = random.sample(BOOK_COORDS_LIST, books_to_spawn)
        for coords in self.book_coords:
            self.books.add(Book(coords))

    # returns true if all books are collected
    def all_books_collected(self):
        return all(self.collected_books)
