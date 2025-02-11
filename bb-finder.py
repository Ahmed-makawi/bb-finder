import os
from serpapi import GoogleSearch
import json
from typing import List, Dict
import time
from urllib.parse import urlparse
import argparse
import sys
from colorama import init, Fore, Style

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

def check_bug_bounty_programs(domains: List[str], api_key: str) -> Dict[str, dict]:
    """
    Check if domains have public bug bounty programs using SerpApi.
    
    Args:
        domains: List of domain names to check
        api_key: SerpApi API key
    
    Returns:
        Dictionary with results for each domain
    """
    results = {}
    total_domains = len(domains)
    
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
                search = GoogleSearch({
                    "q": query,
                    "api_key": api_key,
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
    parser.add_argument('--api', required=True, help='SerpApi API key')
    parser.add_argument('-o', '--output', default='bug_bounty_results.json',
                        help='Output JSON file name (default: bug_bounty_results.json)')
    args = parser.parse_args()
    
    # Handle single domain or domain list
    domains = [args.domain] if args.domain else load_domains(args.file)
    
    print(f"{Fore.CYAN}Loaded {len(domains)} domain(s) to check{Style.RESET_ALL}")
    
    # Check domains
    results = check_bug_bounty_programs(domains, args.api)
    
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