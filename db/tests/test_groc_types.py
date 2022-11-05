"""
module for testing the grocery types
"""

import db.groc_types as gtyp


def test_get_groc_types():
    """
    test get_groc_types
    """
    assert len(gtyp.get_groc_types()) > 0
    assert isinstance(gtyp.get_groc_types(), list)
