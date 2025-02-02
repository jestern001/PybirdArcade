from dataclasses import dataclass
from pathlib import Path
import arcade
import arcade.key


player_path = Path("resources/player.png")
block_path = Path('resources/block.png')
MOVE_SPEED = 5
JUMP_SPEED = 10
GRID_SIZE = 32


class App(arcade.Window):
    def __init__(self, *args, **kwargs):
        self.view
        self.inputs = {}
        self.scene = arcade.Scene()

        super().__init__(*args, **kwargs)
        self.background_color = arcade.color.CORNFLOWER_BLUE

        # add dynamics
        self.dynamics = arcade.SpriteList()

        player = arcade.Sprite(player_path)
        player.center_x = self.width // 2
        player.center_y = self.height // 2
        self.player = player
        self.scene.add_sprite("player", player)
        
        # add statics
        platforms = arcade.SpriteList(use_spatial_hash=True)
        self.scene.add_sprite_list("platforms", platforms)

        # add floor
        for i in range(self.width//GRID_SIZE):
            wall = arcade.Sprite(block_path)
            wall.center_x = wall.width//2 + (i * GRID_SIZE)
            wall.center_y = wall.width//2
            self.scene.add_sprite('platforms', wall)

        self.physics = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.scene.get_sprite_list('platforms'),
        )
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.inputs['left'] = True

        if symbol == arcade.key.RIGHT:
            self.inputs['right'] = True
        
        if symbol == arcade.key.SPACE:
            self.inputs['space'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.inputs['left'] = False

        if symbol == arcade.key.RIGHT:
            self.inputs['right'] = False
        
        if symbol == arcade.key.SPACE:
            self.inputs['space'] = False

    
    def on_update(self, time_delta):

        # handle event change inputs
        pressed = lambda key: self.inputs.get(key) and not self.previous_inputs.get(key)
        self.inputs['space_pressed'] = pressed('space')
        self.previous_inputs = self.inputs.copy() 

        # if left or right, but not both are pressed
        if bool(self.inputs.get('left')) ^ bool(self.inputs.get('right')):
            if self.inputs.get('left') and not self.inputs.get('right'):
                    self.player.change_x = -MOVE_SPEED
            if self.inputs.get('right') and not self.inputs.get('left'):
                    self.player.change_x = MOVE_SPEED
        else:
            self.player.change_x = 0

        # check jump
        if self.inputs.get('space_pressed'):
            if self.physics.can_jump():
                self.player.change_y = JUMP_SPEED
        
        # stay in room
        if self.player.center_x < 0:
            self.player.center_x = 0
        if self.player.center_x > self.width:
            self.player.center_x = self.width

        # handle physics
        self.physics.update()

    def on_draw(self):
        self.clear()
        self.scene.draw()


if __name__ == "__main__":
    app = App(height=480, width=640)
    app.run()
