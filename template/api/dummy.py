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

import bittensor as bt
from template.protocol import Superpi
from abc import ABC, abstractmethod


class SubnetsAPI(ABC):
    """
    Base class for all subnet APIs.
    """
    subnet: int = None

    def __init__(self, wallet: bt.Wallet, subtensor: bt.Subtensor):
        self.wallet = wallet
        self.subtensor = subtensor

    @abstractmethod
    def prepare_synapse(self) -> Superpi:
        """
        Prepare the synapse object for the forward call.
        """
        pass

    @abstractmethod
    def process_responses(self, responses: list[Superpi]) -> list:
        """
        Process the responses from the miners.
        """
        pass


class SuperpiAPI(SubnetsAPI):
    subnet: int = 92

    def prepare_synapse(self) -> Superpi:
        """
        Prepare the synapse object for the forward call.
        """
        synapse = Superpi()
        return synapse

    def process_responses(self, responses: list[Superpi]) -> float:
        """
        Process the responses from the miners.
        
        Args:
            responses: List of Superpi objects from miners
            
        Returns:
            float: The average of all valid pi values returned
        """
        valid_responses = []
        for response in responses:
            if response and response.pi_value is not None:
                valid_responses.append(response.pi_value)
        
        if not valid_responses:
            return 0.0
        
        return sum(valid_responses) / len(valid_responses)