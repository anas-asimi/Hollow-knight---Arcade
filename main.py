"""
Hollow knight Game
"""
import arcade
import pyglet

# Constants
WINDOW_WIDTH = 1664  # 128 * 13
WINDOW_HEIGHT = 896  # 128 * 7
WINDOW_TITLE = "Hollow knight"
WORLD_WIDTH = WINDOW_WIDTH * 3
GRAVITY = 1.5

# Constants used to scale our tiles from their original size
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7

# Jump speed of player, in pixels per frame
PLAYER_JUMP_SPEED = 21

# Player start position
PLAYER_START_X = 128
PLAYER_START_Y = 256

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    # path to the caracter image
    idle_texture_path = 'assets/The_Knight_Idle.webp'

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Load textures for idle standing
        self.idle_texture_pair = [
            arcade.load_texture(self.idle_texture_path),
            arcade.load_texture(self.idle_texture_path,
                                flipped_horizontally=True),
        ]

        # Set the initial texture to right
        self.texture = self.idle_texture_pair[self.character_face_direction]

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        self.texture = self.idle_texture_pair[self.character_face_direction]


class MyGame(arcade.Window):
    """
    Main application class.
    """

    # Our Scene Object
    scene = None

    # Separate variable that holds the player sprite
    player_sprite = None

    # Our physics engine
    physics_engine = None

    # A Camera that can be used for scrolling the screen
    camera = None

    # Our TileMap Object
    tile_map = None

    # Name of map file to load
    map_name = "Map/Hollownest.json"

    # Track the current state of what key is pressed
    left_pressed = False
    right_pressed = False
    up_pressed = False
    jump_needs_reset = False

    def __init__(self):
        ''' __init__ '''
        # Call the parent class and set up the window
        super().__init__(width=WINDOW_WIDTH,
                         height=WINDOW_HEIGHT,
                         title=WINDOW_TITLE,
                         antialiasing=True)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Decors": {
                "use_spatial_hash": True,
            }
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            self.map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            walls=self.scene["Platforms"],
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed:
            if (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - \
            (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update Animations
        self.scene.update_animation(
            delta_time, ["Player"]
        )

        # Position the camera
        self.center_camera_to_player()


if __name__ == "__main__":
    window = MyGame()
    icon = pyglet.image.load('assets/icon-64.png')
    window.set_icon(icon)
    window.setup()
    arcade.run()
