## Testing functions

- Install dependencies
```bash
$ pip install -r dev-requirements.txt
```

- Run integration tests
```bash
$ cd scraping && ./use_localstack.sh
$ cd scraping && pytest
$ cd scraping && python -m pytest
```

- Run code coverage
```bash
$ cd scraping && python -m pytest --cov=src --cov-report=html
```