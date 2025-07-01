
# Analysis Techniques
- **Definition**: Mathematical and physical meaning 
- **Purpose**: What specific degradation mechanisms it reveals 
- **Implementation**: How to calculate from raw data 
- **Interpretation**: How to identify key features and patterns 
- **Limitations**: When the technique might not apply 
- **References**: Academic sources supporting the methodology

## Differential Capacity Analysis (dQ/dV)

### Definition
Shows how battery capacity changes with voltage.  
Mathematically:  
**dQ/dV** = change in capacity per change in voltage

### Purpose
- Reveals phase transitions and reaction plateaus
- Highlights active material usage and degradation

### Implementation
1. Extract charge/discharge curves (Q vs. V)
2. Use numerical differentiation:  
   `dQ/dV = (Q[i+1] - Q[i]) / (V[i+1] - V[i])`
3. Smooth using filters (e.g., Savitzky-Golay)

### Interpretation
- Peaks = phase changes  
- Broadening = increased resistance or aging  
- Shifted peaks = degradation

### Limitations
- Sensitive to noise  
- Hard to interpret in blended chemistries

### References
- [Smith et al., 2012](https://www.sciencedirect.com/...)  
- [PyProBE Docs](https://github.com/clechasseur/pyprobe)

---

## Differential Voltage Analysis (dV/dQ)

### Definition
Shows how battery voltage changes with capacity.  
Mathematically:  
**dV/dQ** = change in voltage per change in capacity

### Purpose
- Provides insight into **internal resistance growth**
- Useful for identifying **phase transformations**
- Helps distinguish between **kinetic vs. thermodynamic degradation**

### Implementation
1. Extract voltage vs. capacity data (V vs. Q)
2. Compute:  
   `dV/dQ = (V[i+1] - V[i]) / (Q[i+1] - Q[i])`
3. Apply smoothing filters if needed

### Interpretation
- Sharp features = distinct electrochemical processes
- Slope increase = higher resistance or aging
- Shift in minima/maxima = loss of active material

### Limitations
- Noisy if data sampling is low resolution
- Interpretation is chemistry-dependent

### References
- [Birkl et al., 2017](https://www.sciencedirect.com/science/article/abs/pii/S0378775316308587)  
- [PyProBE Docs](https://github.com/clechasseur/pyprobe)

---

## Differential Coulometry Spectroscopy (DCS)

### Definition
Uses differences in Coulombic capacity curves between cycles to detect subtle battery degradation effects.

### Purpose
- Sensitive to **minor degradation changes** not seen in single-cycle analysis
- Tracks **loss of lithium inventory**, SEI growth, and side reactions

### Implementation
1. Plot differential capacity over time:  
   `ΔQ = Q_n - Q_reference`  
   (usually comparing each cycle to a baseline)
2. Repeat over many cycles
3. Use smoothing or overlay techniques to enhance visibility

### Interpretation
- Progressive deviation = cumulative degradation
- Signature changes = onset of specific failure modes (e.g., SEI thickening)

### Limitations
- Needs consistent cycling protocol
- Sensitive to measurement drift or inconsistencies
- Requires long-term data for best results

### References
- [Attia et al., 2022](https://www.nature.com/articles/s41586-022-04566-2)  
- [PyProBE Docs](https://github.com/clechasseur/pyprobe)

---

## Power-Energy Analysis (dP/dE)

### Definition
Analyzes the relationship between **power** (rate of energy transfer) and **energy** stored/released.  
**dP/dE** = change in power with respect to energy

### Purpose
- Highlights **rate capability** and **power fade**
- Reveals how efficiently the battery converts energy over time

### Implementation
1. Extract power and energy values from cycling data:  
   - Power = `P = V × I`  
   - Energy = integral of power over time
2. Compute dP/dE:  
   `dP/dE = (P[i+1] - P[i]) / (E[i+1] - E[i])`

### Interpretation
- Slope changes = degradation in energy delivery  
- Peak shifts = reduced instantaneous power  
- Overall shape = degradation pattern over charge/discharge

### Limitations
- Requires accurate time-series data  
- Sensitive to current and voltage noise  
- Less commonly used → harder to interpret without context

### References
- [Severson et al., 2019](https://www.nature.com/articles/s41586-019-1682-5)  
- [PyBaMM Docs](https://www.pybamm.org/)
