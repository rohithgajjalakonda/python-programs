class TrafficPenaltyCalculator:
    def __init__(self, max_penalty_points=12):
        self.max_penalty_points = max_penalty_points
        
       
        self.fine_schedule = {
            "Two-Wheeler": {
                "Speeding": {"base_fine": 1500, "points": 3},
                "Red Light Jump": {"base_fine": 1000, "points": 3},
                "No Helmet": {"base_fine": 1000, "points": 2},
                "Driving Without License": {"base_fine": 5000, "points": 6},
                "Drunk Driving": {"base_fine": 10000, "points": 10}
            },
            "Car": {
                "Speeding": {"base_fine": 2000, "points": 3},
                "Red Light Jump": {"base_fine": 1500, "points": 3},
                "No Seatbelt": {"base_fine": 1000, "points": 2},
                "Driving Without License": {"base_fine": 5000, "points": 6},
                "Drunk Driving": {"base_fine": 15000, "points": 10}
            },
            "Commercial Vehicle": {
                "Speeding": {"base_fine": 4000, "points": 4},
                "Red Light Jump": {"base_fine": 3000, "points": 4},
                "Overloading": {"base_fine": 10000, "points": 6},
                "Driving Without License": {"base_fine": 10000, "points": 8},
                "Drunk Driving": {"base_fine": 25000, "points": 12}
            }
        }
        
        self.repeat_multiplier = 1.5 

    def process_violations(self, offender_name, vehicle_category, violations):
        total_fine = 0.0
        total_points = 0
        itemized_violations = []
        is_critical_infraction = False

        category_schedule = self.fine_schedule.get(vehicle_category, self.fine_schedule["Car"])

        for v in violations:
            offence = v['offence_type']
            is_repeat = v['is_repeat']

           
            
            offence_data = category_schedule.get(offence, {"base_fine": 2000, "points": 3})
            
            base_fine = offence_data['base_fine']
            points = offence_data['points']

            
            
            effective_fine = base_fine * self.repeat_multiplier if is_repeat else base_fine
            
            if offence == "Drunk Driving" or points >= 10:
                is_critical_infraction = True

            total_fine += effective_fine
            total_points += points

            itemized_violations.append({
                "offence": offence,
                "is_repeat": is_repeat,
                "base_fine": base_fine,
                "effective_fine": effective_fine,
                "points": points
            })

      
        
        is_disqualified = total_points >= self.max_penalty_points or is_critical_infraction

       
        notice = f"""
==================================================
        TRAFFIC VIOLATION PENALTY NOTICE
==================================================
Offender Name      : {offender_name}
Vehicle Category   : {vehicle_category}
--------------------------------------------------
ITEMIZED OFFENCE RECORDS
--------------------------------------------------"""

        for idx, item in enumerate(itemized_violations, 1):
            status_tag = " [REPEAT OFFENCE ⚠️]" if item['is_repeat'] else ""
            notice += f"\n{idx}. {item['offence']}{status_tag}\n   Base Fine: ₹{item['base_fine']:,.2f} | Final Fine: ₹{item['effective_fine']:,.2f} | Points: +{item['points']}"

        notice += f"""
--------------------------------------------------
SUMMARY OF PENALTIES
--------------------------------------------------
Total Penalty Points Accrued : {total_points} / {self.max_penalty_points} threshold
Total Statutory Fine Payable : ₹{total_fine:,.2f}
==================================================
LICENSE STATUS & ADJUDICATION
=================================================="""

        if is_disqualified:
            notice += f"\nSTATUS: ❌ LICENSE SUSPENDED / DISQUALIFIED\nReason: {'Accumulated penalty points exceeded maximum limit' if total_points >= self.max_penalty_points else 'Critical zero-tolerance traffic violation detected'}."
        else:
            notice += f"\nSTATUS: ✅ LICENSE ACTIVE (Warning issued - Drive safely)"

        notice += "\n=================================================="
        return notice


if __name__ == "__main__":
    calculator = TrafficPenaltyCalculator(max_penalty_points=12)

   
    offender_name = "Vikram Malhotra"
    vehicle_category = "Car"
    
    violations_recorded = [
        {"offence_type": "Speeding", "is_repeat": False},          
        {"offence_type": "No Seatbelt", "is_repeat": True},      
        {"offence_type": "Red Light Jump", "is_repeat": True},    
        {"offence_type": "Drunk Driving", "is_repeat": False}     
    ]

    print(calculator.process_violations(offender_name, vehicle_category, violations_recorded))
