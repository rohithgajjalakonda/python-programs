class PayrollSystem:
    def __init__(self, pf_rate=0.12, prof_tax=200, insurance=1500, ot_multiplier=1.5):
        self.pf_rate = pf_rate
        self.prof_tax = prof_tax
        self.insurance = insurance
        self.ot_multiplier = ot_multiplier

    def calculate_progressive_tax(self, taxable_income):
        """
        Progressive Tax Slabs:
        - Slab 1: Up to ₹30,000 -> 0%
        - Slab 2: ₹30,001 to ₹60,000 -> 10% on amount over ₹30,000
        - Slab 3: Above ₹60,000 -> 20% on amount over ₹60,000 (plus Slab 2 tax)
        """
        tax = 0.0
        if taxable_income > 60000:
            tax += (taxable_income - 60000) * 0.20
            taxable_income = 60000
        if taxable_income > 30000:
            tax += (taxable_income - 30000) * 0.10
        return tax

    def generate_pay_statement(self, employee):
      
        basic = employee['basic_pay']
        allowances = employee['allowances']
        incentives = employee['incentives']
        
        ot_hours = employee['overtime_hours']
        hourly_rate = employee['hourly_rate']
        overtime_pay = ot_hours * hourly_rate * self.ot_multiplier
        
        gross_salary = basic + allowances + overtime_pay + incentives
        
       
        pf = basic * self.pf_rate
        taxable_base = gross_salary - pf  # Standard tax base deduction context
        income_tax = self.calculate_progressive_tax(taxable_base)
        
        total_deductions = pf + self.prof_tax + self.insurance + income_tax
        
        
        net_salary = gross_salary - total_deductions
        
        
        statement = f"""
==================================================
              SALARY STATEMENT
==================================================
Employee ID   : {employee['emp_id']}
Employee Name : {employee['name']}
Designation   : {employee['designation']}
--------------------------------------------------
EARNINGS                                AMOUNT (₹)
--------------------------------------------------
Basic Pay                          : ₹{basic:,.2f}
Allowances (HRA/DA)                : ₹{allowances:,.2f}
Overtime ({ot_hours} hrs @ ₹{hourly_rate}/hr)  : ₹{overtime_pay:,.2f}
Performance Incentives             : ₹{incentives:,.2f}
--------------------------------------------------
GROSS SALARY                       : ₹{gross_salary:,.2f}
==================================================
DEDUCTIONS                              AMOUNT (₹)
--------------------------------------------------
Provident Fund (PF)                : ₹{pf:,.2f}
Professional Tax                   : ₹{self.prof_tax:,.2f}
Health Insurance                   : ₹{self.insurance:,.2f}
Progressive Income Tax             : ₹{income_tax:,.2f}
--------------------------------------------------
TOTAL DEDUCTIONS                   : ₹{total_deductions:,.2f}
==================================================
NET TAKE-HOME SALARY               : ₹{net_salary:,.2f}
==================================================
"""
        return statement


if __name__ == "__main__":
    payroll_system = PayrollSystem()
    
    sample_employee = {
        "emp_id": "EMP-4021",
        "name": "Sarah Jenkins",
        "designation": "Senior Software Engineer",
        "basic_pay": 55000.0,
        "allowances": 18000.0,
        "overtime_hours": 12,
        "hourly_rate": 350.0,
        "incentives": 7500.0
    }
    
    print(payroll_system.generate_pay_statement(sample_employee))

