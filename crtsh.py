#!/usr/bin/env python3

import argparse
import asyncio
import aiohttp
import validators
from colorama import Fore, Style, init
import sys

init(autoreset=True)

def print_banner():
    banner = f"""{Fore.LIGHTBLUE_EX}
           _         _      
          | |       | |     
  ___ _ __| |_   ___| |__   
 / __| '__| __| / __| '_ \  
| (__| |  | |_ _\__ \ | | | 
 \___|_|   \__(_)___/_| |_| 
                           
    Subdomain Finder via crt.sh | Async Mode ⚡
    Made with 💀 by {Fore.LIGHTMAGENTA_EX}AIwolfie{Style.RESET_ALL}
"""
    print(banner)


# -------- Async Subdomain Fetcher --------
async def fetch_subdomains(session, domain, no_wildcard):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()

    for attempt in range(3):
        try:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    print(f"{Fore.RED}[!] Error: {response.status} for {domain}")
                    return []

                try:
                    data = await response.json()
                except Exception:
                    print(f"{Fore.RED}[!] Failed to parse JSON from crt.sh for {domain}")
                    return []

                for entry in data:
                    name_value = entry.get('name_value', '')
                    for sub in name_value.split('\n'):
                        sub = sub.strip()
                        if no_wildcard and sub.startswith('*.'):
                            continue
                        if sub.endswith(domain):
                            subdomains.add(sub)

                return sorted(subdomains)

        except Exception as e:
            if attempt < 2:
                await asyncio.sleep(2)
            else:
                print(f"{Fore.RED}[!] Failed to fetch for {domain} after 3 attempts.")
    return []

# -------- Load Domains from CLI/File --------
def load_domains(args):
    domains = []

    if args.domain:
        domains = [d.strip() for d in args.domain.split(",") if d.strip()]
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                domains = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Fore.RED}[!] Could not read file: {e}")
            sys.exit(1)

    valid = []
    for d in domains:
        if validators.domain(d):
            valid.append(d)
        else:
            print(f"{Fore.RED}[!] Invalid domain skipped: {d}")

    if not valid:
        print(f"{Fore.RED}[!] No valid domains found.")
        sys.exit(1)

    return valid

# -------- Async Controller --------
async def process_all(domains, no_wildcard):
    all_subdomains = {}
    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_subdomains(session, domain, no_wildcard) for domain in domains]
        results = await asyncio.gather(*tasks)

        for domain, subs in zip(domains, results):
            if subs:
                all_subdomains[domain] = subs

    return all_subdomains

# -------- Main CLI Logic --------
def main():
    parser = argparse.ArgumentParser(description="Async Subdomain Finder using crt.sh")
    parser.add_argument("-d", "--domain", help="Target domain(s), comma-separated")
    parser.add_argument("-f", "--file", help="File containing domains (one per line)")
    parser.add_argument("-o", "--output", help="File to save the output")
    parser.add_argument("--no-wildcard", action="store_true", help="Filter out wildcard subdomains (e.g., *.domain.com)")
    args = parser.parse_args()

    domains = load_domains(args)
    print(f"{Fore.CYAN}[+] Scanning {len(domains)} domain(s)...\n")

    results = asyncio.run(process_all(domains, args.no_wildcard))

    all_found = []

    for domain, subdomains in results.items():
        print(f"{Fore.GREEN}[+] {domain} — {len(subdomains)} subdomain(s) found:")
        for sub in subdomains:
            print(f"    {Fore.WHITE}{sub}")
        print()
        all_found.extend(subdomains)

    if args.output:
        try:
            with open(args.output, 'w') as f:
                for sub in sorted(set(all_found)):
                    f.write(sub + '\n')
            print(f"{Fore.MAGENTA}[+] Saved all results to {args.output}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to save results: {e}")

if __name__ == "__main__":
    main()
