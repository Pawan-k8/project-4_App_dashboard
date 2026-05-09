def calculate_profit_loss(XT, tax_rate=0.18, safe_percent=0.04, profit_percent=0.13, loss_percent=0.05):
    # Step 1: Calculate Xs (safe keeping)
    Xs = XT * safe_percent
    remaining_amount = XT - Xs
    
    # Step 2: Apply tax calculation Xt (assuming tax rate is provided as a percentage)
    Xt = remaining_amount * tax_rate
    remaining_after_tax = remaining_amount - Xt
    
    # Step 3: Calculate profit and loss based on remaining amount (Xa)
    Xa = remaining_after_tax
    profit = Xa * profit_percent
    loss = Xa * loss_percent
    
    print(f"Remaining amount (Xa) after tax: {Xa}")
    print(f"Profit (13% of Xa): {profit}")
    print(f"Loss (-5% of Xa): {loss}")
    
    # Step 4: Ask for the price of the product
    product_price = float(input("Enter the price of the product: "))
    
    # Step 5: Calculate N_price and how many products can be bought
    N_price = product_price / 5
    buyable = int(Xa / N_price)
    
    print(f"Price per product (N_price) after dividing by 5: {N_price}")
    print(f"Number of products that can be bought: {buyable}")
    
    # Step 6: Calculate profit and loss for each product
    product_profit = N_price * (1 + profit_percent)
    product_loss = N_price * (1 - loss_percent)
    
    print(f"Price per product with 13% profit: {product_profit}")
    print(f"Price per product with -5% loss: {product_loss}")

# Example usage:
XT = float(input("Enter the total sum of money (XT): "))
calculate_profit_loss(XT)
