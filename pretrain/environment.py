import gym
import torch as T
import numpy as np
import random
from supersuit import frame_stack_v1, resize_v0, clip_reward_v0
from stable_baselines3.common.atari_wrappers import EpisodicLifeEnv


def create_env(config, name='MsPacman', render=None):
    env = gym.make('ALE/' + name + '-v5',
                   obs_type='grayscale',  # ram | rgb | grayscale
                   frameskip=config['frames_to_skip'],  # frame skip
                   mode=0,  # game mode, see Machado et al. 2018
                   difficulty=0,  # game difficulty, see Machado et al. 2018
                   repeat_action_probability=0.0,  # Sticky action probability
                   full_action_space=True,  # Use all actions
                   render_mode=render  # None | human | rgb_array
                   )

    env = clip_reward_v0(env, lower_bound=-1, upper_bound=1)
    env = resize_v0(env, config['height'], config['width'], linear_interp=True)
    env = frame_stack_v1(env, config['frames_to_stack'])

    env = EpisodicLifeEnv(env)

    return env


def seed_everything(seed, deterministic=False):
    T.manual_seed(seed)

    if deterministic:
        T.backends.cudnn.deterministic = True
        T.backends.cudnn.benchmark = False
    else:
        T.backends.cudnn.benchmark = True

    np.random.seed(seed)
    random.seed(seed)
    if T.cuda.is_available():
        T.cuda.manual_seed(seed)
