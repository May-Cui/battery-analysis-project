# Battery Terminology Glossary

---

## Charging and discharging
### Capacity 
Total electric charge a battery can store. Measured in mAh or Ah.
### Coulombic Efficiency (CE)  
Ratio of discharge capacity to charge capacity. Ideal is 100%.
### Cycle Life  
Number of full charge/discharge cycles before capacity drops to ~80%.
### C-rate  
Rate of charge/discharge. 1C means full charge or discharge in 1 hour.
### Cycling Curve
A **cycling curve** is the voltage–capacity (V–Q) plot of a battery during charging and discharging.  
- One charge/discharge cycle = one curve loop
- Basis for methods like dQ/dV, dV/dQ, DCS
- Used to assess capacity, hysteresis, and aging behavior

## 🔢 Battery Metadata Field Definitions: `Step Type`, `Step Number`, `Step Time`, `Step Position`

This section explains key metadata columns used to describe experimental protocol structure in raw battery cycling data.

---

### 📘 Step Type

**Definition**:  
An **encoded numeric ID** indicating the **type of operation** being performed at each moment in time.

**Typical meanings (numeric codes may vary by dataset)**:
- `1` → Constant Current Charge (CC_Chg)
- `2` → Constant Voltage Hold (CV_Hold)
- `3` → Constant Current Discharge (CC_DChg)
- `4` → Rest (0 current)
- `10+` → Special or protocol-specific actions

**Key Characteristics**:
- Encodes **what** the battery is doing (not where in sequence)
- Same `Step Type` may appear in multiple `Step Numbers` or cycles
- You can use `groupby('Step Type')` + check `Current` signs to decode meanings

**Use in analysis**:  
✅ Best for identifying physical operations like charge/discharge/rest  
✅ Use this column to extract clean charging or discharging segments

---

### 📗 Step Number

**Definition**:  
A sequential ID indicating **which step of the protocol** the battery is currently in — like a step index.

**Key Characteristics**:
- Starts from `1`, increases through each test sequence
- Repeats across cycles (e.g. Step Number `1` might always be charge)
- Tells you the **order** of steps in the protocol

**Use in analysis**:  
✅ Use this when you want to analyze specific steps in the protocol  
✅ Best for identifying position (e.g. "2nd step in every cycle")  
❌ Not always sufficient alone to identify action type (pair with Step Type)

---

### 📙 Step Time

**Definition**:  
The **time elapsed (in seconds)** since the current step began.

**Key Characteristics**:
- Resets to 0 at the start of every new step
- Increases as battery remains in the same step
- Can be used to calculate time durations of steps

**Use in analysis**:  
✅ Useful for plotting time-based trends within one step  
❌ Not used for dV/dQ or capacity-voltage analysis directly

---

### 📒 Step Position

**Definition**:  
The **row index counter within the current step** — like a per-step data point counter.

**Key Characteristics**:
- Starts from 0 in each new step
- Increases by 1 with each data sample (e.g., every second or timestamp)
- Often redundant if timestamp is present

**Use in analysis**:  
✅ Useful for per-step smoothing, filtering, or intra-step statistics  
❌ Not necessary for general voltage–capacity or dV/dQ extraction

---

### 🧠 Summary Table

| Field          | Meaning                                | Use for dV/dQ? | Notes                                    |
|----------------|----------------------------------------|----------------|-------------------------------------------|
| `Step Type`    | Encoded action type (charge/discharge) | ✅ Yes         | Use to extract CC_Chg or CC_DChg          |
| `Step Number`  | Position in protocol (repeats by cycle)| ✅ Sometimes   | Use with Step Type for specific filtering |
| `Step Time`    | Time elapsed in current step (s)       | ❌ No          | For duration or time plots only           |
| `Step Position`| Row index within step (counter)        | ❌ No          | Rarely used unless doing advanced metrics |


---

## State estimation
SOC and SOH are two important parameters in battery diagnostic and battery lifetime expectation.  
They are not directly measurable.  
A poor SOH indicates degradation.
### Battery state of charge (SOC)
Indicates remaining charge, expressed as a percentage (0–100%).  
100% SOC = battery is fully charged
### Battery state of health (SOH)
Indicates the ageing level  
can be defined as a comparison between the battery capability at the beginning of its life and the current operation condition of the battery.  
i.e. SOH = (current capacity/ nominal capacity) × 100%

---

## Degradation
### Calendar Aging  
Degradation over time during storage, even without use.

---

## Half-cell and full-cells
### Half-cell
Consists of one electrode (either positive or negative) from the battery being tested against a reference/counter electrode, typically lithium metal.  
**Usage**:   
Study **degradation mechanisms** like SEI formation and capacity fade, as
- degradation signals are unmixed.
- features are clearer (curves not convoluted) - easier interpretation  

Also allows evaluation of new materials' raw performance and degradation pattern before introducing interactions with another electrode.

**Limitations**:
- Idealized setup, **not representative of real-world operation**
- Cannot assess full battery performance
### Full-cell
Includes both the cathode and anode as in a real battery, providing a complete system view.  
**Usage**: 
- Assess **overall battery performance** under realistic conditions
- Analyze **interactions between both electrodes**, validate how they work together
### Comparison
| Property            | Half-Cell                               | Full-Cell                                |
|---------------------|------------------------------------------|-------------------------------------------|
| **Target**           | Single electrode                         | Full system                                |
| **Precision**        | High (sensitive to individual behavior)  | Lower (electrode interaction complicates)  |
| **Use Case**         | Materials research                       | Commercial validation                      |
| **Interpretation**   | Easier (fewer variables)                 | Harder (signals are mixed)                 |
| **Realism**          | Poor                                     | Strong                                     |

### Alignment
**Alignment** refers to **adjusting and aligning the voltage vs capacity (or SOC) curves of individual electrodes** (from half-cell measurements) so that they can be meaningfully compared or **reconstructed into a full-cell view**.  
We want to reconstruct the **full-cell voltage profile**:

V_{full-cell} = V_{+} - V_{-}

> Without alignment, simply subtracting \( V_{+} \) and \( V_{-} \) curves will result in incorrect full-cell profiles due to mismatched SOC windows and lithium imbalance.

---

### Why Shifts Occur

There will be **shifts between the electrode curves** due to:

1. **SOC mismatch at cell assembly**  
   → Electrodes start at different states of charge for safety or design reasons.

2. **LLI (Loss of Lithium Inventory)**  
   → Irreversible lithium consumption (e.g., SEI formation) shifts usable capacity windows.

3. **Electrode imbalance (N/P ratio ≠ 1)**  
   → One electrode has intentionally more capacity (often the anode) to prevent lithium plating.

---

### What Alignment Involves

To accurately reconstruct the full-cell voltage, we apply:

- **Shifts**  
  Horizontal translation of one electrode’s capacity axis, typically to:
  - Align SOC windows
  - Model LLI effects

- **Scaling**  
  Resizing the capacity window to reflect electrode balancing (e.g., N/P ratio correction)

> Alignment is especially important when analyzing full-cell **dV/dQ** curves. Small voltage shifts reveal degradation mechanisms — without alignment, these features can be misinterpreted or obscured.

---

## Hazards
###  Thermal Runaway  
Dangerous overheating loop that can lead to fire or explosion.
### Lithium plating
