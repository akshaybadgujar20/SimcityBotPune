import logging
import gymnasium as gym
from gymnasium import spaces
import random
import numpy as np
from simcity.bot.enums.material import Material

class SimCityEnv(gym.Env):
    def __init__(self):
        super(SimCityEnv, self).__init__()

        # Define storage parameters
        self.max_capacity = 1080  # Total storage capacity
        self.raw_materials = [

        ]
        self.commercial_products = [
            Material.NAILS,
            Material.PLANKS,
            Material.BRICKS,
            Material.CEMENT,
            Material.GLUE,
            Material.PAINT,
            Material.MEASURING_TAPE,
            Material.SHOVEL,
            Material.COOKING_UTENSILS,
            Material.LADDER,
            Material.DRILL,
            Material.VEGETABLES,
            Material.FLOUR_BAG,
            Material.FRUIT_AND_BERRIES,
            Material.CREAM,
            Material.CORN,
            Material.CHEESE,
            Material.BEEF,
            Material.CHAIRS,
            Material.TABLES,
            Material.HOME_TEXTILES,
            Material.CUPBOARD,
            Material.COUCH,
            Material.GRASS,
            Material.TREE_SAPLINGS,
            Material.GARDEN_FURNITURE,
            Material.FIRE_PIT,
            Material.LAWN_MOWER,
            Material.GARDEN_GNOMES,
            Material.DONUTS,
            Material.GREEN_SMOOTHIE,
            Material.BREAD_ROLL,
            Material.CHERRY_CHEESECAKE,
            Material.FROZEN_YOGURT,
            Material.COFFEE,
            Material.CAP,
            Material.SHOES,
            Material.WATCH,
            Material.BUSINESS_SUITS,
            Material.BACKPACK,
            Material.ICE_CREAM_SANDWICH,
            Material.PIZZA,
            Material.BURGERS,
            Material.CHEESE_FRIES,
            Material.LEMONADE_BOTTLE,
            Material.POPCORN,
            Material.BBQ_GRILL,
            Material.REFRIGERATOR,
            Material.LIGHTING_SYSTEM,
            Material.TV,
            Material.MICROWAVE_OVEN,
            Material.REUSABLE_BAG,
            Material.ECOLOGICAL_SHOES,
            Material.YOGA_MAT,
            Material.MOTOR_OIL,
            Material.CAR_TIRE,
            Material.ENGINE,
            Material.STRING,
            Material.FAN,
            Material.ROBE,
            Material.COCONUT_OIL,
            Material.FACE_CREAM,
            Material.TROPICAL_DRINK,
            Material.CANNED_FISH,
            Material.FISH_SOUP,
            Material.SALMON_SANDWICH,
            Material.TIRAMISU,
            Material.CHURROS,
            Material.PROFITEROLE,
            Material.WOOL_SHIRT,
            Material.PICNIC_BASKET,
            Material.APPLE_JAM,
            Material.TENNIS_RACKET,
            Material.SPORTS_DRINK,
            Material.FOOTBALL_SHOES,
            Material.PROTEIN_BAR,
            Material.PING_PONG_TABLE,
            Material.WROUGHT_IRON,
            Material.CARVED_WOOD,
            Material.CHISELED_STONE,
            Material.TAPESTRY,
            Material.LETTER_BLOCKS,
            Material.KITE,
            Material.TEDDY_BEAR,
            Material.GAME_CONSOLE,
        ]
        self.materials = self.raw_materials + self.commercial_products

        # Initialize storage
        self.inventory = {material: 0 for material in self.materials}

        # Define the building upgrade requirements
        self.building_requirements = {
            "Building1": {Material.WOOD: 2, Material.METAL: 1},
            "Building2": {Material.MINERALS: 3, Material.CHEMICALS: 4},
            # Add more buildings and their material requirements
        }

        # Initialize upgrades (stores the remaining materials needed for upgrade)
        self.upgrades = [
            {"building": "Building1", "remaining": {Material.WOOD: 2, Material.METAL: 1}},
            {"building": "Building2", "remaining": {Material.MINERALS: 3, Material.CHEMICALS: 4}},
        ]

        self.actions = [
            "PRODUCE_FACTORY_MATERIAL",
            "PRODUCE_COMMERCIAL_MATERIAL"
        ]

        # Action space
        self.action_space = spaces.Discrete(2 * len(self.materials))

        # Observation space: Include current storage state and upgrades
        self.observation_space = spaces.Dict({
            "inventory": spaces.Box(
                low=0,
                high=self.max_capacity,
                shape=(len(self.materials),),
                dtype=np.float32
            ),
            "upgrades": spaces.Box(
                low=0,
                high=self.max_capacity,
                shape=(len(self.upgrades), len(self.materials)),
                dtype=np.float32
            ),
        })

        # Initialize the environment state
        self.state = self.reset()

    def decode_action(self, action):
        material_index = action % len(self.materials)
        action_type = action // len(self.materials)
        material = self.materials[material_index]
        logging.info("material_index => %s", material_index)
        logging.info("action_type => %s", action_type)
        logging.info("material => %s", material)
        if action_type == 0:
            return "PRODUCE_FACTORY_MATERIAL", material
        else:
            return "PRODUCE_COMMERCIAL_MATERIAL", material

    def reset(self, seed=None, **kwargs):
        super().reset(seed=seed)
        self.inventory = {material: 0 for material in self.materials}
        self.upgrades = [
            {"building": "Building1", "remaining": {Material.WOOD: 2, Material.METAL: 1}},
            {"building": "Building2", "remaining": {Material.MINERALS: 3, Material.CHEMICALS: 4}},
        ]
        observation = self._get_obs()
        return observation, {}  # Return observation and info for gymnasium>=0.26

    def step(self, action):
        action_type, material = self.decode_action(action)
        reward = 0
        done = False

        print(f"Action: {action_type}, Material: {material}")

        # Handle factory material production
        if action_type == "PRODUCE_FACTORY_MATERIAL":
            if material in self.raw_materials:
                self.inventory[material] += 1
                reward += self._process_material(material)

        # Handle commercial material production
        elif action_type == "PRODUCE_COMMERCIAL_MATERIAL":
            if material in self.commercial_products:
                self.inventory[material] += 1
                reward += self._process_material(material)

        # Check for completed upgrades
        for upgrade in self.upgrades[:]:  # Iterate on a copy to avoid modification issues
            if material in upgrade["remaining"]:
                upgrade["remaining"][material] -= 1
                if upgrade["remaining"][material] <= 0:
                    del upgrade["remaining"][material]
                    reward += 10

            # If all materials are fulfilled, remove the upgrade
            if not upgrade["remaining"]:
                self.upgrades.remove(upgrade)
                reward += 50

        # Check if all upgrades are completed
        terminated = False
        if not self.upgrades:
            terminated = True

        truncated = False  # Modify based on your criteria
        done = terminated or truncated

        # Print the current state for debugging
        # print(f"Updated Inventory: {self.inventory}")
        # print(f"Remaining Upgrades: {self.upgrades}")

        # Create observation
        observation = self._get_obs()
        info = {}

        return observation, reward, terminated, truncated, info

    def _process_material(self, material):
        """Optional helper function to handle material-specific processing."""
        # Customize logic for specific materials if needed
        return 1  # Default reward for producing a material

    def _get_obs(self):
        # Convert inventory to numpy array
        inventory = np.array(list(self.inventory.values()), dtype=np.float32)

        # Convert upgrades to numpy array
        upgrades_array = np.zeros((len(self.upgrades), len(self.materials)), dtype=np.float32)
        for i, upgrade in enumerate(self.upgrades):
            for material, qty in upgrade["remaining"].items():
                material_idx = self.materials.index(material)
                upgrades_array[i, material_idx] = qty

        return {
            "inventory": inventory,
            "upgrades": upgrades_array
        }

    def seed(self, seed=None):
        """Set the seed for the environment's random number generators."""
        if seed is None:
            seed = np.random.randint(0, 2 ** 31 - 1)  # Generate a valid random seed in the valid range for int32
        elif seed < 0 or seed >= 2 ** 31:
            raise ValueError("Seed must be between 0 and 2**31 - 1")

        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def render(self, mode="human"):
        print(f"Current Inventory: {self.inventory}")
        print(f"Building Upgrades: {self.upgrades}")
