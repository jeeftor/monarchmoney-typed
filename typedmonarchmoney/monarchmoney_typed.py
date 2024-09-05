"""Type wrapper around Monarch Money"""

from typing import List, Optional

import monarchmoney.monarchmoney
from monarchmoney import MonarchMoney
from monarchmoney.monarchmoney import DEFAULT_RECORD_LIMIT

from .models import MonarchAccount, MonarchCashflowSummary


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
        data = await super().get_accounts()
        return [MonarchAccount(acc) for acc in data["accounts"]]

    async def get_cashflow_summary(
        self,
        limit: int = DEFAULT_RECORD_LIMIT,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> MonarchCashflowSummary:
        """Return cashflow summary."""
        data = await super().get_cashflow_summary(limit, start_date, end_date)
        return MonarchCashflowSummary(data["summary"][0]["summary"])
