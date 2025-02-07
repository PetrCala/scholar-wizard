from loguru import logger
from scholarly import scholarly, ProxyGenerator


def setup_proxy() -> None:
    """Use a proxy generator to avoid Google Scholar blocking."""
    logger.debug("Using a proxy generator to avoid Google Scholar blocking...")
    pg = ProxyGenerator()
    pg.Tor_Internal(tor_cmd="/Applications/Tor Browser.app/Contents/MacOS/Tor/tor")
    # pg.FreeProxies()
    scholarly.use_proxy(pg)
