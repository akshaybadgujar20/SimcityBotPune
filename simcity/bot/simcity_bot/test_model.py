import gym
from stable_baselines3 import PPO

from simcity.bot.enums.material import Material
from simcity.bot.simcity_bot.SimCityEnv import SimCityEnv


def test_model(model_path, custom_requirements):
    """
    Test a trained model against custom building requirements.

    Args:
        model_path (str): Path to the trained PPO model.
        custom_requirements (list): List of custom building requirements.
                                    Example: [{"id": 1, "level": 3}, {"id": 2, "level": 5}]
    """
    # Initialize the custom environment
    env = SimCityEnv()

    # Set the custom building requirements
    env.buildings = custom_requirements

    # Load the trained model
    model = PPO.load(model_path)

    # Reset the environment
    obs, info = env.reset()

    done = False
    total_reward = 0
    steps = 0

    print("Testing model against custom building requirements:")
    print(f"Initial state: {env.buildings}")

    while not done:
        # Predict the next action using the trained model
        action, _states = model.predict(obs, deterministic=True)

        # Take a step in the environment
        obs, reward, done, truncated, info = env.step(action)

        # Update metrics
        total_reward += reward
        steps += 1

        # Print step details
        print(f"Step: {steps}, Action: {action}, Reward: {reward}")
        print(f"Current state: {env.buildings}")

        # Stop if truncated (optional)
        if truncated:
            print("Episode truncated (max steps reached).")
            break

    print("Test completed.")
    print(f"Final state: {env.buildings}")
    print(f"Total reward: {total_reward}, Total steps: {steps}")


# Example custom building requirements
custom_building_requirements = [
    {"id": 1, "level": 1, "required_materials": [Material.WOOD, Material.NAILS]},
    {"id": 2, "level": 2, "required_materials": [Material.PLANKS, Material.PLASTIC]},
]

# Path to the trained model
model_path = "simcity_ppo_model.zip"

# Test the model
test_model(model_path, custom_building_requirements)
