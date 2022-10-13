# pixiv-scrap

Scrapping from pixiv based on given tags

## Usage

```bash
usage: python3 pixiv-scrap.py [-h] [--depth DEPTH] keyword

Scrap images from pixiv

positional arguments:
  keyword        Search/tags keyword

options:
  -h, --help     show this help message and exit
  --depth DEPTH  Maximum number of page
```

### Example

```bash
python3 pixiv-scrap.py 魔女の旅々10000users入り --depth 2
```

## REQUIREMENTS

Need browser's cookie

**Need to export pixiv cookie from broser and put it together with pixiv-scap.py with name 'cookies.txt'**

Plugins to export cookies as cookies.txt from browser:

Firefox: <https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/>

Chrome: <https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid?hl=en>
