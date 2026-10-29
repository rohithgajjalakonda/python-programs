
class RetailBillingSystem:
    def __init__(self, category_taxes, discount_tiers, max_discount_cap):
        self.category_taxes = category_taxes  # Dictionary mapping category -> tax rate (percentage)
        self.discount_tiers = sorted(discount_tiers, key=lambda x: x['threshold'], reverse=True) # List of dicts: threshold, rate
        self.max_discount_cap = max_discount_cap

    def generate_invoice(self, customer_name, cart_items):
        subtotal = 0.0
        total_tax = 0.0
        itemIZED_details = []

        # 1. Calculate Subtotal and Category Taxes per item
        for item in cart_items:
            name = item['name']
            category = item['category']
            unit_price = item['unit_price']
            qty = item['quantity']
            
            item_subtotal = unit_price * qty
            subtotal += item_subtotal
            
            # Get category tax rate (default to 10% if category not found)
            tax_rate = self.category_taxes.get(category, 10.0) / 100.0
            item_tax = item_subtotal * tax_rate
            total_tax += item_tax
            
            itemIZED_details.append({
                "name": name,
                "category": category,
                "qty": qty,
                "unit_price": unit_price,
                "subtotal": item_subtotal,
                "tax": item_tax
            })

        # 2. Evaluate Threshold Discounts
        applied_discount_rate = 0.0
        for tier in self.discount_tiers:
            if subtotal >= tier['threshold']:
                applied_discount_rate = tier['rate']
                break
                
        raw_discount = subtotal * (applied_discount_rate / 100.0)

        # 3. Enforce Maximum Concession Limit (Cap)
        final_discount = min(raw_discount, self.max_discount_cap)
        is_capped = raw_discount > self.max_discount_cap

        # 4. Compute Final Net Total
        net_total = subtotal - final_discount + total_tax

        # 5. Build Formatted Invoice Output
        invoice = f"""
==================================================
              RETAIL TAX INVOICE
==================================================
Customer Name : {customer_name}
--------------------------------------------------
ITEM DESCRIPTION        QTY  UNIT(₹)   TOTAL(₹)   TAX(₹)
--------------------------------------------------"""
        
        for i in itemIZED_details:
            invoice += f"\n{i['name']:<20} {i['qty']:<4} ₹{i['unit_price']:<7.2f} ₹{i['subtotal']:<9.2f} ₹{i['tax']:.2f}"

        invoice += f"""
--------------------------------------------------
SUBTOTAL                               : ₹{subtotal:,.2f}
Threshold Discount Applied ({applied_discount_rate}%) : -₹{raw_discount:,.2f}"""

        if is_capped:
            invoice += f"\n[NOTE: Discount capped at maximum limit of ₹{self.max_discount_cap:,.2f}]"

        invoice += f"""
FINAL DISCOUNT AMOUNT                  : -₹{final_discount:,.2f}
TOTAL TAX                              : +₹{total_tax:,.2f}
==================================================
NET PAYABLE AMOUNT                     : ₹{net_total:,.2f}
==================================================
"""
        return invoice

# ==========================================
# Sample Execution
# ==========================================
if __name__ == "__main__":
    # Configuration Rules
    category_taxes = {
        "Groceries": 5.0,      # 5% tax
        "Electronics": 18.0,   # 18% tax
        "Clothing": 12.0       # 12% tax
    }
    
    # Threshold tiers: Spend >= 10,000 -> 15% off; Spend >= 5,000 -> 8% off
    discount_tiers = [
        {"threshold": 10000.0, "rate": 15.0},
        {"threshold": 5000.0, "rate": 8.0}
    ]
    
    max_discount_cap = 1200.0  # Maximum concession limit
    
    billing_system = RetailBillingSystem(category_taxes, discount_tiers, max_discount_cap)
    
    # Sample Cart Input
    customer_cart = [
        {"name": "Wireless Earbuds", "category": "Electronics", "unit_price": 2500.0, "quantity": 2},
        {"name": "Organic Rice (5kg)", "category": "Groceries", "unit_price": 600.0, "quantity": 3},
        {"name": "Cotton Denim Jeans", "category": "Clothing", "unit_price": 1800.0, "quantity": 2}
    ]
    
    print(billing_system.generate_invoice("Rohan Malhotra", customer_cart))
