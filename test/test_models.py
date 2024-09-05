from datetime import datetime
from typing import Dict, Any

from monarchmoney_wrapper.models import MonarchAccount


def test_parse_accounts(mock_account_data: Dict[str, Any]) -> None:
    """Test if get_accounts.json can be parsed into MonarchAccount objects."""
    accounts = [MonarchAccount(data) for data in mock_account_data["accounts"]]

    assert len(accounts) == 7

    # Test account 1
    account1 = accounts[0]
    assert account1.id == "900000000"
    assert account1.logo_url == "base64Nonce"
    assert account1.name == "Brokerage"
    assert account1.balance == 1000.50
    assert account1.type == "brokerage"
    assert account1.type_name == "Investments"
    assert account1.subtype == "brokerage"
    assert account1.subtype_name == "Brokerage"
    assert account1.data_provider == "PLAID"
    assert account1.institution_url == "https://rando.brokerage/"
    assert account1.institution_name == "Rando Brokerage"
    assert account1.last_update == datetime.fromisoformat(
        "2022-05-26T00:56:41.322045+00:00"
    )
    assert account1.date_created == datetime.fromisoformat(
        "2021-10-15T01:32:33.809450+00:00"
    )

    # Test account 2
    account2 = accounts[1]
    assert account2.id == "900000002"
    assert account2.logo_url == "data:image/png;base64,base64Nonce"
    assert account2.name == "Checking"
    assert account2.balance == 1000.02
    assert account2.type == "depository"
    assert account2.type_name == "Cash"
    assert account2.subtype == "checking"
    assert account2.subtype_name == "Checking"
    assert account2.data_provider == "PLAID"
    assert account2.institution_url == "https://rando.bank/"
    assert account2.institution_name == "Rando Bank"
    assert account2.last_update == datetime.fromisoformat(
        "2024-02-17T11:21:05.228959+00:00"
    )
    assert account2.date_created == datetime.fromisoformat(
        "2021-10-15T01:32:33.900521+00:00"
    )

    # Test account 3
    account3 = accounts[2]
    assert account3.id == "9000000007"
    assert account3.logo_url == "data:image/png;base64,base64Nonce"
    assert account3.name == "Credit Card"
    assert account3.balance == -200.0
    assert account3.type == "credit"
    assert account3.type_name == "Credit Cards"
    assert account3.subtype == "credit_card"
    assert account3.subtype_name == "Credit Card"
    assert account3.data_provider == "FINICITY"
    assert account3.institution_url == "https://rando.credit/"
    assert account3.institution_name == "Rando Credit"
    assert account3.last_update == datetime.fromisoformat(
        "2022-12-10T18:17:06.129456+00:00"
    )
    assert account3.date_created == datetime.fromisoformat(
        "2021-10-15T01:33:46.646459+00:00"
    )