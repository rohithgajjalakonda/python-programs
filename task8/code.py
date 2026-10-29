class FraudDetectionSystem:
    def __init__(self, high_value_threshold=100000.0):
        self.high_value_threshold = high_value_threshold

    def detect_suspicious_transactions(self, transactions):
        seen_txn_ids = set()
        seen_signatures = set()
        suspicious_entries = []
        clean_count = 0

        for txn in transactions:
            txn_id = txn["txn_id"]
            user_id = txn["user_id"]
            amount = txn["amount"]
            merchant = txn["merchant"]
            timestamp = txn["timestamp"]

            flags = []

            if txn_id in seen_txn_ids:
                flags.append("Duplicate Transaction ID")
            else:
                seen_txn_ids.add(txn_id)

            signature = (user_id, amount, merchant)
            if signature in seen_signatures:
                flags.append("Repeated Identical Payment")
            else:
                seen_signatures.add(signature)

            if amount > self.high_value_threshold:
                flags.append("High-Value Threshold Violation")

            if flags:
                suspicious_entries.append({
                    "txn_id": txn_id,
                    "user_id": user_id,
                    "amount": amount,
                    "merchant": merchant,
                    "timestamp": timestamp,
                    "flags": flags
                })
            else:
                clean_count += 1

        report = f"""
==================================================
        REPEATED TRANSACTION DETECTION
==================================================
Total Transactions Processed : {len(transactions)}
High-Value Threshold Limit   : ₹{self.high_value_threshold:,.2f}
Clean Transactions Verified  : {clean_count}
Suspicious Entries Flagged   : {len(suspicious_entries)}
--------------------------------------------------
SUSPICIOUS TRANSACTION AUDIT QUEUE
--------------------------------------------------"""

        for idx, item in enumerate(suspicious_entries, 1):
            report += f"""
{idx}. Txn ID: {item['txn_id']} | User: {item['user_id']} | Amount: ₹{item['amount']:,.2f}
   Merchant  : {item['merchant']} | Time: {item['timestamp']}
   Risk Flags: {'; '.join(item['flags'])}"""

        report += "\n=================================================="
        return report

if __name__ == "__main__":
    detector = FraudDetectionSystem(high_value_threshold=75000.0)
    
    transaction_stream = [
        {"txn_id": "TXN-9001", "user_id": "U-101", "amount": 4500.0, "merchant": "ElectroMart", "timestamp": "10:15:22"},
        {"txn_id": "TXN-9002", "user_id": "U-102", "amount": 82000.0, "merchant": "LuxuryCars", "timestamp": "10:18:05"},
        {"txn_id": "TXN-9003", "user_id": "U-103", "amount": 1200.0, "merchant": "QuickCoffee", "timestamp": "10:20:10"},
        {"txn_id": "TXN-9004", "user_id": "U-101", "amount": 4500.0, "merchant": "ElectroMart", "timestamp": "10:22:40"},
        {"txn_id": "TXN-9002", "user_id": "U-102", "amount": 82000.0, "merchant": "LuxuryCars", "timestamp": "10:25:11"},
        {"txn_id": "TXN-9005", "user_id": "U-104", "amount": 120000.0, "merchant": "GlobalJewels", "timestamp": "10:30:00"}
    ]
    
    print(detector.detect_suspicious_transactions(transaction_stream))
