Here is a complete system design, algorithm, Mermaid flowchart, Python implementation, and sample test case for the **Traffic Violation Penalty Calculator**.

---

## 1. Problem Statement

Traffic management authorities require an automated penalty calculation system to process vehicle infractions efficiently. The system must evaluate violations based on the vehicle category (e.g., Two-Wheeler, Car, Heavy Commercial Vehicle), the specific offence type (e.g., Speeding, Red Light, No Helmet/Seatbelt, Driving Without License), whether it is a repeat offence, and predefined statutory fine schedules.

Additionally, the system must check for license disqualification or suspension conditions based on accumulated penalty points or severe statutory violations.

### **Rules & Mechanics:**

1. **Base Fine Rules:** Fines vary by vehicle category and offence severity.
2. **Repeat Offence Multiplier:** If the offender has committed the same offence previously within a specified window, a repeat multiplier (e.g., $1.5\times$ or $2\times$) is applied to the base fine.
3. **Penalty Points:** Each violation accrues penalty points (e.g., Speeding = 3 points, Reckless Driving = 6 points).
4. **Disqualification Conditions:** A driver's license is flagged for suspension/disqualification if:
* Total accumulated penalty points exceed a critical limit (e.g., $\ge 12$ points).
* The offence involves a critical zero-tolerance infraction (e.g., Hit-and-Run or extreme speeding).



---

## 2. Algorithm

1. **Initialize Inputs:** Load vehicle category, offence records (offence type, repeat status), fine schedule matrices, and penalty point limits.
2. **Process Each Violation:**
* Look up the base fine for the specific vehicle category and offence type.
* Check if the violation is a repeat offence. If true, apply the repeat multiplier.
* Accumulate penalty points associated with the offence.


3. **Check Disqualification Criteria:**
* Evaluate total accumulated penalty points against the maximum threshold.
* Check for statutory critical infractions requiring immediate license suspension.


4. **Generate Penalty Invoice & Notice:** Format and output the itemized violation penalty statement.

---

## 3. Flowchart (Mermaid)

```mermaid
graph TD
    Start([Start]) --> Input[Input Offence Details: Vehicle Category, Offence Type & Repeat Status]
    Input --> LoopStart{More Violations?}
    
    LoopStart -- Yes --> Lookup[Lookup Base Fine & Penalty Points for Offence & Vehicle]
    Lookup --> CheckRepeat{Is Repeat Offence?}
    
    CheckRepeat -- Yes --> ApplyMultiplier[Apply Repeat Offence Multiplier to Fine] --> Accumulate
    CheckRepeat -- No --> UseBase[Use Standard Base Fine] --> Accumulate
    
    Accumulate[Add to Total Fine & Total Penalty Points] --> LoopStart
    
    LoopStart -- No --> CheckDisqual{Total Points >= Threshold OR Critical Infraction?}
    CheckDisqual -- Yes --> FlagSuspend[Flag License for Suspension / Disqualification 🚨] --> Output
    CheckDisqual -- No --> ClearSuspend[License Status: Active / Clear ✅] --> Output
    
    Output[Generate Itemized Traffic Violation Penalty Notice] --> End([End])

```

---
-

## 5. Sample Input & Output

### **Sample Input Configuration**

* **Offender Name:** Vikram Malhotra
* **Vehicle Category:** `Car`
* **Violations Recorded:**
1. *Speeding* (First-time offence)
2. *No Seatbelt* (Repeat offence)
3. *Red Light Jump* (Repeat offence)
4. *Drunk Driving* (First-time offence)


* **Threshold Rules:** Max penalty points limit = `12`, Repeat offence surcharge = `1.5x`

---

### **Sample Output Penalty Notice**

```text
==================================================
        TRAFFIC VIOLATION PENALTY NOTICE
==================================================
Offender Name      : Vikram Malhotra
Vehicle Category   : Car
--------------------------------------------------
ITEMIZED OFFENCE RECORDS
--------------------------------------------------
1. Speeding
   Base Fine: ₹2,000.00 | Final Fine: ₹2,000.00 | Points: +3
2. No Seatbelt [REPEAT OFFENCE ⚠️]
   Base Fine: ₹1,000.00 | Final Fine: ₹1,500.00 | Points: +2
3. Red Light Jump [REPEAT OFFENCE ⚠️]
   Base Fine: ₹1,500.00 | Final Fine: ₹2,250.00 | Points: +3
4. Drunk Driving
   Base Fine: ₹15,000.00 | Final Fine: ₹15,000.00 | Points: +10
--------------------------------------------------
SUMMARY OF PENALTIES
--------------------------------------------------
Total Penalty Points Accrued : 18 / 12 threshold
Total Statutory Fine Payable : ₹20,750.00
==================================================
LICENSE STATUS & ADJUDICATION
==================================================
STATUS: ❌ LICENSE SUSPENDED / DISQUALIFIED
Reason: Accumulated penalty points exceeded maximum limit.
==================================================

```
