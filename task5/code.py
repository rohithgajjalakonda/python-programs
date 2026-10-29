class InventoryReconciliationSystem:
    def __init__(self):
        pass

    def reconcile_inventory(self, warehouse_name, products):
        reconciliation_records = []
        total_discrepancies_found = 0
        total_replenishment_units = 0

        for prod in products:
            prod_id = prod['product_id']
            name = prod['name']
            opening = prod['opening_stock']
            incoming = prod['incoming']
            dispatched = prod['dispatched']
            reported_closing = prod['reported_closing']
            reorder_level = prod['reorder_level']
            max_capacity = prod['max_capacity']

            # 1. Calculate Expected Closing Stock
            expected_closing = opening + incoming - dispatched

            # 2. Detect Discrepancy
            discrepancy = reported_closing - expected_closing
            if discrepancy != 0:
                total_discrepancies_found += 1

            # Determine discrepancy status text
            if discrepancy > 0:
                disc_status = f"Surplus (+{discrepancy})"
            elif discrepancy < 0:
                disc_status = f"Shrinkage ({discrepancy}) ⚠️"
            else:
                disc_status = "Balanced ✅"

            # 3. Calculate Replenishment Requirements
            replenishment_qty = 0
            if reported_closing <= reorder_level:
                replenishment_qty = max(0, max_capacity - reported_closing)
                total_replenishment_units += replenishment_qty

            reconciliation_records.append({
                "product_id": prod_id,
                "name": name,
                "expected": expected_closing,
                "reported": reported_closing,
                "discrepancy": discrepancy,
                "disc_status": disc_status,
                "needs_reorder": reported_closing <= reorder_level,
                "replenishment_qty": replenishment_qty
            })

        # 4. Generate Formatted Reconciliation Report
        report = f"""
==================================================
        WAREHOUSE INVENTORY RECONCILIATION
==================================================
Warehouse Location : {warehouse_name}
Total Items Audited: {len(products)}
Discrepancies Flagged: {total_discrepancies_found}
--------------------------------------------------
ITEM AUDIT BREAKDOWN
--------------------------------------------------"""

        for r in reconciliation_records:
            report += f"""
- [{r['product_id']}] {r['name']}
  Expected Closing : {r['expected']} | Reported Audit: {r['reported']}
  Discrepancy      : {r['disc_status']}"""
            if r['needs_reorder']:
                report += f"\n  REPLENISHMENT    : Order {r['replenishment_qty']} units (Below reorder threshold) 🚨"
            else:
                report += f"\n  REPLENISHMENT    : Stock levels healthy"

        report += f"""
--------------------------------------------------
SUMMARY ACTIONS REQUIRED
--------------------------------------------------
Total Reorder Purchase Orders Triggered : {sum(1 for r in reconciliation_records if r['needs_reorder'])} Products
Total Units Needed for Replenishment    : {total_replenishment_units:,} units
==================================================
"""
        return report

# ==========================================
# Sample Execution
# ==========================================
if __name__ == "__main__":
    system = InventoryReconciliationSystem()
    
    # Sample Warehouse Inventory Input Data
    warehouse_stock = [
        {
            "product_id": "P-101",
            "name": "Wireless Mechanical Keyboard",
            "opening_stock": 150,
            "incoming": 200,
            "dispatched": 180,
            "reported_closing": 165,  # Expected: 150 + 200 - 180 = 170 (Discrepancy: -5 missing)
            "reorder_level": 50,
            "max_capacity": 300
        },
        {
            "product_id": "P-102",
            "name": "HD 27-inch Monitor",
            "opening_stock": 45,
            "incoming": 30,
            "dispatched": 60,
            "reported_closing": 15,   # Expected: 45 + 30 - 60 = 15 (Balanced)
            "reorder_level": 25,       # Below reorder level -> Triggers replenishment
            "max_capacity": 100
        },
        {
            "product_id": "P-103",
            "name": "USB-C Fast Charging Cable",
            "opening_stock": 500,
            "incoming": 1000,
            "dispatched": 1250,
            "reported_closing": 255,  # Expected: 500 + 1000 - 1250 = 250 (Discrepancy: +5 surplus)
            "reorder_level": 100,
            "max_capacity": 800
        },
        {
            "product_id": "P-104",
            "name": "Ergonomic Office Chair",
            "opening_stock": 30,
            "incoming": 10,
            "dispatched": 35,
            "reported_closing": 5,    # Expected: 30 + 10 - 35 = 5 (Balanced)
            "reorder_level": 15,       # Triggers replenishment
            "max_capacity": 50
        }
    ]
    
    print(system.reconcile_inventory("Central Distribution Hub - North", warehouse_stock))
