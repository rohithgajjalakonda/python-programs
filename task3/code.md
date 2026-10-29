Here is a complete system design, algorithm, Mermaid flowchart, Python implementation, and sample test case for the **Retail Billing with Multiple Discount Rules** system.

---

## 1. Problem Statement

Modern retail checkout and invoicing systems require sophisticated calculation engines that handle heterogeneous product categories, dynamic tax structures, conditional promotional discounts, and safety caps to prevent excessive revenue loss.

The system must process a shopping cart containing multiple items, apply category-specific taxes, evaluate tiered threshold discounts based on the purchase subtotal, enforce a maximum concession limit (cap) on total discounts, and generate a clean, itemized invoice.

### **Rules & Constraints:**

1. **Category-Specific Taxes:** Different product categories attract different tax rates (e.g., Groceries: 5%, Electronics: 18%, Clothing: 12%).
2. **Threshold Discounts:** Progressive discount rates based on total subtotal value (e.g., Orders over ₹5,000 get 5% off; orders over ₹10,000 get 10% off).
3. **Maximum Concession Limit:** A safety cap that restricts the maximum total discount amount a customer can receive in a single transaction (e.g., capped at ₹1,500).
4. **Final Bill Computation:** $\text{Final Total} = \text{Subtotal} - \text{Applied Discount} + \text{Total Taxes}$.

---

## 2. Algorithm

1. **Initialize Inputs:** Load cart items (product name, category, unit price, quantity) and system rules (tax rates, discount tiers, max discount cap).
2. **Calculate Item Subtotals & Taxes:**
* For each item, compute `Item Subtotal = Unit Price * Quantity`.
* Look up the category tax rate and compute `Item Tax = Item Subtotal * Tax Rate`.
* Accumulate total subtotal and total taxes.


3. **Evaluate Threshold Discounts:**
* Compare total subtotal against configured spending thresholds in descending order.
* Determine the applicable discount percentage.
* Calculate `Raw Discount = Subtotal * Discount Percentage`.


4. **Enforce Maximum Concession Limit:**
* Compare `Raw Discount` against the maximum allowable discount cap.
* If `Raw Discount > Max Cap`, set `Final Discount = Max Cap`. Otherwise, `Final Discount = Raw Discount`.


5. **Compute Net Total:**
* `Net Payable = Subtotal - Final Discount + Total Tax`.


6. **Generate Invoice:** Format and print the itemized bill statement.

---

## 3. Flowchart (Mermaid)

```mermaid
graph TD
    Start([Start]) --> Input[Input Cart Items & Pricing Rules]
    Input --> LoopStart{More Cart Items?}
    
    LoopStart -- Yes --> CalcItem[Calculate Item Subtotal & Category Tax] --> LoopStart
    LoopStart -- No --> SumTotals[Sum Total Subtotal & Total Taxes]
    
    SumTotals --> CheckThreshold{Evaluate Subtotal against Threshold Tiers}
    CheckThreshold --> CalcDiscount[Calculate Raw Discount Percentage]
    
    CalcDiscount --> CheckCap{Raw Discount > Max Concession Cap?}
    CheckCap -- Yes --> ApplyCap[Cap Discount to Maximum Limit] --> ComputeNet
    CheckCap -- No --> UseRaw[Use Raw Discount Value] --> ComputeNet
    
    ComputeNet[Compute Final Total = Subtotal - Discount + Tax] --> Output[Generate Itemized Invoice Statement]
    Output --> End([End])

```

---

## 4. Python Source Code

```python
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

```

---

## 5. Sample Input & Output

### **Sample Input Configuration**

* **Customer Name:** Rohan Malhotra
* **Cart Items:**
1. Wireless Earbuds (`Electronics`): 2 units @ ₹2,500.00 each
2. Organic Rice 5kg (`Groceries`): 3 units @ ₹600.00 each
3. Cotton Denim Jeans (`Clothing`): 2 units @ ₹1,800.00 each


* **Tax Rules:** Groceries (5%), Clothing (12%), Electronics (18%)
* **Discount Tiers:**
* Subtotal $\ge$ ₹10,000 $\rightarrow$ 15% discount
* Subtotal $\ge$ ₹5,000 $\rightarrow$ 8% discount


* **Maximum Concession Limit:** ₹1,200.00 cap

---

### **Sample Output Invoice**

```text
==================================================
              RETAIL TAX INVOICE
==================================================
Customer Name : Rohan Malhotra
--------------------------------------------------
ITEM DESCRIPTION        QTY  UNIT(₹)   TOTAL(₹)   TAX(₹)
--------------------------------------------------
Wireless Earbuds     2    ₹2500.00  ₹5000.00    ₹900.00
Organic Rice (5kg)   3    ₹600.00   ₹1800.00    ₹90.00
Cotton Denim Jeans   2    ₹1800.00  ₹3600.00    ₹432.00
--------------------------------------------------
SUBTOTAL                               : ₹10,400.00
Threshold Discount Applied (15.0%)     : -₹1,560.00
[NOTE: Discount capped at maximum limit of ₹1,200.00]
FINAL DISCOUNT AMOUNT                  : -₹1,200.00
TOTAL TAX                              : +₹1,422.00
==================================================
NET PAYABLE AMOUNT                     : ₹10,622.00
==================================================

```
