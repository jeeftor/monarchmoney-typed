"""Type wrapper around Monarch Money"""

import asyncio
from typing import List, Optional

import monarchmoney.monarchmoney
from monarchmoney import MonarchMoney
from monarchmoney.monarchmoney import DEFAULT_RECORD_LIMIT

from .models import (
    MonarchAccount,
    MonarchCashflowSummary,
    MonarchSubscription,
    MonarchHoldings,
)


class TypedMonarchMoney(MonarchMoney):
    def __init__(
        self,
        session_file: str = monarchmoney.monarchmoney.SESSION_FILE,
        timeout: int = 10,
        token: Optional[str] = None,
    ) -> None:
        """Call superclass initializer"""
        super().__init__(session_file, timeout, token)

    async def get_accounts(self, with_holdings: bool = False) -> List[MonarchAccount]:
        """Return accounts."""
        data = await super().get_accounts()

        accounts = [MonarchAccount(acc) for acc in data["accounts"]]
        if with_holdings:
            tasks = [self.get_account_holdings(account) for account in accounts]
            holdings = await asyncio.gather(*tasks)
            for account, holding in zip(accounts, holdings):
                account.holdings = holding
        return accounts

    async def get_accounts_as_dict_with_id_key(
        self, with_holdings: bool = False
    ) -> dict[str, MonarchAccount]:
        """Return accounts as a dictionary where account id is the key."""
        accounts = await self.get_accounts(with_holdings)
        return {account.id: account for account in accounts}

    async def get_cashflow_summary(
        self,
        limit: int = DEFAULT_RECORD_LIMIT,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> MonarchCashflowSummary:
        """Return cashflow summary."""
        data = await super().get_cashflow_summary(limit, start_date, end_date)
        return MonarchCashflowSummary(data["summary"][0]["summary"])

    async def get_subscription_details(self) -> MonarchSubscription:
        """Return subscription details."""
        data = await super().get_subscription_details()
        return MonarchSubscription(data["subscription"])

    async def get_account_holdings_for_id(
        self, account_id: str | int
    ) -> MonarchHoldings | None:
        """Return account holdings for a given account id."""
        data = await super().get_account_holdings(int(account_id))
        if len(data["portfolio"]["aggregateHoldings"]["edges"]) == 0:
            return None
        return MonarchHoldings(data)

    async def get_account_holdings(
        self, account: MonarchAccount
    ) -> MonarchHoldings | None:
        """Return account holdings for a given account."""
        return await self.get_account_holdings_for_id(account.id)
