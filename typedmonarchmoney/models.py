import json
from datetime import datetime
from typing import Any

from rich.console import Console
from rich.table import Table


# ------ Helper Functions --------
def _parse_float(value: Any) -> float:
    """Attempt to parse a value to float, return -1.0 if it fails."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return -1.0


def _parse_int(value: Any) -> int:
    """Attempt to parse a value to int, return -1 if it fails."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return -1


class MonarchAccount:
    """Dataclass to store & parse account data from monarch accounts."""

    id: str
    logo_url: str | None
    name: str
    balance: float
    type: str  # type will be used for icons
    type_name: str  # type name will be used for device
    subtype: str
    subtype_name: str
    data_provider: str
    institution_url: str | None
    institution_name: str | None
    last_update: datetime
    date_created: datetime

    @property
    def is_value_account(self):
        """Return true if we are tracking a value type asset."""
        return self.type in ["real-estate", "vehicle", "valuables", "other_assets"]

    @property
    def is_balance_account(self):
        """Whether to show a balance sensor or a value sensor."""
        return not self.is_value_account

    def __init__(self, data: dict[str, Any]):
        """Initialize MonarchAccount object from dict."""
        institution = data.get("institution") or {}
        credential = data.get("credential") or {}

        self.id = data["id"]
        self.logo_url = data.get("logoUrl")
        self.name = data["displayName"]
        self.balance = data["currentBalance"]
        self.type = data["type"]["name"]
        self.type_name = data["type"]["display"]
        self.subtype = data["subtype"]["name"]
        self.subtype_name = data["subtype"]["display"]
        self.data_provider = credential.get("dataProvider", "Manual entry")
        self.last_update = datetime.fromisoformat(data["updatedAt"])
        self.date_created = datetime.fromisoformat(data["createdAt"])
        self.institution_url = institution.get("url", "http://monarchmoney.com")

        if not self.institution_url.startswith(("http://", "https://")):
            self.institution_url = f"http://{self.institution_url}"

        self.institution_name = institution.get("name", "Manual entry")


class MonarchCashflowSummary:
    """Cashflow data class."""

    income: float
    expenses: float
    savings: float
    savings_rate: float

    def __init__(self, data: dict[str, Any]):
        """Build a monarch cashflow object."""
        if (
            "summary" in data
            and isinstance(data["summary"], list)
            and len(data["summary"]) > 0
        ):
            data = data["summary"][0]["summary"]

        self.income = _parse_float(data.get("sumIncome", -1.0))
        self.expenses = _parse_float(data.get("sumExpense", -1.0))
        self.savings = _parse_float(data.get("savings", -1.0))
        self.savings_rate = _parse_float(data.get("savingsRate", -1.0))


class MonarchSubscription:
    """Dataclass to store & parse subscription data from monarch accounts."""

    id: str
    payment_source: str
    referral_code: str
    is_on_free_trial: bool
    has_premium_entitlement: bool

    def __init__(self, data: dict[str, Any]):
        """Initialize MonarchSubscription object from dict."""
        subscription = data.get("subscription", data)
        self.id = subscription["id"]
        self.payment_source = subscription["paymentSource"]
        self.referral_code = subscription["referralCode"]
        self.is_on_free_trial = subscription["isOnFreeTrial"]
        self.has_premium_entitlement = subscription["hasPremiumEntitlement"]

    def __str__(self):
        return (
            f"MonarchSubscription(id={self.id}, payment_source={self.payment_source}, "
            f"referral_code={self.referral_code}, is_on_free_trial={self.is_on_free_trial}, "
            f"has_premium_entitlement={self.has_premium_entitlement})"
        )


class MonarchHolding:
    ticker: str
    name: str
    quantity: int
    total_value: float
    type: str
    type_name: str
    price: float
    price_date: datetime | None
    percentage: float = -1.0

    def __init__(self, data: dict[str:Any]):
        # Set easy mode values
        self.total_value = _parse_float(data["node"]["totalValue"])
        self.quantity = _parse_int(data["node"]["quantity"])

        security = data["node"].get("security", {})
        holding0 = data["node"]["holdings"][0]

        if security := data["node"]["security"]:
            self.ticker = security["ticker"]
            self.name = security["name"]
            self.type = security["type"]
            self.type_name = security["typeDisplay"]
            self.price = _parse_float(security["currentPrice"])
            self.price_date = security["currentPriceUpdatedAt"]
        else:
            self.ticker = holding0["ticker"]
            if self.ticker == "CUR:USD":
                self.name = "cash"
                self.price = 1
            else:
                self.type = holding0["type"]
                self.price = _parse_float(holding0["closingPrice"])
                self.price_date = holding0["closingPriceUpdatedAt"]

            self.name = holding0["name"]
            self.type_name = holding0["typeDisplay"]

    def __str__(self):
        return (
            f'MonarchHolding(ticker={self.ticker}, name="{self.name}", quantity={self.quantity}, '
            f"total_value={self.total_value},  type_name={self.type_name}, price={self.price})"
        )


class MonarchHoldings:
    holdings: list[MonarchHolding] = []

    _account: MonarchAccount | None = None
    _account_id_str: str
    total_value: float = 0.0

    def __init__(
        self,
        data: dict[str, Any],
        account_or_id: MonarchAccount | int | str | None = None,
    ) -> None:
        # Default info
        self._account_id_str = "UNKNOWN"

        if isinstance(account_or_id, MonarchAccount):
            self._account = account_or_id
            self._account_id_str = str(account_or_id.id)

        elif isinstance(account_or_id, str):  # String case
            self._account_id_str = account_or_id
        else:  # int case
            self._account_id_str = str(account_or_id)

        for item in data["portfolio"]["aggregateHoldings"]["edges"]:
            self.holdings.append(MonarchHolding(item))
            self.total_value += self.holdings[-1].total_value

        # Set the percentage
        for item in self.holdings:
            try:
                item.percentage = item.total_value / self.total_value
            except ZeroDivisionError:
                item.percentage = 0.0

    def __str__(self):
        return str([str(holding) for holding in self.holdings])

    def to_json(self) -> str:
        """Return holdings data as a JSON string."""
        holdings_list = [
            {
                "index": idx,
                "ticker": holding.ticker,
                "quantity": holding.quantity,
                "totalValue": holding.total_value,
                "type": holding.type_name,
                "percentage": round(holding.percentage * 100.0, 1),
                "name": holding.name,
                "sharePrice": holding.price,
                "sharePriceUpdate": holding.price_date,
            }
            for idx, holding in enumerate(self.holdings)
        ]
        return json.dumps({holdings_list}, indent=2)

    def print_table(self):
        console = Console()

        # If we have an account

        if self._account is not None:
            title = f"Holdings for {self._account.name}"
        else:
            title = f"Holdings for {self._account_id_str}"

        table = Table(title=title)
        table.add_column("Ticker", style="cyan")
        table.add_column("Quantity", style="green")
        table.add_column("Total Value", style="blue")
        table.add_column("Type", style="yellow")
        table.add_column("Percentage", style="red")
        table.add_column("Name", style="magenta")

        for holding in self.holdings:
            table.add_row(
                holding.ticker,
                str(holding.quantity),
                str(holding.total_value),
                holding.type_name,
                str(round(holding.percentage * 100.0, 1)),
                holding.name,
            )
        console.print(table)
