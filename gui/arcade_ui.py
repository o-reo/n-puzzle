# -*- coding: utf-8 -*-
import arcade
import numpy as np
from PIL import Image, ImageFont, ImageDraw

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_MARGIN = 50

SPRITE_SIZE = 256
PIECE_SPACE = 1

class PuzzleInterface(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, 'n-puzzle solver')
        arcade.set_background_color(arcade.csscolor.GREY)
        self.board = np.array([])
        self.size = 0
        self.moves = []
        self.puzzle = []
        self.piece_size = 0
        self.slowing = 20
        self.iter = 0
        self.speed = 15
        self.pause = True

    def setup(self, solver, solution, image = None):
        # init values
        self.solver = solver
        self.size = solver._size
        self.puzzle = solver._puzzle.copy()
        self.moves = solution[0][1]
        self.pieces = arcade.SpriteList()
        self.labels = []
        self.image = image
        self.piece_size = int((WINDOW_WIDTH - 2 * WINDOW_MARGIN) / self.size)
        self._generate_sprites()
        self._init_pieces()

    def _generate_sprites(self):
        if not self.image:
            for i in range(1, self.size ** 2):
                img = Image.open("gui/assets/square.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("gui/assets/font.ttf", 128)
                draw.text((int(SPRITE_SIZE / 2) - 20 * (1 + int(i / 10)), int(SPRITE_SIZE / 2) - 64), "{}".format(i), (255, 255, 255), font=font)
                img.save('gui/assets/p_{}.png'.format(i))
                piece = arcade.Sprite('gui/assets/p_{}.png'.format(i), self.piece_size / SPRITE_SIZE)
                self.pieces.append(piece)
        else:
            img = Image.open(self.image)
            image_width = WINDOW_WIDTH - 2 * WINDOW_MARGIN if img.height > img.width else img.width / img.height * (WINDOW_HEIGHT - 2 * WINDOW_MARGIN)
            image_height = img.height / img.width * (WINDOW_WIDTH - 2 * WINDOW_MARGIN) if img.height > img.width else WINDOW_HEIGHT - 2 * WINDOW_MARGIN
            img = img.resize((int(image_width), int(image_height)))
            for i in range(1, self.size ** 2):
                wsx, wsy = map(lambda x: x[0], np.where(self.solver._solution == i))
                crop = img.crop((wsy * self.piece_size, wsx * self.piece_size, (wsy + 1) * self.piece_size, (wsx + 1) * self.piece_size))
                crop.save('gui/assets/p_{}.png'.format(i))
                piece = arcade.Sprite('gui/assets/p_{}.png'.format(i), 1)
                self.pieces.append(piece)

    def _init_pieces(self):
        it = np.nditer(self.puzzle, flags=['multi_index'])
        while not it.finished:
            if (self.puzzle[it.multi_index] == 0):
                it.iternext()
                continue
            w_coords = self._draw_coordinates(it.multi_index)
            piece = self.pieces[self.puzzle[it.multi_index] - 1]
            piece.center_x = w_coords[0]
            piece.center_y = w_coords[1]
            piece.color = arcade.color.LIGHT_STEEL_BLUE if self.image else arcade.color.WHITE
            it.iternext()

    def _update_pieces(self, delta_time):
        it = np.nditer(self.puzzle, flags=['multi_index'])
        while not it.finished:
            if (self.puzzle[it.multi_index] == 0):
                it.iternext()
                continue
            w_coords = self._draw_coordinates(it.multi_index)
            piece = self.pieces[self.puzzle[it.multi_index] - 1]
            if self.puzzle[it.multi_index] == self.solver._solution[it.multi_index]:
                piece.color = arcade.color.WHITE if self.image else arcade.color.ROYAL_BLUE
            else:
                piece.color = arcade.color.LIGHT_STEEL_BLUE if self.image else arcade.color.WHITE   
            if piece.center_x != w_coords[0]:
                piece.change_x = min(abs(piece.center_x - w_coords[0]), self.speed) * (2 * (piece.center_x < w_coords[0]) - 1)
                return
            elif piece.center_y != w_coords[1]:
                piece.change_y = min(abs(piece.center_y - w_coords[1]), self.speed) * (2 * (piece.center_y < w_coords[1]) - 1)
                return
            piece.change_x = 0
            piece.change_y = 0
            it.iternext()
        if (self.iter >= len(self.moves)):
            return
        self._slide(self.moves[int(self.iter)])
        self.iter += 1


    def _slide(self, direction):
        wx, wy = map(lambda x: x[0], np.where(self.puzzle == 0))
        if direction == 0:
            self.puzzle[wx, wy], self.puzzle[wx,
                                 wy - 1] = self.puzzle[wx, wy - 1], self.puzzle[wx, wy]
        if direction == 1:
            self.puzzle[wx, wy], self.puzzle[wx - 1,
                                 wy] = self.puzzle[wx - 1, wy], self.puzzle[wx, wy]
        if direction == 2:
            self.puzzle[wx, wy], self.puzzle[wx,
                                 wy + 1] = self.puzzle[wx, wy + 1], self.puzzle[wx, wy]
        if direction == 3:
            self.puzzle[wx, wy], self.puzzle[wx + 1,
                                 wy] = self.puzzle[wx + 1, wy], self.puzzle[wx, wy]
    
    def _draw_coordinates(self, coords):
        return (WINDOW_MARGIN + coords[1] * self.piece_size + int(
                self.piece_size / 2), WINDOW_HEIGHT - (WINDOW_MARGIN + coords[0] * self.piece_size + int(self.piece_size / 2)))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT and self.speed > 5:
            self.speed -= 5
        if key == arcade.key.RIGHT:
            self.speed += 5
        if key == arcade.key.SPACE:
            self.pause = not self.pause
        if key == arcade.key.R:
            self.pause = True
            self.puzzle = self.solver._puzzle.copy()
            self.iter = 0
            self._init_pieces()
        if key == arcade.key.ESCAPE:
            arcade.close_window()
    
    def update(self, delta_time):
        if self.pause:
            return
        self._update_pieces(delta_time)
        self.pieces.update()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.pieces.draw()
