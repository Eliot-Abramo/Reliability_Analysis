"""
Task 2: Sensitivity Analysis for Reliability
==============================================

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

def run_sensitivity_analysis(excel_file: str,
                            sheet_name: str,
                            variation_percent: float = 10):
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