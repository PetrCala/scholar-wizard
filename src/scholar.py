from loguru import logger
from scholarly import scholarly, ProxyGenerator


def use_proxy() -> None:
    """Use a proxy generator to avoid Google Scholar blocking."""
    logger.debug("Using proxy generator to avoid Google Scholar blocking...")
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)
