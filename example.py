from dotenv import load_dotenv
import os
import asyncio

from monarchmoney_typed import TypedMonarchMoney

# Configure logging
# logging.basicConfig(level=logging.DEBUG)
#
# # Enable aiohttp client logging
# aiohttp_logger = logging.getLogger("aiohttp.client")
# aiohttp_logger.setLevel(logging.DEBUG)
# aiohttp_logger.addHandler(logging.StreamHandler())


# Load environment variables from .env file
load_dotenv()


# Access the variables
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
mfa_secret = os.getenv("MFA_SECRET")


async def main():
    mm = TypedMonarchMoney()
    await mm.login(
        email=username,
        password=password,
        save_session=True,
        use_saved_session=True,
        mfa_secret_key=mfa_secret,
    )

    data = await mm.get_accounts()
    print("-" * 80)
    print("\n")
    print(data)

    cashflow_summary = await mm.get_cashflow_summary()
    print("-" * 80)
    print("\n")
    print(cashflow_summary)


asyncio.run(main())
