# eenaduPDF

**eenaduPDF** is a python script to download ఈనాడు newspaper.

# Usage

* Dump your cookies to `cookies.txt` in your CWD or pass it through `--cookies` arg.
* to use telegram auto post feature, create `telegram.json`

    ```json
    {
    "bot_token": "51xxxxxyyzz:xxxxxxxxxxxxxxxxxxxxxxxxx",
    "chan_id": "-1000000000"
    }
    ```
    Fill your details and and use `--telegram` flag.


```
pipenv install
EENADU_DEBUG=INFO python eenadu.py
```

```
options:
  -h, --help            show this help message and exit
  -e {ANDHRAPRADESH,TELANGANA,HYDERABAD,SUNDAY}, --edition {ANDHRAPRADESH,TELANGANA,HYDERABAD,SUNDAY}
  -d DATE, --date DATE  date of e-paper (DD/MM/YYYY)
  -t, --telegram        Telegram JSON Config
  -c COOKIES, --cookies COOKIES
                        Cookie Dump.
```                        