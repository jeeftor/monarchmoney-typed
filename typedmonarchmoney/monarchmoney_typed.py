"""Type wrapper around Monarch Money"""

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

    async def get_accounts(self) -> List[MonarchAccount]:
        """Return accounts."""
        data = await super().get_accounts()
        return [MonarchAccount(acc) for acc in data["accounts"]]

    async def get_accounts_as_dict_with_id_key(self) -> dict[int, MonarchAccount]:
        """Return accounts as a dictionary where account id is the key."""
        data = await super().get_accounts()
        return {int(acc["id"]): MonarchAccount(acc) for acc in data["accounts"]}

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

    async def get_account_holdings(self, account: MonarchAccount) -> MonarchHoldings:
        """Return account holdings for a given account."""
        data = await super().get_account_holdings(account.id)
        return MonarchHoldings(data)

    async def get_account_holdings_for_id(self, account_id: int) -> MonarchHoldings:
        """Return account holdings for a given account id."""
        data = await super().get_account_holdings(account_id)
        return MonarchHoldings(data)
