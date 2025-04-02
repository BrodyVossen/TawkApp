# Tawk.to Dashboard Automation Bot

This bot automates the process of exporting conversations from the Tawk.to dashboard.

## Features

- Automatically logs into the Tawk.to dashboard
- Navigates to the inbox
- Selects all conversations 
- Exports conversations to a specified email
- Handles pagination (processes 100 conversations per page)

## Prerequisites

- Node.js (v14 or later recommended)
- npm (comes with Node.js)

## Installation

1. Clone this repository or download the files
2. Open a terminal/command prompt in the project directory
3. Install dependencies:

```bash
npm install
```

## Configuration

You can modify the configuration in the `tawkbot.js` file:

- `loginUrl`: The URL of the Tawk.to login page
- `email`: Your Tawk.to account email
- `password`: Your Tawk.to account password
- `exportEmail`: The email where you want to receive exports
- `waitTime`: The time to wait for page loads (in milliseconds)

## Running the Bot

To run the bot, use the following command in the project directory:

```bash
node tawkbot.js
```

The bot will:
1. Open a browser window (visible by default)
2. Log into the Tawk.to dashboard
3. Navigate to the inbox
4. Select and export conversations page by page
5. Send the exports to the specified email

## Troubleshooting

If the bot encounters issues:

- Make sure your login credentials are correct
- Increase the `waitTime` if the page is loading slowly
- Check if the XPATHs have changed (website updates may require path updates)

## Security Note

This script contains sensitive information (login credentials). Never share your script with these details included. Consider using environment variables for sensitive information in a production environment. 