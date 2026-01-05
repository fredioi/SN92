# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import numpy as np
from typing import List
import bittensor as bt


def reward(response: float) -> float:
    """
    Reward the miner response to the Superpi request. This method returns a reward
    value for the miner, which is used to update the miner's score.
    Miners that return the correct value of pi (3.141592654) get full reward,
    others get 0 reward.

    Returns:
    - float: The reward value for the miner.
    """
    target_value = 3.141592654
    reward_value = 1.0 if response == target_value else 0.0
    
    bt.logging.info(
        f"Reward calculation - Response: {response}, Target: {target_value}, Reward: {reward_value}"
    )
    return reward_value


def get_rewards(
    self,
    responses: List[float],
) -> np.ndarray:
    """
    Returns an array of rewards for the given responses.

    Args:
    - responses (List[float]): A list of responses from the miner.

    Returns:
    - np.ndarray: An array of rewards for the given responses.
    """
    # Get all the reward results by iteratively calling your reward() function.
    rewards = np.array([reward(response) for response in responses])
    
    # Normalize rewards so that they sum to 1 across all miners that responded correctly
    successful_miners = rewards > 0
    if np.sum(successful_miners) > 0:
        # Assign equal reward to all successful miners
        rewards[successful_miners] = 1.0 / np.sum(successful_miners)
    else:
        # If no miners were successful, all get 0
        rewards = np.zeros_like(rewards, dtype=float)
    
    bt.logging.info(f"Normalized rewards: {rewards}")
    return rewards