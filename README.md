1# bb-finder
A Python tool that helps you discover bug bounty programs and security vulnerability disclosure pages for specified domains with Google dorking and by using SerpApi's Google Search API.


## Features

- Use list of SerpApi keys so when one reach the quota limit the tools jump to the next key.
- Search for bug bounty programs and vulnerability disclosure pages.
- Support for both single domain and bulk domain checking.
- Identifies common bug bounty program indicators.
- Colored output for better visibility.
- Saves detailed results in JSON format.
- Rate limit friendly with built-in delays.

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

`python3 bb-finder.py -d example.com --api-key YOUR_API_KEY`

### Check multiple domains from a file:

`python3 bb-finder.py -f domains.txt --api YOUR_API_KEY`

### Use a file that contains list of Apis 

`python3 bb-finder.py -f domains.txt --api-keys FILE_OF_YOUR_API_KEYS`

## Arguments
**-d, --domain:** Single domain to check

**-f, --file:** Text file containing list of domains (one per line)

**--api:** Your SerpApi API key (required)

**--api-keys:** Use a file that contians a list of Apis, so when one an Api reach the quota limit the tool automaticly use other api key.

**-o, --output:** Output JSON file name (default: bug_bounty_results.json)

**Example domains.txt format**
google.com
facebook.com
microsoft.com





## Example output:
![image](https://github.com/user-attachments/assets/48ed2614-0638-4e2e-821b-a65056868257)

![image](https://github.com/user-attachments/assets/6dab3918-2b9c-48a4-bd31-03178caaed73)

![image](https://github.com/user-attachments/assets/6eebee58-3ff3-40c4-a687-0dfa703df70f)

![WhatsApp Image 2025-02-11 at 21 14 10_d8d2f4e7](https://github.com/user-attachments/assets/c9d43437-de4d-4025-89cb-16f61f4c1140)






## Rate Limiting
The tool includes a 2-second delay between searches to respect SerpApi's rate limits. Monitor your API usage on your SerpApi dashboard.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer
This tool is for educational and ethical hacking purposes only. Always ensure you have permission to test any systems and follow responsible disclosure guidelines.
