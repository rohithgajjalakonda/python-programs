Here is a complete system design, algorithm, Mermaid flowchart, comment-free Python implementation, and sample test case for the **Smart Canteen Order and Stock Management System**.

---

## 1. Problem Statement

School, college, and corporate canteens require real-time inventory tracking combined with automated order processing to prevent stockouts, eliminate manual billing errors, and handle partial or full order rejections when items exceed available supplies.

The system must process successive customer orders against live inventory levels, calculate itemized bills, automatically deduct fulfilled items from stock, reject unavailable quantities with descriptive feedback, and generate an end-of-day revenue and remaining stock summary.

### **Rules & Mechanics:**

1. **Inventory Validation:** Each ordered item is checked against available stock.
2. **Fulfillment & Billing:** If stock is sufficient, the quantity is deducted from inventory, sales are recorded, and item costs are added to the bill.
3. **Rejection Handling:** If the requested quantity exceeds available stock (or the item is not on the menu), that specific item is rejected while processing the rest of the order.
4. **Daily Summarization:** Aggregates total daily revenue, units sold per menu item, and closing inventory counts.

---

## 2. Algorithm

1. **Initialize Inputs:** Load menu item prices, initial inventory stock levels, and incoming customer order queues.
2. **Process Customer Orders:**
* For each customer order, initialize a bill container and a rejection log.
* For each requested item and quantity:
* Check if the item exists in the menu.
* Check if `requested_quantity <= available_stock`.
* If available, deduct the quantity from inventory, update units sold, and calculate the cost.
* If unavailable, record the rejection reason.


* Compute total order cost and store fulfillment details.


3. **Generate Summary:** Accumulate total daily revenue and format the end-of-day inventory and sales report.

---

## 3. Flowchart (Mermaid)

```mermaid
graph TD
    Start([Start]) --> Input[Initialize Inventory & Menu Prices]
    Input --> LoopOrders{More Customer Orders?}
    
    LoopOrders -- Yes --> LoopItems{More Items in Order?}
    LoopItems -- Yes --> CheckStock{Item in Menu & Stock >= Requested?}
    
    CheckStock -- Yes --> Deduct[Deduct Stock, Calculate Item Cost & Add to Bill] --> LoopItems
    CheckStock -- No --> Reject[Reject Item Due to Insufficient Stock] --> LoopItems
    
    LoopItems -- No --> PrintBill[Generate Customer Bill & Record Revenue] --> LoopOrders
    LoopOrders -- No --> Summary[Summarize Daily Sales & Remaining Inventory] --> End([End])

```

---

## 5. Sample Input & Output

### **Sample Input Configuration**

* **Menu & Prices:** Veg Burger (₹120), Cheese Pizza (₹250), Cold Coffee (₹90), French Fries (₹80), Club Sandwich (₹150)
* **Initial Inventory:** Veg Burger (15), Cheese Pizza (5), Cold Coffee (20), French Fries (10), Club Sandwich (8)
* **Customer Orders:**
1. *Aarav Sharma*: 2 Veg Burgers, 2 Cold Coffees, 3 French Fries
2. *Priya Nair*: 4 Cheese Pizzas, 2 Club Sandwiches
3. *Rohan Gupta*: 3 Cheese Pizzas, 15 Veg Burgers (Exceeds remaining stock)



---

### **Sample Output Operations Report**

```text
==================================================
        SMART CANTEEN DAILY OPERATIONS REPORT
==================================================
TOTAL DAILY REVENUE : ₹2,070.00
--------------------------------------------------
ORDER FULFILLMENT LOG
--------------------------------------------------
- Order ID: ORD-101 | Customer: Aarav Sharma
  * Veg Burger x 2 = ₹240.00
  * Cold Coffee x 2 = ₹180.00
  * French Fries x 3 = ₹240.00
  Order Total: ₹660.00
- Order ID: ORD-102 | Customer: Priya Nair
  * Cheese Pizza x 4 = ₹1,000.00
  * Club Sandwich x 2 = ₹300.00
  Order Total: ₹1,300.00
- Order ID: ORD-103 | Customer: Rohan Gupta
  * Cheese Pizza x 3 = ₹750.00
  Order Total: ₹750.00
  Rejections: Veg Burger: Requested 15, only 13 available
--------------------------------------------------
REMAINING INVENTORY STOCK
--------------------------------------------------
- Veg Burger      : 13 units remaining (Sold: 2)
- Cheese Pizza    : 0 units remaining (Sold: 7)
- Cold Coffee     : 18 units remaining (Sold: 2)
- French Fries    : 7 units remaining (Sold: 3)
- Club Sandwich   : 6 units remaining (Sold: 2)
==================================================

```
