import json
import os
from typing import List, Dict, Any

import pytest


@pytest.fixture
def mock_account_data() -> List[Dict[str, Any]]:
    """Fixture to load sample accounts data from get_accounts.json."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "fixtures", "get_accounts.json")
    with open(file_path, "r") as file:
        return json.load(file)


@pytest.fixture
def mock_subscription_data1() -> Dict[str, Any]:
    """Fixture to load sample accounts data from get_accounts.json."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "fixtures", "get_subscription_details.json")
    with open(file_path, "r") as file:
        return json.load(file)


@pytest.fixture
def mock_subscription_data2() -> Dict[str, Any]:
    """Fixture to load sample accounts data from get_accounts.json."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "fixtures", "get_subscription_details_2.json")
    with open(file_path, "r") as file:
        return json.load(file)
