import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RPCRetrier:
    """A utility class to handle retry logic for RPC calls."""
    def __init__(self, max_retries: int = 3, retry_delay: int = 1):
        """
        Initialize the retrier with retry configuration.

        :param max_retries: Maximum number of retry attempts.
        :param retry_delay: Delay (in seconds) between retries.
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def call(self, func, *args, **kwargs):
        """
        Execute the given function with retry logic.

        :param func: The function to execute.
        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        :return: The result of the function if successful.
        :raises: The last exception if all retries fail.
        """
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"RPC call failed: {e}. Retrying... ({attempt + 1}/{self.max_retries})")
                    await asyncio.sleep(self.retry_delay)
                else:
                    logger.error(f"RPC call failed after {self.max_retries} attempts: {e}")
                    raise
                