from scholar_wizard.static import STATIC
from scholar_wizard.libs.wp import check_doi_resolution


class TestCheckDoiResolution:
    """Test the 'check_doi_resolution' function."""

    def test_call_to_valid_doi(self):
        """Should return True."""
        doi = STATIC.VALID_DOI
        assert check_doi_resolution(doi) is True

    def test_call_to_invalid_doi(self):
        """Should return False"""
        invalid_doi = "10.1234/invalid-doi"
        assert check_doi_resolution(invalid_doi) is False
