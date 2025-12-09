from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from simcity.bot.test.SimCityEnv import SimCityEnv

# Define the main class that initializes, trains, and tests the model
def train_and_test_model():
    # Create environment with make_vec_env
    env = make_vec_env(lambda: SimCityEnv(), n_envs=1)  # Use n_envs=1 for a single environment

    # Initialize PPO model with MultiInputPolicy for Dict observation space
    model = PPO("MultiInputPolicy", env, verbose=1)

    # Train the model
    model.learn(total_timesteps=100000)  # Train for 100,000 timesteps

    # Save the trained model
    model.save("ppo_simcity")

    # Load the saved model and continue training if needed
    model = PPO.load("ppo_simcity", env=env)
    model.learn(total_timesteps=100000, tb_log_name="ppo_run")

    # Testing the model after training
    obs = env.reset()
    for _ in range(1000):  # Run for 1000 steps
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)

        # Access inventory and upgrades directly from `obs`
        # print(f"Action: {action}, Reward: {reward}, Done: {done}")
        # print("Inventory:", obs["inventory"])
        # print("Remaining Upgrades:", obs["upgrades"])
        # print("\n\n")

        if done:
            obs = env.reset()

# Test the environment separately if needed
def test_environment():
    env = make_vec_env(lambda: SimCityEnv(), n_envs=1)  # Create the environment instance with make_vec_env
    obs, info = env.reset()  # Reset to initial state

    done = False
    while not done:
        action = env.action_space.sample()  # Random action for testing
        obs, reward, done, info = env.step(action)

        # Print action, reward, done, and environment state
        # print(f"Action: {action}, Reward: {reward}, Done: {done}")
        # print("Inventory:", obs[0]["inventory"])
        # print("Remaining Upgrades:", obs[0]["upgrades"])

# Run the training and testing
if __name__ == "__main__":
    train_and_test_model()
    # test_environment()  # Uncomment this line if you want to test separately
