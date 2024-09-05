from datetime import datetime
from typing import Any


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
        self.institution_url = institution.get("url", None)
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

        self.income = data.get("sumIncome", -1.0)
        self.expenses = data.get("sumExpense", -1.0)
        self.savings = data.get("savings", -1.0)
        self.savings_rate = data.get("savingsRate", -1.0)
