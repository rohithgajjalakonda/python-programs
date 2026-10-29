class CanteenSystem:
    def __init__(self, menu_prices, initial_stock):
        self.menu_prices = menu_prices
        self.inventory = initial_stock
        self.total_revenue = 0.0
        self.items_sold_summary = {item: 0 for item in initial_stock}

    def process_orders(self, customer_orders):
        daily_reports = []

        for order_idx, order in enumerate(customer_orders, 1):
            customer_name = order["customer_name"]
            cart = order["items"]
            
            bill_items = []
            order_total = 0.0
            rejections = []

            for item_name, qty in cart.items():
                if item_name not in self.menu_prices:
                    rejections.append(f"{item_name}: Item not on menu")
                    continue
                
                available = self.inventory.get(item_name, 0)
                if qty <= available:
                    self.inventory[item_name] -= qty
                    self.items_sold_summary[item_name] += qty
                    item_cost = self.menu_prices[item_name] * qty
                    order_total += item_cost
                    bill_items.append({"name": item_name, "qty": qty, "cost": item_cost})
                else:
                    rejections.append(f"{item_name}: Requested {qty}, only {available} available")

            self.total_revenue += order_total
            
            daily_reports.append({
                "order_id": f"ORD-{100 + order_idx}",
                "customer": customer_name,
                "bill_items": bill_items,
                "order_total": order_total,
                "rejections": rejections
            })

        return daily_reports

    def generate_daily_summary(self, daily_reports):
        summary = f"""
==================================================
        SMART CANTEEN DAILY OPERATIONS REPORT
==================================================
TOTAL DAILY REVENUE : ₹{self.total_revenue:,.2f}
--------------------------------------------------
ORDER FULFILLMENT LOG
--------------------------------------------------"""

        for rep in daily_reports:
            summary += f"\n- Order ID: {rep['order_id']} | Customer: {rep['customer']}"
            if rep['bill_items']:
                for bi in rep['bill_items']:
                    summary += f"\n  * {bi['name']} x {bi['qty']} = ₹{bi['cost']:,.2f}"
                summary += f"\n  Order Total: ₹{rep['order_total']:,.2f}"
            else:
                summary += f"\n  Order fully unfulfilled."
            if rep['rejections']:
                summary += f"\n  Rejections: {'; '.join(rep['rejections'])}"

        summary += f"""
--------------------------------------------------
REMAINING INVENTORY STOCK
--------------------------------------------------"""

        for item, qty in self.inventory.items():
            sold = self.items_sold_summary[item]
            summary += f"\n- {item:<15} : {qty} units remaining (Sold: {sold})"

        summary += "\n=================================================="
        return summary

if __name__ == "__main__":
    menu_prices = {
        "Veg Burger": 120.0,
        "Cheese Pizza": 250.0,
        "Cold Coffee": 90.0,
        "French Fries": 80.0,
        "Club Sandwich": 150.0
    }

    initial_stock = {
        "Veg Burger": 15,
        "Cheese Pizza": 5,
        "Cold Coffee": 20,
        "French Fries": 10,
        "Club Sandwich": 8
    }

    canteen = CanteenSystem(menu_prices, initial_stock)

    customer_orders = [
        {
            "customer_name": "Aarav Sharma",
            "items": {"Veg Burger": 2, "Cold Coffee": 2, "French Fries": 3}
        },
        {
            "customer_name": "Priya Nair",
            "items": {"Cheese Pizza": 4, "Club Sandwich": 2}
        },
        {
            "customer_name": "Rohan Gupta",
            "items": {"Cheese Pizza": 3, "Veg Burger": 15}
        }
    ]

    reports = canteen.process_orders(customer_orders)
    print(canteen.generate_daily_summary(reports))
