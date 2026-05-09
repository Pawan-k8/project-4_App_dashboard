# Project_Algo-Main_App_desktop 

## calculation/order/main_dashboard

### Duration: Jan 2025 - Nov 2025

**Git upload : 8 may 2026**

## Summary

This script logs into the Angel One SmartAPI using your stored credentials and a TOTP code, retrieves your live RMS net balance (available funds). 

Then opens a Tkinter GUI. In the GUI you enter a product price, and the script calculates how much you can buy plus profit and loss scenarios. 

After applying a safety buffer, tax rate, and fixed profit/loss percentages on the usable capital.

## Basic Workflow

    main
    |_ start_program
    |  |_ load modules and constants
    |  |_ read API credentials from credentials file
    |  |_ create SmartConnect client with api_key
    |  |_ call fetch_rms_and_calculate()
    |
    |_ fetch_rms_and_calculate
    |  |_ generate TOTP from saved token
    |  |_ login to SmartAPI and get authToken (jwt)
    |  |_ call get_rms_data() to fetch RMS info
    |  |_ parse JSON and extract net_amount (available funds)
    |  |_ call retail_calculator(net_amount)
    |
    |_ retail_calculator (GUI)
       |_ open Tkinter window
       |_ show XT (total available funds)
       |_ take user input: product price
       |_ on "Calculate":
       |  |_ validate input
       |_  |_ compute safe amount, tax, usable amount
       |  |_ compute how many units can be bought
       |  |_ compute profit and loss values
       |  |_ show all results in a table
       |_ keep window running until user closes it


## Tools 
Python, SQL, VS code, Excel, Json

## Libraries used 
Pandas, Matplotlib, tKinter, SmartApi, pyotp, asyncio, Telegram

## API connection
AngelOne API

## Market 
NSE

## Steps

**1-Program starts**

The script imports required libraries, sets constants (safe percent, tax, profit/loss), 
reads your API credentials from credentials.py, 
and creates the SmartConnect client using your api_key.

**2-Login and authentication**

A TOTP code is generated from your stored token using pyotp, 
and this code, along with your username and password, 
is used to call smartApi.generateSession to log in and get a jwtToken (stored as authToken).

**3-Fetch RMS (funds) data**

Using authToken, the code sends an HTTPS GET request to Angel One’s /getRMS endpoint, 
receives JSON data, and extracts the net field, which represents your available funds. 
this value is converted to float and checked to be positive.

**4-Launch the retail calculator GUI**

The retail_calculator(net_amount) function opens a Tkinter window showing your total available funds (XT) 
and provides an input box for you to enter the product price plus a “Calculate” button.

**5-Take user input and validate**

When you click “Calculate”, the program reads the entered product price, 
converts it to a number, and ensures both XT and the price are positive. 
if not, it shows an error message.

**6-Perform safety, tax, and usable-capital calculations**

The script sets aside 4% of XT as a safe buffer, applies the tax rate to the remaining amount, 
and computes the final usable amount (Xa) that can actually be deployed for buying the product.

**7-Calculate units, profit, and loss**

It derives an effective per-unit price by dividing the product price by a fixed multiplier, 
calculates how many units can be bought with Xa, and then computes profit and loss values based
on the configured profit and loss percentages per unit and in total.

**8-Display results in a table**

All computed values (amount before tax, usable amount, buyable units, profit/loss prices and differences) 
are inserted into a Tkinter Treeview table so you can see the breakdown clearly.

**9-Keep the GUI running**

The Tkinter event loop continues running, letting you try different product prices and recalculate, 
until you manually close the window.

## Calculations

Safe money set aside:

    Xs=XT×SAFE_PERCENT=XT×0.04

So 4% is kept as safe capital.

Remaining amount for trading:

    remaining_amount=XT−Xs

Tax on remaining amount:

    Xt=remaining_amount×TAX_RATE

Amount after tax (usable amount):
    
    Xa=remaining_amount−Xt

Profit and loss targets (on usable amount):

    profit=Xa×PROFIT_PERCENT=Xa×0.045
    loss=Xa×LOSS_PERCENT=Xa×0.01

Per-unit price:

    N_price=product_pricePRICE_MULTIPLIER
    N_price=PRICE_MULTIPLIERproduct_price​

So if product price is 100, N_price = 20.

Buyable quantity:
    
    buyable=⌊XaN_price⌋
    buyable=⌊N_priceXa​​⌋

## Archietecture 

    main
    |_ imports_and_constants
    |  |_ http.client, json, tkinter, SmartApi, pyotp, logzero, credentials 
    |  |_ SAFE_PERCENT, TAX_RATE, PROFIT_PERCENT, LOSS_PERCENT, PRICE_MULTIPLIER 
    |
    |_ auth_and_rms_fetch
    |  |_ SmartConnect(api_key) 
    |  |_ fetch_rms_and_calculate()
    |     |_ generate TOTP from wd.Token 
    |     |_ smartApi.generateSession(username, pwd, totp) -> authToken (jwtToken) 
    |     |_ get_rms_data() -> HTTPS GET /getRMS with authToken 
    |     |_ json.loads(response), check status and data 
    |     |_ extract net_amount = data["net"], validate > 0 
    |     |_ retail_calculator(net_amount) 
    |
    |_ retail_calculator(XT)
       |_ build Tk root window "Retail Owner Calculator" 
       |_ label showing XT and entry for product_price 
       |_ "Calculate" button -> calculate_profit_loss() 
       |  |_ read and validate product_price > 0 
       |  |_ Xs = XT * SAFE_PERCENT (safe amount) 
       |  |_ remaining_amount = XT - Xs 
       |  |_ Xt = remaining_amount * TAX_RATE (tax) 
       |  |_ Xa = remaining_amount - Xt (usable amount) 
       |  |_ profit = Xa * PROFIT_PERCENT, loss = Xa * LOSS_PERCENT 
       |  |_ N_price = product_price / PRICE_MULTIPLIER 
       |  |_ buyable = int(Xa / N_price) 
       |  |_ compute product_profit_at_buy/sell, product_loss_at_buy/sell 
       |  |_ value_profit, value_loss per unit 
       |  |_ update_results_table() to fill Treeview 
       |
       |_ helper: update_results_table(), clear_fields() 
       |_ root.mainloop() 

## Results:

When run successfully:
It logs in to Angel One using your API key, username, password, and TOTP.
It fetches your current RMS net value (your net cash / margin available as reported by the broker).
Then opens a GUI that shows this XT amount and lets you enter a product’s price.

After clicking “Calculate”, it shows, in a table:

  1. Amount kept safe
  2. Amount after tax
  3. Profit and loss targets for the usable amount
  4. Effective per-unit price
  5. How many units you can buy
  6. Profit/loss per unit in both directions.

## Conclusion:

1. The code tightly couples a brokerage API (SmartAPI) with a local risk/profit calculator GUI.
2. It enforces safety (4% buffer), taxes, and fixed profit/loss percentages as part of a simple risk management model.
3. The RMS net value becomes the dynamic input for the calculator, so you always base your calculations on your actual available capital.
