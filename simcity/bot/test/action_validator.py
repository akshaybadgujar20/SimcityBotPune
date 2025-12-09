from stable_baselines3 import PPO
import numpy as np
from simcity.bot.enums.material import Material
from simcity.bot.test.SimCityEnv import SimCityEnv

# Load your trained model
model = PPO.load("ppo_simcity")


# Initialize the environment
env = SimCityEnv()

# Example state setup
inventory = {material: 0 for material in env.materials}  # Initialize all material quantities to 0
upgrades = np.zeros((len(env.upgrades), len(env.materials)))  # Example, you might need actual upgrade data

# Example building requirements (for testing)
building_requirements = {
    "Building1": {Material.WOOD: 2, Material.METAL: 1},
    "Building2": {Material.MINERALS: 3, Material.CHEMICALS: 2},
}

# Flatten the building requirements for all buildings
flattened_building_requirements = []
for building, requirements in building_requirements.items():  # Use items() to access the building and its requirements
    flattened_requirements = [requirements.get(material, 0) for material in env.materials]
    flattened_building_requirements.extend(flattened_requirements)

# Construct the observation including building requirements
obs = {
    "inventory": np.array([inventory[material] for material in env.materials], dtype=np.float32),
    "upgrades": upgrades,
    "building_requirements": np.array(flattened_building_requirements, dtype=np.float32)
}

# Construct the observation as a dictionary
obs = {
    "inventory": np.array([inventory[material] for material in env.materials], dtype=np.float32),
    "upgrades": upgrades
}

# Predict the action using the model
action, _ = model.predict(obs, deterministic=True)

# Map the action to its meaning
action_meaning = env.actions[action]
print(f"Predicted Action: {action_meaning}")

