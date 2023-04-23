## Testing functions

https://tilburgsciencehub.com/building-blocks/configure-your-computer/task-specific-configurations/configuring-python-for-webscraping/

- Install dependencies
```bash
$ pip install -r requirements.txt
```

- Install chromedriver

  - [Download Driver](https://chromedriver.chromium.org/downloads)
  - [Install Chrome](https://tilburgsciencehub.com/building-blocks/configure-your-computer/task-specific-configurations/configuring-python-for-webscraping/)


- Export environment variables
```bash
export AWS_OFFLINE=true
export GOOGLE_CHROME_DRIVER=/tmp/chromedriver
```

- Run integration tests
```bash
$ ./use_localstack.sh
$ pytest
$ python -m pytest
$ pytest -k "test_handler_kabum_success" test_app.py
```

- Run code coverage
```bash
$ python -m pytest --cov=src --cov-report=html
```