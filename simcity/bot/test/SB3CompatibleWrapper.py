import gymnasium as gym

class SB3CompatibleWrapper(gym.Wrapper):
    def reset(self, **kwargs):
        # Gymnasium's reset returns (observation, info), but SB3 expects only observation
        observation, _ = self.env.reset(**kwargs)
        return observation

    def step(self, action):
        # Gymnasium's step returns (observation, reward, terminated, truncated, info),
        # SB3 expects (observation, reward, done, info)
        observation, reward, terminated, truncated, info = self.env.step(action)
        done = terminated or truncated  # Combine terminated and truncated into done
        return observation, reward, done, info
