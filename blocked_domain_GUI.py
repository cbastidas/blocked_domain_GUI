import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def load_files():
    global landing_pages, affiliates

    landing_pages_file = filedialog.askopenfilename(title="Select the landing_pages_search.csv file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    affiliates_file = filedialog.askopenfilename(title="Select the MyAffiliates - Affiliate Report.csv file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    try:
        landing_pages = pd.read_csv(landing_pages_file)
        affiliates = pd.read_csv(affiliates_file)
        messagebox.showinfo("Success", "Files loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading files: {e}")

def generate_report():
    domain = domain_entry.get()

    if not domain:
        messagebox.showwarning("Input Error", "Please enter a domain.")
        return

    filtered_landing_pages = landing_pages[landing_pages['Tracking Domain'] == domain][['Landing Page ID', 'Channels']]

    if filtered_landing_pages.empty:
        messagebox.showinfo("No Results", f"There are not Landing Pages for the domain {domain}.")
        return

    merged_data = pd.merge(filtered_landing_pages, affiliates, on='Landing Page ID', how='inner')

    result = merged_data[['Affiliate ID', 'Affiliate', 'Landing Page', 'Landing Page ID', 'Channels', 'Clicks', 'Signups', 'NDC', 'Deposits']]

    # Get the user's Desktop directory
    desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop")
    output_file = os.path.join(desktop_directory, f'{domain}_affiliate_report.xlsx')

    result.to_excel(output_file, index=False, engine='openpyxl')

    messagebox.showinfo("Success", f'File Saved Successfully on the Desktop as {output_file}.')

# Create the main window
root = tk.Tk()
root.title("Affiliate Report Generator")

# Create and place widgets
load_button = tk.Button(root, text="Load CSV Files", command=load_files)
load_button.pack(pady=10)

domain_label = tk.Label(root, text="Insert an Ad-Server Domain Address:")
domain_label.pack(pady=5)
domain_entry = tk.Entry(root, width=50)
domain_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Report", command=generate_report)
generate_button.pack(pady=20)

# Run the application
root.mainloop()
