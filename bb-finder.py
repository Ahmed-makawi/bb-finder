import os
from serpapi import GoogleSearch
import json
from typing import List, Dict
import time
from urllib.parse import urlparse
import argparse
import sys
from colorama import init, Fore, Style
import requests

# Initialize colorama
init(autoreset=True)

def load_domains(file_path: str) -> List[str]:
    """Load domains from a text file"""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_path}' not found!{Style.RESET_ALL}")
        sys.exit(1)

def load_api_keys(file_path: str = None, api_key: str = None) -> List[str]:
    """Load API keys from a file or use a single API key provided directly"""
    if file_path:
        try:
            with open(file_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}Error: File '{file_path}' not found!{Style.RESET_ALL}")
            sys.exit(1)
    elif api_key:
        return [api_key]
    else:
        print(f"{Fore.RED}Error: No API key or file provided!{Style.RESET_ALL}")
        sys.exit(1)

def get_remaining_requests(api_key: str) -> int:
    """Get the number of remaining requests for an API key"""
    url = f"https://serpapi.com/account?api_key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("total_searches_left", 0)
    except Exception as e:
        print(f"{Fore.RED}Error fetching remaining requests: {str(e)}{Style.RESET_ALL}")
        return 0

def check_bug_bounty_programs(domains: List[str], api_keys: List[str]) -> Dict[str, dict]:
    """
    Check if domains have public bug bounty programs using SerpApi.
    
    Args:
        domains: List of domain names to check
        api_keys: List of SerpApi API keys
    
    Returns:
        Dictionary with results for each domain
    """
    results = {}
    total_domains = len(domains)
    api_key_index = 0
    current_api_key = api_keys[api_key_index]

    for idx, domain in enumerate(domains, 1):
        print(f"{Fore.CYAN}Checking {domain}... [{idx}/{total_domains}]{Style.RESET_ALL}")
        
        # Clean domain name
        clean_domain = urlparse(domain).netloc if '//' in domain else domain
        
        # Create search queries for bug bounty programs
        search_queries = [
            f'site:{clean_domain} "bug bounty" OR "vulnerability disclosure" OR "VDP" OR "report vulnerability" OR "security rewards"',
            f'site:{clean_domain} "responsible disclosure" OR "security.txt" OR "security vulnerability" OR "hall of fame" OR "bug hunters"'
        ]
        
        domain_results = {
            'has_bb_program': False,
            'relevant_urls': [],
            'program_hints': []
        }
        
        for query in search_queries:
            try:
                # Check remaining requests for the current API key
                remaining_requests = get_remaining_requests(current_api_key)
                if remaining_requests <= 0:
                    # Switch to the next API key
                    api_key_index = (api_key_index + 1) % len(api_keys)
                    current_api_key = api_keys[api_key_index]
                    print(f"{Fore.YELLOW}Switching to API key {api_key_index + 1}/{len(api_keys)}{Style.RESET_ALL}")
                    remaining_requests = get_remaining_requests(current_api_key)
                    if remaining_requests <= 0:
                        print(f"{Fore.RED}No remaining requests for any API key. Exiting.{Style.RESET_ALL}")
                        return results
                
                search = GoogleSearch({
                    "q": query,
                    "api_key": current_api_key,
                    "num": 5  # Limit results to reduce API usage
                })
                
                response = search.get_dict()
                
                if "organic_results" in response:
                    for result in response["organic_results"]:
                        title = result.get("title", "").lower()
                        snippet = result.get("snippet", "").lower()
                        url = result.get("link", "")
                        
                        # Look for common bug bounty indicators
                        bb_keywords = [
                            "bug bounty", "security rewards", "bug hunters",
                            "vulnerability disclosure", "responsible disclosure",
                            "security.txt", "report vulnerability", "VDP", "BB Program"
                        ]
                        
                        for keyword in bb_keywords:
                            if keyword in title or keyword in snippet:
                                domain_results['has_bb_program'] = True
                                if url not in domain_results['relevant_urls']:
                                    domain_results['relevant_urls'].append(url)
                                    domain_results['program_hints'].append(
                                        f"Found '{keyword}' mention at {url}"
                                    )
                
                # Respect rate limits
                time.sleep(2)
                
            except Exception as e:
                print(f"{Fore.RED}Error checking {domain}: {str(e)}{Style.RESET_ALL}")
                # If the error is due to API limit, switch to the next key
                if "API key usage limit reached" in str(e):
                    api_key_index = (api_key_index + 1) % len(api_keys)
                    current_api_key = api_keys[api_key_index]
                    print(f"{Fore.YELLOW}API limit reached. Switching to API key {api_key_index + 1}/{len(api_keys)}{Style.RESET_ALL}")
                    continue
                else:
                    sys.exit(1)
        
        if domain_results['has_bb_program']:
            results[clean_domain] = domain_results
    
    return results

def save_results(results: Dict[str, dict], output_file: str):
    """Save results to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

def main():
    parser = argparse.ArgumentParser(
        description='Check domains for bug bounty programs using SerpApi'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='Text file containing list of domains (one per line)')
    group.add_argument('-d', '--domain', help='Single domain to check')
    parser.add_argument('--api', help='Text file containing SerpApi API keys (one per line)')
    parser.add_argument('--api-key', help='Single SerpApi API key')
    parser.add_argument('-o', '--output', default='bug_bounty_results.json',
                        help='Output JSON file name (default: bug_bounty_results.json)')
    args = parser.parse_args()
    
    # Handle single domain or domain list
    domains = [args.domain] if args.domain else load_domains(args.file)
    
    # Load API keys
    if args.api:
        api_keys = load_api_keys(file_path=args.api)
    elif args.api_key:
        api_keys = load_api_keys(api_key=args.api_key)
    else:
        print(f"{Fore.RED}Error: No API key or file provided!{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.CYAN}Loaded {len(domains)} domain(s) to check{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Using {len(api_keys)} API key(s){Style.RESET_ALL}")
    
    # Check domains
    results = check_bug_bounty_programs(domains, api_keys)
    
    # Save results
    save_results(results, args.output)
    
    # Print summary only for positive results
    if results:
        print(f"\n{Fore.GREEN}Found {len(results)} domains with bug bounty programs:{Style.RESET_ALL}")
        for domain, data in results.items():
            print(f"\n{Fore.GREEN}✓ {domain}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Relevant URLs:{Style.RESET_ALL}")
            for url in data['relevant_urls']:
                print(f"  {Fore.CYAN}→{Style.RESET_ALL} {url}")
    else:
        print(f"\n{Fore.YELLOW}No bug bounty programs found for any of the checked domains.{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Full results saved to {args.output}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
