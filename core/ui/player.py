import math
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.image import Image

from .theme import Theme

__all__ = (
    "Player",
)


class Player(Image, Theme):

    """
        ACCEL_X = 5 / FPS
        ACCEL_Y = 5 / FPS

        MAX_SPEED_X = 1.5 / FPS
        MAX_SPEED_Y = 2 / FPS

        MIN_SPEED_X = 0.01
        MIN_SPEED_Y = 0.01

        SPEED_ATT_X = 0.80
    """

    accel_x = NumericProperty(0)
    accel_y = NumericProperty(0)

    speed_x = NumericProperty(0)
    speed_y = NumericProperty(0)

    ipos_x = NumericProperty(0)
    ipos_y = NumericProperty(0)

    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)

    physic_running = BooleanProperty(True)

    move_right = BooleanProperty(False)
    move_left = BooleanProperty(False)
    jump = BooleanProperty(False)

    factor = NumericProperty(0)

    PLAYER_SIZE = 1.5
    DEADZONE_X = .2 * PLAYER_SIZE
    DEADZONE_Y = .15 * PLAYER_SIZE

    # idle, walk, jump, fall
    state = StringProperty("idle")

    flip_horizontal = BooleanProperty(False)
    flip_vertical = BooleanProperty(False)

    gamefield = ObjectProperty(None)

    def __init__(self, **kwargs):
        src = f"{self.theme}/player.gif"
        super().__init__(source=src, **kwargs)

    def on_kv_post(self, base_widget):
        self.pos_x = self.ipos_x
        self.render()

    def on_factor(self, instance, value):
        self.size = (self.factor * 1.5, self.factor * 1.5)
        self.render()

    def on_ipos_x(self, instance, value):
        self.pos_x = self.ipos_x
        self.render()

    def on_ipos_y(self, instance, value):
        self.pos_y = self.ipos_y
        self.render()

    def render(self):
        self.x = self.factor * self.ipos_x
        self.y = self.factor * self.pos_y

    def on_pos_y(self, instance, value):
        self.y = self.factor * self.pos_y


    def move(self, dx, dy) -> bool:
        if dx == dy == 0: return True

        if dx != 0 and dy != 0:
            return self.move(dx, 0) and self.move(0, dy)

        game = self.gamefield

        hitbox_x = self.PLAYER_SIZE - 2 * self.DEADZONE_X
        hitbox_y = self.PLAYER_SIZE - self.DEADZONE_Y

        src_x = self.pos_x + self.DEADZONE_X
        src_y = self.pos_y

        dest_x = src_x + dx
        dest_y = src_y + dy

        grid_size_x = game.grid_size_x()
        grid_size_y = game.grid_size_y()

        x_min = max(math.floor(dest_x), 0)
        y_min = max(math.floor(dest_y), 0)

        x_max = min(math.ceil(dest_x + hitbox_x), grid_size_x)
        y_max = min(math.ceil(dest_y + hitbox_y), grid_size_y)

        block_hitbox_x = 1
        block_hitbox_y = 1

        collision_ok = True

        for block_x in range(x_min, x_max):
            for block_y in range(y_min, y_max):

                block = game.get_block(block_x, block_y)
                is_solid = game.is_wall(block)
                if not is_solid: continue

                # x
                if dx != 0:
                    if dx > 0:
                        if dest_x + hitbox_x > block_x:
                            dest_x = block_x - hitbox_x
                            collision_ok = False
                            game.trigger_block(block_x, block_y)

                    else:
                        if dest_x < block_x + block_hitbox_x:
                            dest_x = block_x + block_hitbox_x
                            collision_ok = False
                            game.trigger_block(block_x, block_y)

                # y
                if dy != 0:
                    if dy > 0:
                        if dest_y + hitbox_y > block_y:
                            dest_y = block_y - hitbox_y
                            collision_ok = False
                            game.trigger_block(block_x, block_y)
                    else:
                        if dest_y < block_y + block_hitbox_y:
                            dest_y = block_y + block_hitbox_y
                            collision_ok = False
                            game.trigger_block(block_x, block_y)

        self.pos_x += dest_x - src_x
        self.pos_y += dest_y - src_y

        return collision_ok


    def set_state(self, state):
        if self.state == state: return
        self.state = state
        self.update_animation()

    def on_flip_horizontal(self, instance, value):
        self.update_animation()

    def on_flip_vertical(self, instance, value):
        self.update_animation()

    def update(self, dt):
        #self.move(0.01, 0)
        #self.move(0, 0.001)

        if not self.physic_running: return

        speed_add = 1/30.

        if self.move_right:
            self.speed_x += speed_add
            #self.accel_x =  self.ACCEL_X
        elif self.move_left:
            self.speed_x -= speed_add
            #self.accel_x = -self.ACCEL_X
        #else:
            #self.accel_x = 0

        gravity = -1/30.
        self.speed_y += gravity
        self.speed_y *= 0.8

        on_ground = False

        if not self.move(0, self.speed_y):
            if self.speed_y < 0:
                on_ground = True
                self.speed_y = 0

        jump_add = 25/30.
        if on_ground and self.jump:
            self.speed_y += jump_add




        #self.speed_x += self.accel_x
        #self.speed_y += self.accel_y
        self.speed_x *= 0.8
        if not self.move(self.speed_x, 0):
            self.speed_x = 0

        if on_ground:
            if abs(self.speed_x) <= 0.001:
                self.speed_x = 0
                self.set_state("idle")
                # idle animation
            else:
                self.set_state("walk")
                self.flip_horizontal = self.speed_x < 0
        else:
            #self.flip_horizontal = self.speed_x < 0
            self.set_state("jump")
            



        #if self.jump:
        #    self.move(0, s)


        """
        if self.physic_running:

            if self.move_right:
                self.accel_x = self.ACCEL_X
            elif self.move_left:
                self.accel_x = -self.ACCEL_X
            else:
                self.accel_x = 0

            if self.jump:
                self.accel_y = self.ACCEL_Y
            else:
                self.accel_y = -.5

            sx = self.speed_x + self.accel_x
            sy = self.speed_y + self.accel_y

            sx = max(-self.MAX_SPEED_X, min(self.MAX_SPEED_X, sx)) * self.SPEED_ATT_X
            sy = max(-self.MAX_SPEED_Y, min(self.MAX_SPEED_Y, sy)) * self.SPEED_ATT_X

            if abs(sx) < self.MIN_SPEED_X:
                sx = 0

            if abs(sy) < self.MIN_SPEED_Y:
                sy = 0

            px = self.pos_x
            py = self.pos_y

            src_left_limit = px + self.DEADZONE_X
            src_right_limit = px + 1 - self.DEADZONE_X
            src_bottom_limit = py
            src_top_limit = py + 1 - self.DEADZONE_Y

            dst_left_limit = src_left_limit + sx
            dst_right_limit = src_right_limit + sx
            dst_bottom_limit = src_bottom_limit + sy
            dst_top_limit = src_top_limit + sy

            if self.gamefield and (lmap := self.gamefield.map):
                R_valid = True
                L_valid = True
                T_valid = True
                B_valid = True

                if dst_left_limit < 0:  # left limit, move the player at visual x=0
                    sx = -src_left_limit
                    L_valid = False
                elif dst_right_limit >= len(lmap[0]):
                    sx = len(lmap[0]) - src_right_limit
                    R_valid = False

                if dst_top_limit < 0:  # low limit, fall
                    T_valid = False
                elif dst_bottom_limit >= len(lmap):
                    B_valid = False

                if L_valid:
                    if T_valid:
                        block = lmap[int(dst_top_limit)][int(dst_left_limit)]
                        if self.gamefield.is_wall(block):
                            if int(dst_left_limit) != int(src_left_limit) or int(dst_top_limit) != int(src_top_limit):
                                if sx <= 0: sx = 0  # int(dst_left_limit) - dst_left_limit
                                if sy > 0: sy = 0  # dst_top_limit - int(dst_top_limit)

                    if B_valid:
                        block = lmap[int(dst_bottom_limit)][int(dst_left_limit)]
                        if self.gamefield.is_wall(block):
                            if int(dst_left_limit) != int(src_left_limit) or int(dst_bottom_limit) != int(src_bottom_limit):
                                if sx <= 0: sx = 0  # int(dst_left_limit) - dst_left_limit
                                if sy <= 0: sy = 0  # int(dst_bottom_limit) - dst_bottom_limit

                if R_valid:
                    if T_valid:
                        block = lmap[int(dst_top_limit)][int(dst_right_limit)]
                        if self.gamefield.is_wall(block):
                            if int(dst_right_limit) != int(src_right_limit) or int(dst_top_limit) != int(src_top_limit):
                                if sx > 0:  sx = 0  # dst_right_limit - int(dst_right_limit)
                                if sy > 0: sy = 0  # sy = dst_top_limit - int(dst_top_limit)

                    if B_valid:
                        block = lmap[int(dst_bottom_limit)][int(dst_right_limit)]
                        if self.gamefield.is_wall(block):
                            if int(dst_right_limit) != int(src_right_limit) or int(dst_bottom_limit) != int(src_bottom_limit):
                                if sx > 0: sx = 0  # dst_right_limit - int(dst_right_limit)
                                if sy <= 0: sy = 0  # int(dst_bottom_limit) - dst_bottom_limit

            self.speed_x = sx
            self.speed_y = sy

            self.pos_x += sx
            self.pos_y += sy

            self.accel_x = 0
            self.accel_y = 0
            """

    def on_theme(self, instance, value):
        super().on_theme(instance, value)
        #self.change_animation(self.source.split("/", 1)[-1])
        self.update_animation()

    def update_animation(self):
        self.source = f"{self.theme}/player_{self.state}{"_left" if self.flip_horizontal else ""}.gif"
        self.anim_loop = 0
        if self.state == "walk":
            self.anim_delay = 0.07
        elif self.state == "idle":
            self.anim_delay = 0.5
        elif self.state == "jump":
            self.anim_delay = 0.08
            self.anim_loop = 1


    def on_texture(self, instance, value):
        self.config_texture(False)

    def on_size(self, instance, value):
        self.config_texture()

    def config_texture(self, tex: bool = True):
        self.texture: Texture

        if not self.texture:
            return

        self.texture.min_filter = 'nearest'
        self.texture.mag_filter = 'nearest'



