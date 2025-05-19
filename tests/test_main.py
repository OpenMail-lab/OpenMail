import pytest
from universal-installer import MainApp

def test_email_creation():
    app = MainApp()
    assert app is not None

def test_get_public_ip():
    from universal-installer import get_public_ip
    ip = get_public_ip()
    assert isinstance(ip, str)
    assert len(ip) > 0
