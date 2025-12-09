import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from simcity.bot.simcity_bot.SimCityEnv import SimCityEnv  # Ensure this path matches your project structure

# Define the environment
class SimCityEnvWrapper(SimCityEnv):
    def __init__(self):
        super(SimCityEnvWrapper, self).__init__()

# Training script
def train_model():
    # Create the environment and wrap it for vectorized processing
    env = make_vec_env(SimCityEnvWrapper, n_envs=1)

    # Initialize the PPO model
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./simcity_tensorboard/")

    # Train the model
    print("Starting model training...")
    model.learn(total_timesteps=100000)
    print("Training complete.")

    # Save the model
    model.save("simcity_ppo_model")
    print("Model saved as 'simcity_ppo_model'.")

if __name__ == "__main__":
    train_model()
