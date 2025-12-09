import gymnasium as gym
from simcity.bot.enums.building import get_commercial_building
from simcity.bot.enums.material import Material
from simcity.bot.simcity_bot.commercial_data import get_commercial_data
from simcity.bot.simcity_bot.factory_data import get_factory_data
import numpy as np
from gymnasium import spaces

class SimCityEnv(gym.Env):
    def __init__(self):
        super(SimCityEnv, self).__init__()

        # Factory and commercial production data
        self.factory_data = get_factory_data()  # List of dictionaries with material and production time
        self.commercial_production_data = get_commercial_data()

        # Extract materials and production times
        self.raw_materials = [data["material"] for data in self.factory_data]
        self.material_production_times = {data["material"]: data["production_time"] for data in self.factory_data}

        # Commercial materials and their production times
        for building in self.commercial_production_data:
            for item in building["produces"]:
                self.material_production_times[item["material"]] = item["production_time"]

        # Constants
        self.max_level = 7  # Set the max level of buildings
        self.num_factories = 12
        self.num_factory_slots = 5
        self.num_commercial_buildings = len(self.commercial_production_data)
        self.num_commercial_slots = 11
        self.max_buildings = 5

        # Factories and commercial buildings
        self.factories = [{"slots": [None] * self.num_factory_slots} for _ in range(self.num_factories)]
        self.commercial_buildings = [
            {
                "name": building["name"],
                "slots": [None] * self.num_commercial_slots,
                "produces": building["produces"],  # List of materials with different production times
            }
            for building in self.commercial_production_data
        ]

        # State attributes
        self.state = None
        self.buildings = [self._init_building() for _ in range(self.max_buildings)]
        self.inventory = {material: 0 for material in self.material_production_times.keys()}
        self.production_queues = []

        # Define observation and action spaces
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(self._get_state_size(),), dtype=np.float32
        )
        self.action_space = spaces.MultiDiscrete(
            [len(self.raw_materials) + len(self.material_production_times), self.num_factories + self.num_commercial_buildings]
        )

    def _init_building(self):
        """Initialize a building with random material requirements."""
        num_requirements = np.random.randint(1, 4)  # Random 1-3 materials required
        requirements = {
            material: np.random.randint(1, 4)  # Require 1-3 units of each material
            for material in np.random.choice(
                [item["material"] for building in self.commercial_production_data for item in building["produces"]],
                size=num_requirements,
                replace=False,
            )
        }
        return {
            "level": 1,
            "requirements": requirements,
            "status": "idle"
        }

    def _get_state_size(self):
        """Determine the size of the flattened state vector."""
        factory_state_size = self.num_factories * self.num_factory_slots
        commercial_state_size = self.num_commercial_buildings * self.num_commercial_slots
        return (
            len(self.buildings) * 10  # Example: 10 features per building
            + len(self.inventory)  # Inventory items
            + factory_state_size  # Factory slots
            + commercial_state_size  # Commercial slots
        )

    def reset(self, seed=None, **kwargs):
        """Reset the environment to an initial state."""
        if seed is not None:
            np.random.seed(seed)  # Set the random seed for reproducibility

        self.buildings = [self._init_building() for _ in range(self.max_buildings)]
        self.inventory = {material: 0 for material in self.material_production_times.keys()}
        self.production_queues = []
        self.factories = [{"slots": [None] * self.num_factory_slots} for _ in range(self.num_factories)]
        self.commercial_buildings = [
            {"name": building["name"], "slots": [None] * self.num_commercial_slots, "produces": building["produces"]}
            for building in self.commercial_production_data
        ]
        self.state = self._get_observation()
        return self.state, {}

    def step(self, action):
        """Execute one time step within the environment."""
        # Decode the action
        material_index, building_index = action

        # Validate material index
        total_materials = len(self.raw_materials) + len(self.material_production_times)
        if material_index < len(self.raw_materials):
            material = self.raw_materials[material_index]
        elif material_index < total_materials:
            material = list(self.material_production_times.keys())[material_index - len(self.raw_materials)]
        else:
            raise ValueError(f"Invalid material index: {material_index}")

        # Validate building index
        if building_index < self.num_factories:
            building_type = "factory"
            building_id = building_index
        elif building_index < self.num_factories + self.num_commercial_buildings:
            building_type = "commercial"
            building_id = building_index - self.num_factories
        else:
            raise ValueError(f"Invalid building index: {building_index}")

        # Implement the logic for material production in the specified building
        # Example logic (replace with your actual implementation)
        if building_type == "factory":
            self._produce_in_factory(building_id, material)
        elif building_type == "commercial":
            self._produce_in_commercial_building(building_id, material)

        # Update the state
        self.state = self._get_observation()

        # Calculate the reward (customize this based on your environment)
        reward = self._calculate_reward()

        # Check if the episode is done (customize as needed)
        done = self._check_done()

        # Return the new state, reward, and done flag
        return self.state, reward, done, {}, {}

    def _process_production(self):
        """Simulate production queue processing."""
        # Process factories
        for factory in self.factories:
            for slot in range(len(factory["slots"])):
                if factory["slots"][slot]:
                    factory["slots"][slot]["time_remaining"] -= 1
                    if factory["slots"][slot]["time_remaining"] <= 0:
                        self.inventory[factory["slots"][slot]["material"]] += 1
                        factory["slots"][slot] = None

        # Process commercial buildings
        for building in self.commercial_buildings:
            for slot in range(len(building["slots"])):
                if building["slots"][slot]:
                    building["slots"][slot]["time_remaining"] -= 1
                    if building["slots"][slot]["time_remaining"] <= 0:
                        self.inventory[building["slots"][slot]["material"]] += 1
                        building["slots"][slot] = None

    def _produce_in_commercial_building(self, building_id, material):
        """Simulate producing a material in a commercial building."""
        # Implement the logic for producing materials in a commercial building
        commercial_building = self.commercial_buildings[building_id]
        # Example logic (you can modify it according to your needs):
        if material in commercial_building["produces"]:
            # Add material to the inventory or production queue, etc.
            self.inventory[material] += 1
            return True  # Return success or failure of the production
        return False

    def _produce_in_factory(self, building_id, material):
        """Simulate producing a material in a factory."""
        factory = self.factories[building_id]
        # Example logic (you can modify it according to your needs):
        if material in factory["slots"]:
            # Add material to the inventory or production queue, etc.
            self.inventory[material] += 1
            return True  # Return success or failure of the production
        return False

    def _check_done(self):
        """Check if the environment has reached a terminal state."""
        # Example: Episode ends after a certain number of steps or when a specific goal is reached.

        # Example: End when all buildings are fully upgraded
        for building in self.buildings:
            if building["level"] < self.max_level:
                return False  # Episode continues if any building is not fully upgraded

        # Example: Limit the number of steps or actions
        if self.steps_taken >= self.max_steps:
            return True  # Episode ends after max_steps

        # Alternatively, you can define custom conditions for episode termination
        return False  # Return False to continue the episode by default

    def _calculate_reward(self):
        """Calculate and return the reward based on the current state."""
        # Example: Calculate reward based on the number of buildings produced or the materials in inventory
        reward = 0

        # Reward based on building production (example)
        for building in self.buildings:
            reward += building["level"]  # Reward could be based on the level of the building, for example

        # Reward based on inventory (example)
        for material, quantity in self.inventory.items():
            reward += quantity  # Reward could be based on the quantity of materials produced

        # Optionally, apply penalties (e.g., for running out of resources)
        if any(qty < 0 for qty in self.inventory.values()):
            reward -= 10  # Penalty for negative inventory

        return reward

    def _get_observation(self):
        """Generate a flattened state vector."""
        # Flatten buildings
        max_requirements = max(len(b["requirements"]) for b in self.buildings)
        building_state = np.concatenate([
            np.array([b["level"]] + list(b["requirements"].values()) + [0] * (max_requirements - len(b["requirements"])))
            for b in self.buildings
        ])

        # Inventory state
        inventory_state = np.array(list(self.inventory.values()))

        # Factory state
        factory_state = np.array([
            1 if slot else 0 for factory in self.factories for slot in factory["slots"]
        ])

        # Commercial buildings state
        commercial_state = np.array([
            1 if slot else 0 for building in self.commercial_buildings for slot in building["slots"]
        ])

        # Combine all components
        observation = np.concatenate([building_state, inventory_state, factory_state, commercial_state])

        # Validate the size
        expected_size = self.observation_space.shape[0]
        if observation.size < expected_size:
            # Pad with zeros if smaller
            observation = np.pad(observation, (0, expected_size - observation.size))
        elif observation.size > expected_size:
            # Truncate if larger
            observation = observation[:expected_size]

        return observation

    def render(self, mode="human"):
        """Render the environment (optional)."""
        print(f"Buildings: {self.buildings}")
        print(f"Inventory: {self.inventory}")
        print(f"Factories: {self.factories}")
        print(f"Commercial Buildings: {self.commercial_buildings}")
