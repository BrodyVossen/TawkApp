import os
import json
import pandas as pd
from datetime import datetime
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import re

class JsonToExcelConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON to Excel Converter")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input directory selection
        input_frame = ttk.LabelFrame(main_frame, text="Input Directory (JSON Files)", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        self.input_dir_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_dir_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(input_frame, text="Browse", command=self.browse_input_dir).pack(side=tk.RIGHT)
        
        # Output directory selection
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory (Excel File)", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        self.output_dir_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(output_frame, text="Browse", command=self.browse_output_dir).pack(side=tk.RIGHT)
        
        # Output file name
        file_name_frame = ttk.Frame(main_frame, padding="5")
        file_name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_name_frame, text="Output File Name:").pack(side=tk.LEFT, padx=(5, 0))
        self.output_file_var = tk.StringVar(value="tawk_chats.xlsx")
        ttk.Entry(file_name_frame, textvariable=self.output_file_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Label(file_name_frame, text=".xlsx").pack(side=tk.LEFT)
        
        # Progress area
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.status_var).pack(fill=tk.X)
        
        # Status count labels
        self.count_frame = ttk.Frame(progress_frame)
        self.count_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.count_frame, text="Processed:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.processed_var = tk.StringVar(value="0")
        ttk.Label(self.count_frame, textvariable=self.processed_var).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(self.count_frame, text="Total:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        self.total_var = tk.StringVar(value="0")
        ttk.Label(self.count_frame, textvariable=self.total_var).grid(row=0, column=3, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Convert", command=self.start_conversion).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        
    def browse_input_dir(self):
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_dir_var.set(directory)
            
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def start_conversion(self):
        input_dir = self.input_dir_var.get().strip()
        output_dir = self.output_dir_var.get().strip()
        output_file = self.output_file_var.get().strip()
        
        if not input_dir:
            messagebox.showerror("Error", "Please select input directory")
            return
            
        if not output_dir:
            messagebox.showerror("Error", "Please select output directory")
            return
            
        if not output_file:
            messagebox.showerror("Error", "Please enter output file name")
            return
            
        if not output_file.endswith('.xlsx'):
            output_file += '.xlsx'
            
        output_path = os.path.join(output_dir, output_file)
        
        # Start conversion in a separate thread
        threading.Thread(target=self.convert_json_to_excel, args=(input_dir, output_path), daemon=True).start()
        
    def convert_json_to_excel(self, input_dir, output_path):
        try:
            # Reset progress
            self.progress_var.set(0)
            self.status_var.set("Scanning files...")
            self.root.update_idletasks()
            
            # Get list of JSON files
            json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
            total_files = len(json_files)
            
            if total_files == 0:
                self.status_var.set("No JSON files found in the input directory")
                messagebox.showinfo("Info", "No JSON files found in the input directory")
                return
                
            self.total_var.set(str(total_files))
            
            # Prepare data structures for Excel
            chat_data = []
            
            # Process each JSON file
            for i, file_name in enumerate(json_files):
                try:
                    file_path = os.path.join(input_dir, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Extract chat information
                    chat_info = self.extract_chat_info(data)
                    chat_data.append(chat_info)
                    
                    # Update progress
                    self.processed_var.set(str(i + 1))
                    self.progress_var.set((i + 1) / total_files * 100)
                    self.status_var.set(f"Processing: {file_name}")
                    self.root.update_idletasks()
                    
                except Exception as e:
                    print(f"Error processing {file_name}: {str(e)}")
                    continue
            
            # Convert to DataFrame
            self.status_var.set("Creating Excel file...")
            df = pd.DataFrame(chat_data)
            
            # Save to Excel
            df.to_excel(output_path, index=False)
            
            self.status_var.set(f"Completed! Excel file saved to: {output_path}")
            messagebox.showinfo("Success", f"Conversion completed!\nExcel file saved to:\n{output_path}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during conversion:\n{str(e)}")
    
    def extract_chat_info(self, data):
        """Extract relevant information from the chat JSON data"""
        chat_info = {
            'Chat ID': data.get('id', ''),
            'Type': data.get('type', ''),
            'Page ID': data.get('pageId', ''),
            'Domain': data.get('domain', ''),
            'Visitor Name': data.get('visitor', {}).get('name', ''),
            'Visitor ID': data.get('visitor', {}).get('id', ''),
            'Visitor Email': data.get('visitor', {}).get('email', ''),
            'Country': data.get('location', {}).get('countryCode', ''),
            'City': data.get('location', {}).get('city', ''),
            'Message Count': data.get('messageCount', 0),
            'Chat Duration (minutes)': round(data.get('chatDuration', 0) / 60.0, 2),  # Convert seconds to minutes
            'Rating': data.get('rating', 0),
            'Created On': data.get('createdOn', ''),
            'First Message': '',
            'First Visitor Message': '',
            'Last Message': '',
            'Agent Names': '',
            'All Visitor Messages': '',
            'All Agent Messages': '',
            'All System Messages': '',
            'Conversation': ''
        }
        
        # Extract message information
        messages = data.get('messages', [])
        
        if messages:
            # Get first message
            chat_info['First Message'] = messages[0].get('msg', '') if messages else ''
            
            # Get first visitor message
            for msg in messages:
                if msg.get('sender', {}).get('t') == 'v':
                    chat_info['First Visitor Message'] = msg.get('msg', '')
                    break
            
            # Get last message
            chat_info['Last Message'] = messages[-1].get('msg', '') if messages else ''
            
            # Get all agent names
            agent_names = set()
            for msg in messages:
                sender = msg.get('sender', {})
                if sender.get('t') == 'a' and 'n' in sender:
                    agent_names.add(sender['n'])
            
            chat_info['Agent Names'] = ', '.join(agent_names)
            
            # Create separate lists for different types of messages
            visitor_messages = []
            agent_messages = []
            system_messages = []
            
            # Compile full conversation and separate by sender type
            conversation = []
            
            # Create individual message columns for every message
            # We'll limit to 100 messages to avoid too many columns
            max_messages = min(len(messages), 100) 
            
            for idx, msg in enumerate(messages):
                sender_type = msg.get('sender', {}).get('t', '')
                sender_name = msg.get('sender', {}).get('n', '')
                message_text = msg.get('msg', '')
                message_time = msg.get('time', '')
                
                # Skip empty messages
                if not message_text or not sender_type:
                    continue
                
                # Format message with time and sender
                if sender_type == 's':
                    sender_prefix = "System: "
                    formatted_msg = f"[{message_time}] {sender_prefix}{message_text}"
                    system_messages.append(formatted_msg)
                elif sender_type == 'v':
                    sender_prefix = "Visitor: "
                    formatted_msg = f"[{message_time}] {sender_prefix}{message_text}"
                    visitor_messages.append(formatted_msg)
                elif sender_type == 'a':
                    sender_prefix = f"Agent ({sender_name}): "
                    formatted_msg = f"[{message_time}] {sender_prefix}{message_text}"
                    agent_messages.append(formatted_msg)
                else:
                    formatted_msg = f"[{message_time}] {message_text}"
                
                # Add to full conversation
                conversation.append(formatted_msg)
                
                # Add individual message to columns if within limit
                if idx < max_messages:
                    chat_info[f'Message {idx+1} Time'] = message_time
                    chat_info[f'Message {idx+1} Sender'] = f"{sender_prefix.strip()}"
                    chat_info[f'Message {idx+1} Text'] = message_text
            
            # Add the combined messages
            chat_info['All Visitor Messages'] = "\n".join(visitor_messages)
            chat_info['All Agent Messages'] = "\n".join(agent_messages)
            chat_info['All System Messages'] = "\n".join(system_messages)
            chat_info['Conversation'] = "\n".join(conversation)
        
        return chat_info

def main():
    root = tk.Tk()
    app = JsonToExcelConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 