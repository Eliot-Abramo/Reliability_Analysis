"""
Task 1: Monte Carlo Simulation for Reliability Analysis
=========================================================

RANDOM PARAMETERS SPECIFICATIONS:
----------------------------------
Refer to the comments in the original code for the probability distributions
of each parameter. Key parameters with uncertainty:

1. LamB (Lambda_B values from IEC page 37):
   - Q5, Q6, D3, D12, D2:                                                       uniform(5.7, 6.9)
   - D10, D8:                                                                   uniform(1, 6.9)
   - Q10, Q14, Q17, Q19, Q20, Q22, Q12, Q13, Q16, Q23, Q26, Q32, Q34, Q36,      uniform(1, 6.9)
   - Q9, Q1, Q11, Q15, Q18, Q2, Q21, Q28, Q3, Q4, Q8, D4, D5, D6, D7:           uniform(1, 6.9)
   - Q24, Q25, Q27, Q33, Q35, Q37, Q7:                                          uniform(5.7, 6.9)

2. Lam3 (Lambda_3 values from IEC page 34):
   - U22:                                                                       50% probability 6.479, 50% probability 1.3
   - U17, U19:                                                                  uniform(0.315, 0.627)
   - U11, U21, U3, U7:                                                          uniform(0.202, 0.371)
   - U42:                                                                       uniform(0.084, 0.118)
   - U10, U2, U6:                                                               50% probability 4.1, 50% probability 1.3
   - U12, U4, U8:                                                               uniform(1.3, 4.1)
   - U35:                                                                       uniform(1.3, 2.94)
   - U23, U32, U14, U20, U25, U27, U29, U31, U36, U39, U40, U41:                50% probability 1.164, 50% probability 0.2808

3. VDS (Drain-Source Voltage):
   - Q5, Q6:                                                                    uniform(17, 23)
   - All other VDS:                                                             uniform(1.5, 2.5)

4. VCE (Collector-Emitter Voltage):
   - Q10, Q14, Q17, Q19, Q20, Q22:                                              uniform(10, 15)
   - Q12, Q13, Q16, Q23, Q26, Q32, Q34, Q36, Q9:                                uniform(3, 3.6)

5. Operating Power:
   - U42, U23, U32, U41, U33, U34, U43:                                         uniform(3, 5)
   - L1, L2, L3, L4, L5:                                                        uniform(5, 15)
   - All other components:                                                      uniform(0.5, 1.5)

YOUR TASKS:
-----------
@Louise STP add the math description of what they need to do here

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import reliability_math as rm

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INFO = '\033[10m'

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_monte_carlo_analysis(excel_file: str, sheet_name: str):
    """
    Complete Monte Carlo analysis workflow.
    This is called in the main.py
    """

    # Load Excel file
    print_info(f"Loading data from {excel_file}...")
    df = pd.read_excel(excel_file)

    if 'Sheet' not in df.columns:
        raise ValueError("Excel file must have a 'Sheet' column")

    # TODO: Implement the complete analysis workflow
    
    # c.f. run_block_reliability() in main.py if you want inspiration for the
    # automation

    print("\nAnalysis complete")


# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

if __name__ == "__main__":
    """
    Test your implementation here.
    
    This means you can do a python task1_monte_carlo.py in your terminal to directly test
    your code in case the main.py implementation is not adapted. 
    """
    print("I love reliability")
