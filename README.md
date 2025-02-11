# bb-finder
A Python tool that helps you discover bug bounty programs and security vulnerability disclosure pages for specified domains with Google dorking and by using SerpApi's Google Search API.


## Features

- Search for bug bounty programs and vulnerability disclosure pages
- Support for both single domain and bulk domain checking
- Identifies common bug bounty program indicators
- Colored output for better visibility
- Saves detailed results in JSON format
- Rate limit friendly with built-in delays

**🚀Tip: Make a list of startups domains and check them periodically so you be the first one who test their bug bounty program.**

## Installation

Clone the repository:

`git clone https://github.com/Ahmed-makawi/bb-finder.git`

`cd bb-finder`

Install requirements:

`sudo apt install python3-venv` (Linux only)

`python3 -m venv myenv` (Linux only)

`source myenv/bin/activate` (Linux only)

`pip install -r requirements.txt`

### requirements:
- Python
- serpapi Python package
- colorama package
- A SerpApi API key (**get one at https://serpapi.com**)

## Usage
The tool can be used in two ways:

### Check a single domain:

`python3 bb-finder.py -d example.com --api YOUR_API_KEY`

### Check multiple domains from a file:

`python3 bb-finder.py -f domains.txt --api YOUR_API_KEY`

## Arguments
**-d, --domain:** Single domain to check

**-f, --file:** Text file containing list of domains (one per line)

**--api:** Your SerpApi API key (required)

**-o, --output:** Output JSON file name (default: bug_bounty_results.json)

**Example domains.txt format**
google.com
facebook.com
microsoft.com





## Example output:
![image](https://github.com/user-attachments/assets/3a54a994-4ea0-483c-9407-2c4ed1c93382)

![image](https://github.com/user-attachments/assets/6dab3918-2b9c-48a4-bd31-03178caaed73)




## Rate Limiting
The tool includes a 2-second delay between searches to respect SerpApi's rate limits. Monitor your API usage on your SerpApi dashboard.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer
This tool is for educational and ethical hacking purposes only. Always ensure you have permission to test any systems and follow responsible disclosure guidelines.
