from unittest.mock import MagicMock, patch
import logging
import pytest
from scholar_wizard.libs.scholar_utils import setup_proxy


class TestSetupProxy:
    """Test the 'setup_proxy' function."""

    @pytest.fixture
    def mock_use_proxy(self):
        """Mocks the call to the use_proxy method of the scholarly module."""
        scholarly_mock = MagicMock()
        scholarly_mock.use_proxy.return_value = None
        with patch(f"{setup_proxy.__module__}.scholarly") as mock:
            mock.return_value = scholarly_mock
            yield scholarly_mock

    def test_proxy_setup(
        self, caplog: pytest.LogCaptureFixture, mock_use_proxy: pytest.FixtureRequest
    ):
        """Should set up the scholarly proxy."""
        with caplog.at_level(logging.DEBUG):
            setup_proxy()

        assert "Using a proxy generator" in caplog.text
        mock_use_proxy.assert_called_once()
