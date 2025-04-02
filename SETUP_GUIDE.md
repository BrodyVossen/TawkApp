# Tawk.to Bot Setup Guide

This guide will help you set up and run the Tawk.to Dashboard Automation Bot on your computer.

## System Requirements

- Windows 10 or later
- Node.js version 14 or later
- Internet connection

## Installation Steps

1. **Install Node.js** (if not already installed):
   - Download Node.js from [nodejs.org](https://nodejs.org/)
   - Choose the LTS (Long Term Support) version
   - Run the installer and follow the instructions
   - Verify installation by opening Command Prompt and typing:
     ```
     node --version
     npm --version
     ```

2. **Set up the Bot:**
   - Extract the bot files to a folder on your computer
   - Open Command Prompt as Administrator
   - Navigate to the folder where you extracted the bot files:
     ```
     cd path\to\tawkbot\folder
     ```
   - Install required dependencies:
     ```
     npm install
     ```
   - Install Playwright browsers:
     ```
     npx playwright install chromium
     ```

## Running the Bot

### Option 1: Using the Simple Version (with hardcoded credentials)

1. Double-click the `run-bot.bat` file
2. A browser window will open and the bot will start running
3. You'll see progress in the command prompt window

### Option 2: Using the Secure Version (with environment variables)

1. Edit the `run-bot-secure.bat` file if you want to change any settings
2. Double-click the `run-bot-secure.bat` file
3. A browser window will open and the bot will start running
4. You'll see progress in the command prompt window

## Customizing the Bot

### To change login credentials or export email:

1. For the simple version:
   - Open `tawkbot.js` in a text editor
   - Modify the values in the config section

2. For the secure version:
   - Open `run-bot-secure.bat` in a text editor
   - Update the environment variable values

### To change wait times:

If the bot is moving too fast or too slow for your internet connection:
- Increase or decrease the `waitTime` value (in milliseconds)
- 3000 = 3 seconds wait time

## Troubleshooting

### Common Issues:

1. **Bot cannot log in:**
   - Verify your login credentials
   - Make sure you have internet access
   - Check if the Tawk.to login page has changed

2. **Bot cannot find elements:**
   - The website layout may have changed
   - Try increasing the wait time
   - You may need to update the XPATHs in the script

3. **Browser crashes:**
   - Make sure you have enough system resources
   - Try closing other applications
   - Restart your computer and try again

### Getting Help:

If you encounter persistent issues, please provide:
- Screenshots of the error
- Description of what happened
- Any error messages from the command prompt window

## Security Considerations

The simple version of the bot (`tawkbot.js`) contains hardcoded credentials. 
For better security, prefer using the secure version (`tawkbot-secure.js`) which uses environment variables. 