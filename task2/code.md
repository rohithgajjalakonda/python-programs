Here is a complete system design, algorithm, Mermaid flowchart, Python implementation, and sample test case for the **Employee Payroll and Deduction Analysis System**.

---

## 1. Problem Statement

Organizations need a reliable payroll management system to calculate monthly or periodic employee compensation accurately. The system must process multiple earnings components (basic pay, allowances, overtime, and performance incentives), apply statutory and progressive deductions (such as tiered income tax brackets, provident fund, and insurance), and generate a clean, itemized salary statement.

### **Components & Rules:**

1. **Earnings:**
* **Gross Salary:** Sum of Basic Pay, Allowances, Overtime Pay, and Incentives.
* **Overtime Pay:** Overtime Hours $\times$ Hourly Rate $\times$ Overtime Multiplier.


2. **Deductions:**
* **Provident Fund (PF):** A fixed percentage of the Basic Pay.
* **Professional Tax / Insurance:** Fixed standard deductions.
* **Progressive Income Tax:** Tiered tax calculation based on taxable income thresholds (e.g., higher income slabs are taxed at higher marginal rates).


3. **Net Salary:** Gross Salary minus Total Deductions.

---

## 2. Algorithm

1. **Initialize Inputs:** Retrieve employee details, basic pay, allowances, overtime hours, hourly rate, incentives, and deduction parameters.
2. **Calculate Gross Earnings:**
* Compute `Overtime Pay = Overtime Hours * Hourly Rate * Multiplier`.
* Compute `Gross Salary = Basic Pay + Allowances + Overtime Pay + Incentives`.


3. **Calculate Standard Deductions:**
* Compute `Provident Fund (PF) = Basic Pay * PF Rate`.
* Add fixed deductions like Professional Tax and Health Insurance.


4. **Calculate Progressive Income Tax:**
* Determine taxable base.
* Iterate through tax brackets (e.g., 0% up to limit A, 10% between limit A and B, 20% above limit B) and accumulate tax across slabs.


5. **Calculate Net Salary:**
* `Total Deductions = PF + Professional Tax + Insurance + Income Tax`
* `Net Salary = Gross Salary - Total Deductions`


6. **Format Statement:** Generate and print an itemized salary breakdown sheet.

---

## 3. Flowchart (Mermaid)

```mermaid
graph TD
    Start([Start]) --> Input[Input Employee Data & Pay Components]
    Input --> CalcOT[Calculate Overtime Pay = Hours * Rate * Multiplier]
    CalcOT --> CalcGross[Calculate Gross Salary = Basic + Allowances + OT + Incentives]
    CalcGross --> CalcPF[Calculate Provident Fund = Basic * PF Rate]
    CalcPF --> CalcTax[Calculate Progressive Income Tax across Slabs]
    CalcTax --> CalcTotalDed[Sum All Deductions: PF + Tax + Insurance + Prof. Tax]
    CalcTotalDed --> CalcNet[Calculate Net Salary = Gross Salary - Total Deductions]
    CalcNet --> Output[Generate Formatted Salary Statement]
    Output --> End([End])

```

---

## 4. Python Source Code

```python
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
        # 1. Earnings Calculation
        basic = employee['basic_pay']
        allowances = employee['allowances']
        incentives = employee['incentives']
        
        ot_hours = employee['overtime_hours']
        hourly_rate = employee['hourly_rate']
        overtime_pay = ot_hours * hourly_rate * self.ot_multiplier
        
        gross_salary = basic + allowances + overtime_pay + incentives
        
        # 2. Deductions Calculation
        pf = basic * self.pf_rate
        taxable_base = gross_salary - pf  # Standard tax base deduction context
        income_tax = self.calculate_progressive_tax(taxable_base)
        
        total_deductions = pf + self.prof_tax + self.insurance + income_tax
        
        # 3. Net Salary Calculation
        net_salary = gross_salary - total_deductions
        
        # 4. Formatted Output Statement
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

# ==========================================
# Sample Execution
# ==========================================
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

```

---

## 5. Sample Input & Output

### **Sample Input Data**

* **Employee ID:** `EMP-4021`
* **Name:** Sarah Jenkins
* **Basic Pay:** ₹55,000.00
* **Allowances:** ₹18,000.00
* **Overtime Hours:** 12 hours (at ₹350/hr with 1.5x multiplier)
* **Incentives:** ₹7,500.00
* **Standard Deductions Config:**
* PF Rate: $12\%$ of Basic Pay
* Professional Tax: ₹200.00
* Health Insurance: ₹1,500.00



---

### **Sample Output Statement**

```text
==================================================
              SALARY STATEMENT
==================================================
Employee ID   : EMP-4021
Employee Name : Sarah Jenkins
Designation   : Senior Software Engineer
--------------------------------------------------
EARNINGS                                AMOUNT (₹)
--------------------------------------------------
Basic Pay                          : ₹55,000.00
Allowances (HRA/DA)                : ₹18,000.00
Overtime (12 hrs @ ₹350/hr)        : ₹6,300.00
Performance Incentives             : ₹7,500.00
--------------------------------------------------
GROSS SALARY                       : ₹86,800.00
==================================================
DEDUCTIONS                              AMOUNT (₹)
--------------------------------------------------
Provident Fund (PF)                : ₹6,600.00
Professional Tax                   : ₹200.00
Health Insurance                   : ₹1,500.00
Progressive Income Tax             : ₹7,040.00
--------------------------------------------------
TOTAL DEDUCTIONS                   : ₹15,340.00
==================================================
NET TAKE-HOME SALARY               : ₹71,460.00
==================================================

```
