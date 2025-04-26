# light-bulb-analyser-and-plascer


**An experimental tool for calculating optimal lamp positioning based on room dimensions and lighting requirements**

---

## 🔍 Project Purpose

This experimental calculator determines:
- How many lamps are needed for a space
- Where to position them optimally
- Whether current lamps provide sufficient illumination

*No financial calculations - pure lighting physics only*

---

## 📐 Input Parameters

The tool requires:
1. **Room Dimensions**
   - Length (meters)
   - Width (meters)
   - Height (meters)

2. **Lighting Requirements**
   - Desired lux level at floor level
   - Type of activity (presets available)

3. **Lamp Specifications** (per unit)
   - Luminous flux (lumens)
   - Beam angle (degrees)
   - Mounting height

---

## 📊 Calculation Method

Using photometric formulas, the tool calculates:

Number of lamps = (Room area × Target lux) / (Lamp lumens × CU × LLF)

Where:
- CU = Coefficient of Utilization
- LLF = Light Loss Factor

The experimental algorithm then suggests:
- Minimum number of lamps required
- Recommended spacing pattern
- Expected lux distribution map

---
