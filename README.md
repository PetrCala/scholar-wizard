# Scholar wizard

Scholar Wizard is a custom package to help facilitate searching through the Google Scholar database.

## How to install

The package has not yet been posted to any package libraries. You can install the package using pip like so:

```bash
pip install git+https://github.com/PetrCala/scholar-wizard.git
```

## Documentation

The package is still in development, so a thorough documentation would not stay up-to-date for too long.

For a brief overview, here is a list of available functions:

- **`search`**: Search the Google Scholar database using a custom query
- **`snowball`**: Snowball from a study set.

You can run these functions by simply importing from the package like so:

```python
# In a python module
import scholar_wizard as sw

search_results = sw.search()
snowballing_results = sw.snowball()
```
