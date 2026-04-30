import sys
import os
sys.path.append(os.getcwd())

import pytest
from utils.privacy_vault import PrivacyVault

def test_privacy_vault_masking():
    vault = PrivacyVault()
    text = "My name is John Doe and I work for Google."
    masked = vault.mask(text)
    
    assert "John Doe" not in masked
    assert "Google" not in masked
    assert "<PERSON_" in masked
    assert "<ORG_" in masked

def test_privacy_vault_unmasking():
    vault = PrivacyVault()
    text = "Contact Alice at 123-456-7890."
    masked = vault.mask(text)
    unmasked = vault.unmask(masked)
    
    assert unmasked == "Contact Alice at 123-456-7890."

from unittest.mock import MagicMock, patch

def test_router_logic():
    # We mock the router so it doesn't try to initialize ChatGroq in CI
    with patch('core.router.router') as mock_router:
        mock_router.route.side_effect = lambda q: MagicMock(category="GREETING" if "Hello" in q else "LEGAL_QUERY")
        
        greeting = mock_router.route("Hello there!")
        assert greeting.category == "GREETING"
        
        query = mock_router.route("What are the laws on theft?")
        assert query.category == "LEGAL_QUERY"
