# LeetCode Problem Scraper and Python File Generator

This project automates the process of fetching LeetCode problems, extracting their descriptions, code snippets (Python), and example test cases, and then generating individual Python files for each problem, ready for local development and testing.

## Features

*   **Scrapes LeetCode problems:** Fetches problem data from LeetCode, including title, description URL, code snippets, and test cases, using the LeetCode GraphQL API.
*   **Handles Premium Problems:** Identifies and skips premium-only problems that are not accessible without a subscription.
*   **Generates Python Files:** Creates well-structured Python files for each problem, including:
    *   The problem's code (with proper indentation and formatting).
    *   Example test cases (formatted as function calls within a `main()` function).
    *   Standard Python `if __name__ == '__main__':` entry point.
    *   A comment linking back to the original problem on LeetCode.
*   **Asynchronous Operations:** Uses `asyncio`, `aiohttp`, and `aiofiles` for efficient and non-blocking network requests and file operations.

## Project Structure

*   **`leetcode_async_parser_problems.py`:** Contains the core logic for scraping LeetCode problem data using `aiohttp` and `BeautifulSoup`.
*   **`creation_python_files.py`:** Handles the creation of individual Python files from the scraped problem data.
*   **`launcher.py`:** The main entry point for running the scraper and file generator.
*   **`config.py`:** Stores configuration settings, such as cookies and headers for making requests to LeetCode.

## Getting Started

### Prerequisites

1. **Python 3.7+**
2. **LeetCode Account**

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Fer1dlock/leetcode-problems-parser
    cd leetcode-problems-parser
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. **Update `config.py`:**
    *   Replace 'your_cookies' and 'your_headers' with your values. I recommend using this site (https://curlconverter.com/). The cURL bash can be taken from any problem on Leetcode (e.g. https://leetcode.com/problems/two-sum/description/).

### Usage

1. **Run the script:**

    ```bash
    python launcher.py
    ```

    *   The script will scrape LeetCode problems and store them in `data/result_list.json`.
    *   Individual Python files for each problem will be generated in the `problems/` directory.

### Important Notes

*   **Premium Problems:** Premium-only problems will be skipped, and a message will be printed to the console.
*   **Error Handling:** The script has basic error handling, but you might encounter issues depending on your network connection and LeetCode's server status.

## Contributing

Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (You need to create a LICENSE file in your project - choose a license that suits your needs. The MIT License is a common choice for open-source projects).

---
**Remember to:**

1. Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub username and repository name.
2. Create a `LICENSE` file in your repository and choose an appropriate license.
3. Fill in the shields at the top with the correct links (stars, issues, license).
4. Consider adding a section on how to run the generated Python files and how to use them for solving LeetCode problems.

This comprehensive README will make your project more accessible and easier to understand for other developers. I hope this helps!
