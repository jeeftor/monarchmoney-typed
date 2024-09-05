import json
from typing import List, Dict, Any

import pytest


@pytest.fixture
def mock_account_data() -> List[Dict[str, Any]]:
    """Fixture to load sample accounts data from get_accounts.json."""
    with open("fixtures/get_accounts.json", "r") as file:
        return json.load(file)
