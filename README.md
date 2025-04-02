# JSON to Excel Converter

This application converts Tawk.to JSON chat files to Excel format.

## Features

- Simple GUI interface
- Batch conversion of all JSON files in a directory
- Progress tracking
- Extracts key information from chat files:
  - Chat ID, type, page ID
  - Visitor information (name, email)
  - Location information (country, city)
  - Message count, chat duration (in minutes), rating
  - Timestamps
  - Full conversation text
  - Separated visitor and agent messages
  - Individual messages with sender and timestamp
  - Agent names
  - First/last messages

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Run the application:

```
python json_to_excel.py
```

2. Select the input directory containing your JSON files
3. Select the output directory where the Excel file will be saved
4. Optionally, change the output Excel file name
5. Click "Convert" to start the conversion process
6. Wait for the conversion to complete
7. Open the generated Excel file

## Excel Output Format

The Excel file will contain one row per chat, with the following columns:

- Chat ID
- Type
- Page ID
- Domain
- Visitor Name
- Visitor ID
- Visitor Email
- Country
- City
- Message Count
- Chat Duration (minutes)
- Rating
- Created On
- First Message
- First Visitor Message
- Last Message
- Agent Names
- All Visitor Messages (combined in one cell)
- All Agent Messages (combined in one cell)
- All System Messages (combined in one cell)
- Message 1 Time, Message 1 Sender, Message 1 Text
- Message 2 Time, Message 2 Sender, Message 2 Text
- ... (up to 100 individual messages)
- Conversation (all messages combined)

## Troubleshooting

If you encounter any issues:

1. Make sure the input directory contains valid JSON files
2. Check that you have write permissions for the output directory
3. Ensure all dependencies are installed 