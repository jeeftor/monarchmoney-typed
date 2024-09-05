"""Type wrapper around Monarch Money"""

from typing import List, Optional

import monarchmoney.monarchmoney
from monarchmoney import MonarchMoney

from monarchmoney_wrapper.models import MonarchAccount


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
