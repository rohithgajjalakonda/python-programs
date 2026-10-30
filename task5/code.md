Here is a complete system design, algorithm, Mermaid flowchart, Python implementation, and sample test case for the **Warehouse Inventory Reconciliation System**.

---

## 1. Problem Statement

Warehouses handle thousands of items daily, making inventory shrinkage, unrecorded damages, counting errors, and stockouts major operational risks. An automated inventory reconciliation system is required to compare physical audit counts (reported closing stock) against calculated system expectations (opening stock + incoming shipments - dispatched orders), detect discrepancies, and compute automated replenishment orders when stock falls below pre-defined safety thresholds.

### **Rules & Mechanics:**

1. **Expected Stock Calculation:** $\text{Expected Closing} = \text{Opening Stock} + \text{Incoming} - \text{Dispatched}$.
2. **Discrepancy Detection:** $\text{Discrepancy} = \text{Reported Closing Stock} - \text{Expected Closing}$.
* *Positive Discrepancy:* Surplus inventory (unrecorded stock found during audit).
* *Negative Discrepancy:* Shrinkage/loss (missing stock due to theft, damage, or miscount).
* *Zero Discrepancy:* Perfect match.


3. **Replenishment Analysis:** If $\text{Reported Closing Stock} \le \text{Reorder Level}$, calculate the necessary replenishment quantity to restore inventory to the target maximum stock level.

---

## 2. Algorithm

1. **Initialize Inputs:** Load warehouse inventory records including product ID, name, opening stock, incoming quantities, dispatched quantities, reported physical closing stock, reorder level, and maximum stock capacity.
2. **Process Each Product:**
* Compute `Expected Closing Stock = Opening + Incoming - Dispatched`.
* Compute `Discrepancy = Reported Closing - Expected Closing`.
* Evaluate `Discrepancy Status` (Balanced, Shrinkage/Loss, or Surplus).


3. **Evaluate Replenishment Requirements:**
* Check if `Reported Closing <= Reorder Level`.
* If true, calculate `Replenishment Quantity = Maximum Capacity - Reported Closing`. Otherwise, replenishment is 0.


4. **Generate Audit & Replenishment Report:** Compile all itemized metrics into a structured summary statement.

---

## 3. Flowchart (Mermaid)

```mermaid
graph TD
    Start([Start]) --> Input[Input Product Inventory Records & Thresholds]
    Input --> LoopStart{More Products?}
    
    LoopStart -- Yes --> CalcExpected[Calculate Expected Closing = Opening + Incoming - Dispatched]
    CalcExpected --> CalcDisc[Calculate Discrepancy = Reported Closing - Expected Closing]
    CalcDisc --> CheckReorder{Reported Closing <= Reorder Level?}
    
    CheckReorder -- Yes --> CalcReplen[Calculate Replenishment = Max Capacity - Reported Closing] --> LoopStart
    CheckReorder -- No --> NoReplen[Replenishment Required = 0] --> LoopStart
    
    LoopStart -- No --> Output[Generate Reconciliation & Replenishment Report]
    Output --> End([End])

```

---


## 5. Sample Input & Output

### **Sample Input Configuration**

* **Warehouse Location:** `Central Distribution Hub - North`
* **Inventory Records:**
1. *Wireless Mechanical Keyboard* (`P-101`): Opening = 150, Incoming = 200, Dispatched = 180, Reported = 165, Reorder Level = 50, Max Capacity = 300
2. *HD 27-inch Monitor* (`P-102`): Opening = 45, Incoming = 30, Dispatched = 60, Reported = 15, Reorder Level = 25, Max Capacity = 100
3. *USB-C Fast Charging Cable* (`P-103`): Opening = 500, Incoming = 1000, Dispatched = 1250, Reported = 255, Reorder Level = 100, Max Capacity = 800
4. *Ergonomic Office Chair* (`P-104`): Opening = 30, Incoming = 10, Dispatched = 35, Reported = 5, Reorder Level = 15, Max Capacity = 50



---

### **Sample Output Report**

```text
==================================================
        WAREHOUSE INVENTORY RECONCILIATION
==================================================
Warehouse Location : Central Distribution Hub - North
Total Items Audited: 4
Discrepancies Flagged: 2
--------------------------------------------------
ITEM AUDIT BREAKDOWN
--------------------------------------------------
- [P-101] Wireless Mechanical Keyboard
  Expected Closing : 170 | Reported Audit: 165
  Discrepancy      : Shrinkage (-5) ⚠️
  REPLENISHMENT    : Stock levels healthy
- [P-102] HD 27-inch Monitor
  Expected Closing : 15 | Reported Audit: 15
  Discrepancy      : Balanced ✅
  REPLENISHMENT    : Order 85 units (Below reorder threshold) 🚨
- [P-103] USB-C Fast Charging Cable
  Expected Closing : 250 | Reported Audit: 255
  Discrepancy      : Surplus (+5)
  REPLENISHMENT    : Stock levels healthy
- [P-104] Ergonomic Office Chair
  Expected Closing : 5 | Reported Audit: 5
  Discrepancy      : Balanced ✅
  REPLENISHMENT    : Order 45 units (Below reorder threshold) 🚨
--------------------------------------------------
SUMMARY ACTIONS REQUIRED
--------------------------------------------------
Total Reorder Purchase Orders Triggered : 2 Products
Total Units Needed for Replenishment    : 130 units
==================================================

```
