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

import typing
import bittensor as bt

# TODO(developer): Rewrite with your protocol definition.

# This is the protocol for the Superpi miner and validator.
# It is a simple request-response protocol where the validator sends a request
# to the miner, and the miner responds with the value of pi.

# ---- miner ----
# Example usage:
#   def get_superpi( synapse: Superpi ) -> Superpi:
#       synapse.pi_value = 3.141592654
#       return synapse
#   axon = bt.Axon().attach( get_superpi ).serve(netuid=...).start()

# ---- validator ---
# Example usage:
#   dendrite = bt.Dendrite()
#   pi_value = dendrite.query( Superpi() )
#   assert pi_value == 3.141592654


class Superpi(bt.Synapse):
    """
    A protocol for requesting the value of pi from miners.
    This protocol helps in handling Superpi request and response communication between
    the miner and the validator.

    Attributes:
    - pi_value: An optional float value which, when filled, represents the response from the miner.
    """

    # Optional request output, filled by receiving axon.
    pi_value: typing.Optional[float] = None

    def deserialize(self) -> float:
        """
        Deserialize the pi value. This method retrieves the response from
        the miner in the form of pi_value, deserializes it and returns it
        as the output of the dendrite.query() call.

        Returns:
        - float: The deserialized response, which in this case is the value of pi_value.

        Example:
        Assuming a Superpi instance has a pi_value of 3.141592654:
        >>> superpi_instance = Superpi()
        >>> superpi_instance.pi_value = 3.141592654
        >>> superpi_instance.deserialize()
        3.141592654
        """
        return self.pi_value