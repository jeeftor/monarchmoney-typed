import logging

from dotenv import load_dotenv
import os
import asyncio

from typedmonarchmoney import TypedMonarchMoney
from typedmonarchmoney.models import MonarchHoldings

# Configure logging
logging.basicConfig(level=logging.INFO)
#
# # Enable aiohttp client logging
aiohttp_logger = logging.getLogger("gql.transport.aiohttp")
aiohttp_logger.setLevel(logging.WARNING)
aiohttp_logger.addHandler(logging.StreamHandler())


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

    data = await mm.get_subscription_details()
    print("-" * 80)
    print("\n")
    print(data)

    accounts = await mm.get_accounts()
    print("-" * 80)

    # Parse and Print holdings

    for account in accounts:
        print(f"---[{account.name}]---")
        print(f"   {account.type} {account.subtype} {account.id}")

        holdings: MonarchHoldings = await mm.get_account_holdings(account)

        holdings.print_table()

    #
    # cashflow_summary = await mm.get_cashflow_summary()
    # print("-" * 80)
    # print("\n")
    # print(cashflow_summary)


# async def main2():
#     # Load in json
#     current_dir = os.path.dirname(__file__)
#     file_path = os.path.join(current_dir, "test/fixtures", "get_account_holdings.json")
#     with open(file_path, "r") as file:
#         holdings = MonarchHoldings(json.load(file))
#
#     print(holdings)
#
#     holdings.print_table()


asyncio.run(main())
