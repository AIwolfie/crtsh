# crtsh.py

A Python utility to fetch (or scrape) subdomains from [crt.sh](https://crt.sh)

---

## Requirements

- `argparse`  
- `aiohttp`  
- `asyncio`  
- `colorama`  
- `validators`  

Install with:

```bash
pip install -r requirements.txt
```

---

## Installation

```bash
git clone https://github.com/YashGoti/crtsh.py.git
cd crtsh.py
python3 crtsh.py -h
```

### If you want to use `crtsh` from anywhere:

```bash
git clone https://github.com/YashGoti/crtsh.py.git
cd crtsh.py
mv crtsh.py crtsh
chmod +x crtsh
sudo cp crtsh /usr/local/bin/
```

---

## Options

| Flag                  | Description                                  |
|-----------------------|----------------------------------------------|
| `-h`, `--help`        | Show this help message and exit              |
| `-d`, `--domain`      | Specify target domain(s) (comma-separated)   |
| `-f`, `--file`        | File containing domains to scan              |
| `-n`, `--no-wildcard` | Remove wildcard subdomains from the results  |
| `-o`, `--output`      | Save subdomains to a file                    |

---

## Usage

```bash
python3 crtsh.py -d example.com
python3 crtsh.py -d example.com -n
python3 crtsh.py -d example.com,github.com
python3 crtsh.py -f domains.txt -n -o subs.txt
```

---

**Made by AIwolfie**

<a href="https://www.buymeacoffee.com/mayankmalac" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

