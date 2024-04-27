"""
Platformer Game
"""
import arcade
import pyglet

# Constants
WINDOW_WIDTH = 1700
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Hollow knight"
BACKGROUND_HEX_COLOR = '#222222'
WORLD_WIDTH = WINDOW_WIDTH * 3
GRAVITY = 0.75

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.75
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
# Jump speed of player, in pixels per frame
PLAYER_JUMP_SPEED = 15


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                         title=WINDOW_TITLE, antialiasing=True)

        # Our Scene Object
        self.scene = None

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        arcade.set_background_color(
            arcade.color_from_hex_string(BACKGROUND_HEX_COLOR))

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "assets/The_Knight_Front.webp"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the ground
        for x in range(0, WORLD_WIDTH, 64):
            stone = arcade.Sprite(
                ":resources:images/tiles/stoneMid.png", TILE_SCALING)
            stone.left = x
            stone.bottom = 0
            self.scene.add_sprite("Walls", stone)

        # Create the roof
        for x in range(0, WORLD_WIDTH, 64):
            stone_center = arcade.Sprite(
                ":resources:images/tiles/stoneCenter.png", TILE_SCALING, flipped_vertically=True)
            stone_center.left = x
            stone_center.top = WINDOW_HEIGHT

            stone = arcade.Sprite(
                ":resources:images/tiles/stoneMid.png", TILE_SCALING, flipped_vertically=True)
            stone.left = x
            stone.top = WINDOW_HEIGHT - stone_center.height

            self.scene.add_sprite("Walls", stone_center)
            self.scene.add_sprite("Walls", stone)

        # Put some spikeS on the ground
        coordinate_list = [[256, 96], [768, 96], [1024, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            spike = arcade.Sprite(
                ":resources:images/tiles/spikes.png", TILE_SCALING
            )
            spike.position = coordinate
            self.scene.add_sprite("Walls", spike)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            walls=self.scene["Walls"],
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


if __name__ == "__main__":
    window = MyGame()
    icon = pyglet.image.load('assets/icon-64.png')
    window.set_icon(icon)
    window.setup()
    arcade.run()
