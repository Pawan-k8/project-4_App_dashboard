import http.client
import json
import tkinter as tk
from tkinter import ttk, messagebox
from SmartApi import SmartConnect
import pyotp
from logzero import logger
import credentials as wd

# Constants
SAFE_PERCENT = 0.04
TAX_RATE = 0.008  # actual tax rate is 0.0055
PROFIT_PERCENT = 0.045
LOSS_PERCENT = 0.01
PRICE_MULTIPLIER = 5

def get_rms_data():
    conn = http.client.HTTPSConnection("apiconnect.angelone.in")
    payload = ''
    headers = {
        'Authorization': f'{authToken}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
        'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
        'X-MACAddress': 'MAC_ADDRESS',
        'X-PrivateKey': wd.api_key
    }
    conn.request("GET", "/rest/secure/angelbroking/user/v1/getRMS", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return data

def fetch_rms_and_calculate():
    try:
        # Generate TOTP
        token = wd.Token
        totp = pyotp.TOTP(token).now()

        # Authenticate SmartConnect
        data = smartApi.generateSession(username, pwd, totp)
        if not data['status']:
            logger.error(data)
            raise Exception("Login failed")

        global authToken
        authToken = data['data']['jwtToken']

        # Fetch RMS data
        rms_data = get_rms_data()
        rms_data_parsed = json.loads(rms_data)
        print(rms_data)
                
        if rms_data_parsed.get("status") and "data" in rms_data_parsed:
            rms_data = rms_data_parsed["data"]
            net_amount = rms_data.get("net")  # Fetch the 'net' field
        
            if net_amount is None:
                raise ValueError("Net amount is missing in RMS data")
        
            try:
                net_amount = float(net_amount)  # Convert to float for calculations
            except ValueError:
                raise ValueError(f"Invalid net amount format: {net_amount}")
        
            if net_amount <= 0:
                raise ValueError("Net amount must be greater than zero")
        
            # Pass net_amount to the retail calculator
            retail_calculator(net_amount)
        else:
            raise ValueError("RMS data is not valid or incomplete")

    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error fetching RMS data: {e}")
        messagebox.showerror("Error", f"Error: {e}")

def retail_calculator(XT):
    root = tk.Tk()
    root.title("Retail Owner Calculator")

    def calculate_profit_loss():
        try:
            product_price = float(entry_product_price.get())

            if XT <= 0 or product_price <= 0:
                raise ValueError("Values must be positive numbers")

            # Calculations
            Xs = XT * SAFE_PERCENT
            remaining_amount = XT - Xs

            Xt = remaining_amount * TAX_RATE
            Xa = remaining_amount - Xt

            profit = Xa * PROFIT_PERCENT
            loss = Xa * LOSS_PERCENT

            N_price = product_price / PRICE_MULTIPLIER
            buyable = int(Xa / N_price)

            product_profit_at_buy = N_price * (1 + PROFIT_PERCENT)
            product_profit_at_sell = N_price * (1 - PROFIT_PERCENT)
            product_loss_at_buy = N_price * (1 - LOSS_PERCENT)
            product_loss_at_sell = N_price * (1 + LOSS_PERCENT)
            value_profit = product_profit_at_buy - N_price
            value_loss = product_loss_at_buy - N_price

            # Update results table
            update_results_table({
                "Amount Before Tax (Xts)": f"{remaining_amount:.2f}",
                "Remaining Amount (Xa)": f"{Xa:.2f}",
                f"Profit ({PROFIT_PERCENT*100}% of Xa)": f"{profit:.2f}",
                f"Loss ({LOSS_PERCENT*100}% of Xa)": f"{loss:.2f}",
                "Price per Product (N_price)": f"{N_price:.2f}",
                "Products Buyable": f"{buyable}",
                "Product Buy Profit": f"{product_profit_at_buy:.2f}",
                "Product Sell Profit": f"{product_profit_at_sell:.2f}",
                "Product Buy Loss": f"{product_loss_at_buy:.2f}",
                "Product Sell Loss": f"{product_loss_at_sell:.2f}",
                "Value Profit": f"{value_profit:.2f}",
                "Value Loss": f"{value_loss:.2f}"
            })

        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid positive numbers")
            clear_fields()

    def update_results_table(results):
        for row in tree.get_children():
            tree.delete(row)
        for description, value in results.items():
            tree.insert("", "end", values=(description, value))

    def clear_fields():
        entry_product_price.delete(0, tk.END)
        for row in tree.get_children():
            tree.delete(row)

    # Input Section
    ttk.Label(root, text=f"Total sum of money (XT): {XT}").pack(pady=5)
    ttk.Label(root, text="Price of the product:").pack(pady=5)
    entry_product_price = ttk.Entry(root, width=20)
    entry_product_price.pack(pady=5)

    ttk.Button(root, text="Calculate", command=calculate_profit_loss).pack(pady=5)
    
    # Results Table
    tree = ttk.Treeview(root, columns=("Description", "Value"), show="headings")
    tree.heading("Description", text="Description")
    tree.heading("Value", text="Value")
    tree.pack(pady=10)

    root.mainloop()

# SmartApi credentials
api_key = wd.api_key
username = wd.username
pwd = wd.pwd
smartApi = SmartConnect(api_key)

# Fetch RMS data and calculate
fetch_rms_and_calculate()
