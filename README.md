# smtp-gmail-sender

This repository contains Python code for sending personalized marketing emails via Gmail, utilizing the Gmail SMTP server and the ChatGPT API. The entire process is automated and can be executed with a single click.

## Overview

The `smtp-gmail-sender` script streamlines the process of sending customized marketing emails. It fetches a contact list that includes details such as the recipient's name, email, company name, and website. The script then web scrapes the company's website to extract a description and uses the ChatGPT API to generate a tailored marketing email based on this information. Finally, it sends the generated content through Gmail automatically.

## Main Features

- **Contact List Fetching**: Retrieves contact details including name, email, company name, and website.
- **Web Scraping**: Extracts the company description from the provided website.
- **AI-Powered Email Generation**: Uses the ChatGPT API to create a unique and relevant marketing email.
- **Automated Email Sending**: Sends the generated email content via Gmail using the SMTP server.
- **One-Click Execution**: The entire process is initiated and completed by running a single `run.bat` file.

![Demo](https://github.com/starglow-it/smtp-gmail-sender/smtp-gmail-sender-guide.gif)

## Prerequisites

- Python 3.10
- Required Python libraries (see `requirements.txt`)
- Gmail account with SMTP enabled
- OpenAI API key

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/starglow-it/smtp-gmail-sender.git
   cd smtp-gmail-sender
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your Gmail SMTP settings and OpenAI API key in the script.

4. Prepare your contact list in the specified format.

## Usage

1. Ensure all prerequisites are met.
2. Double-click the `run.bat` file.
3. The script will automatically:
   - Fetch contact details.
   - Scrape company descriptions.
   - Generate and send personalized marketing emails.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License.
"""
