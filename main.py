"""
Main Launcher for Reliability Analysis Student Project
=======================================================

This is the main interface for running reliability analysis tasks.
It provides a clean, automated workflow with robust error handling.
"""

import sys
import os
from pathlib import Path
from typing import Optional, Callable
import traceback

import task1_monte_carlo as mc
import task2_sensitivity_analysis as sa

# Color codes for terminal output (works on most terminals)
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

def print_header(text: str):
    """Print formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def safe_execute(func: Callable, error_msg: str = "An error occurred") -> bool:
    """
    Execute a function with error handling.
    
    Args:
        func: Function to execute
        error_msg: Custom error message
    
    Returns:
        True if successful, False otherwise
    """
    try:
        func()
        return True
    except FileNotFoundError as e:
        print_error(f"{error_msg}: File not found - {e.filename}")
        print_info("Please ensure all required files are in the correct location.")
        return False
    except ImportError as e:
        print_error(f"{error_msg}: Missing dependency - {e.name}")
        print_info("Please install required packages: pip install numpy pandas matplotlib openpyxl")
        return False
    except Exception as e:
        print_error(f"{error_msg}: {type(e).__name__}")
        print(f"{Colors.RED}{str(e)}{Colors.ENDC}")
        print("\nFull error traceback:")
        print(f"{Colors.YELLOW}{traceback.format_exc()}{Colors.ENDC}")
        return False

def check_environment() -> bool:
    """
    Check if the environment is properly set up.
    
    Returns:
        True if all checks pass, False otherwise
    """
    print_info("Checking environment setup...")
    
    all_ok = True
    
    # Check Python version
    if sys.version_info < (3, 7):
        print_error(f"Python 3.7+ required, found {sys.version}")
        all_ok = False
    else:
        print_success(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check for required modules
    required_modules = ['numpy', 'pandas', 'matplotlib', 'math', 'openpyxl']
    for module in required_modules:
        try:
            __import__(module)
            print_success(f"Module '{module}' found")
        except ImportError:
            print_error(f"Module '{module}' not found")
            all_ok = False
    
    # Check for required files
    required_files = ['reliability_math.py', 'task1_monte_carlo.py', 'task2_sensitivity_analysis.py']
    for file in required_files:
        if Path(file).exists():
            print_success(f"File '{file}' found")
        else:
            print_error(f"File '{file}' not found")
            all_ok = False
    
    return all_ok

def get_excel_file() -> Optional[Path]:
    """
    Prompt user for Excel file path with validation.
    
    Returns:
        Path object if valid, None otherwise
    """
    print_info("Please enter the path to your Excel data file:")
    print(f"{Colors.CYAN}(Press ENTER for default placement. Example: Reliability_Total.xlsx or ./data/Reliability_Total.xlsx){Colors.ENDC}")
    
    while True:
        file_path = input(f"{Colors.BOLD}File path: {Colors.ENDC}").strip()
        
        if not file_path:
            print_warning("No file path entered. Please try again.")
            continue
        
        # Remove quotes if present
        file_path = file_path.strip('"').strip("'")
        
        path = Path(file_path)
        
        if not path.exists():
            print_error(f"File not found: {file_path}")
            retry = input(f"{Colors.YELLOW}Try again? (y/n): {Colors.ENDC}").lower()
            if retry != 'y':
                return None
            continue
        
        if path.suffix not in ['.xlsx', '.xls']:
            print_warning("File doesn't appear to be an Excel file (.xlsx or .xls)")
            proceed = input(f"{Colors.YELLOW}Proceed anyway? (y/n): {Colors.ENDC}").lower()
            if proceed != 'y':
                continue
        
        print_success(f"Excel file validated: {path}")
        return path

def get_sheet_name(excel_file: Path) -> Optional[str]:
    """
    Get block name from user with hierarchical preview.
    
    This function reads the 'Sheet' column from the Excel file and displays
    the hierarchical block structure for selection.
    
    Args:
        excel_file: Path to Excel file
    
    Returns:
        Block name (Sheet column value) if valid, None otherwise
    """
    try:
        import pandas as pd
        
        print_info("Loading Excel file to list available blocks...")
        
        # Read the Excel file - assuming first sheet or 'Board3'
        try:
            df = pd.read_excel(excel_file, sheet_name='Board3')
        except:
            df = pd.read_excel(excel_file, sheet_name=0)
        
        if 'Sheet' not in df.columns:
            print_error("Excel file must have a 'Sheet' column containing block names")
            return None
        
        # Get unique blocks and sort them
        blocks = sorted(df['Sheet'].unique())
        
        # Organize blocks hierarchically for display
        print(f"\n{Colors.BOLD}Available blocks (hierarchical structure):{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}")
        
        # Group by top-level hierarchy
        hierarchy = {}
        for block in blocks:
            parts = [p for p in block.split('/') if p]
            if len(parts) >= 2:
                top_level = '/' + parts[0] + '/' + parts[1] + '/'
                if top_level not in hierarchy:
                    hierarchy[top_level] = []
                hierarchy[top_level].append(block)
        
        # Display organized by top-level
        block_list = []
        idx = 1
        
        for top_level in sorted(hierarchy.keys()):
            # Count total components in this top-level
            top_blocks = hierarchy[top_level]
            total_comps = sum(len(df[df['Sheet'] == b]) for b in top_blocks)
            
            print(f"\n{Colors.BOLD}{top_level}{Colors.ENDC} ({total_comps} total components)")
            
            for block in sorted(top_blocks):
                comp_count = len(df[df['Sheet'] == block])
                
                # Calculate indentation based on depth
                depth = block.count('/') - top_level.count('/')
                indent = "  " + "  " * depth
                
                # Different color for different depths
                if depth == 0:
                    color = Colors.GREEN
                elif depth == 1:
                    color = Colors.CYAN
                else:
                    color = Colors.BLUE
                
                print(f"{color}{idx:3d}. {indent}{block:<50} ({comp_count:3d} components){Colors.ENDC}")
                block_list.append(block)
                idx += 1
        
        print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print_info(f"\nTotal: {len(block_list)} blocks with {len(df)} components")
        print_info("\nEnter block number or exact block name:")
        print(f"{Colors.YELLOW}Tip: Start with a top-level block and use sub-block processing!{Colors.ENDC}")
        
        while True:
            choice = input(f"\n{Colors.BOLD}Block: {Colors.ENDC}").strip()
            
            if not choice:
                print_warning("No block selected.")
                return None
            
            # Check if user entered a number
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(block_list):
                    block_name = block_list[idx]
                    comp_count = len(df[df['Sheet'] == block_name])
                    print_success(f"Selected: {block_name} ({comp_count} components)")
                    return block_name
                else:
                    print_error(f"Invalid number. Please choose 1-{len(block_list)}")
                    continue
            
            # Check if user entered an exact name
            if choice in blocks:
                comp_count = len(df[df['Sheet'] == choice])
                print_success(f"Selected: {choice} ({comp_count} components)")
                return choice
            
            # Check for partial match (helpful for long paths)
            matches = [b for b in blocks if choice in b]
            if len(matches) == 1:
                comp_count = len(df[df['Sheet'] == matches[0]])
                print_info(f"Found match: {matches[0]}")
                confirm = input(f"{Colors.YELLOW}Use this block? (y/n): {Colors.ENDC}").lower()
                if confirm == 'y':
                    print_success(f"Selected: {matches[0]} ({comp_count} components)")
                    return matches[0]
            elif len(matches) > 1:
                print_warning(f"Multiple matches found for '{choice}':")
                for i, match in enumerate(matches[:5], 1):
                    comp_count = len(df[df['Sheet'] == match])
                    print(f"  {i}. {match} ({comp_count} components)")
                if len(matches) > 5:
                    print(f"  ... and {len(matches) - 5} more")
                print_info("Please be more specific or use the block number.")
                continue
            
            print_error(f"Block '{choice}' not found in Excel file.")
            retry = input(f"{Colors.YELLOW}Try again? (y/n): {Colors.ENDC}").lower()
            if retry != 'y':
                return None
    
    except Exception as e:
        print_error(f"Error reading Excel file: {e}")
        print(f"{Colors.YELLOW}{traceback.format_exc()}{Colors.ENDC}")
        return None

def display_menu() -> str:
    """
    Display main menu and get user choice.
    
    Returns:
        User's menu choice
    """
    print_header("RELIABILITY ANALYSIS - MAIN MENU")
    
    print(f"{Colors.BOLD}Please select an option:{Colors.ENDC}\n")
    print(f"{Colors.CYAN}  1. {Colors.ENDC}Calculate Block Reliability (Deterministic)")
    print(f"{Colors.CYAN}  2. {Colors.ENDC}Task 1: Monte Carlo Simulation")
    print(f"{Colors.CYAN}  3. {Colors.ENDC}Task 2: Sensitivity Analysis")
    print(f"{Colors.CYAN}  4. {Colors.ENDC}Test Environment Setup")
    print(f"{Colors.CYAN}  5. {Colors.ENDC}Help & Documentation")
    print(f"{Colors.CYAN}  0. {Colors.ENDC}Exit")
    
    choice = input(f"\n{Colors.BOLD}Your choice: {Colors.ENDC}").strip()
    return choice

def show_help():
    """Display help and documentation."""
    print_header("HELP & DOCUMENTATION")
    
    help_text = f"""
{Colors.BOLD}Project Overview:{Colors.ENDC}
This project performs reliability analysis on electronic components using
three complementary approaches:

{Colors.BOLD}Option 1 - Block Reliability Calculation (Deterministic):{Colors.ENDC}
  • Core functionality - calculates baseline reliability
  • Processes individual blocks or entire subsystems
  • Automatic sub-block detection (e.g., /Power/ → /Power/Boost/, /Power/Deploy/)
  • Provides detailed component breakdown
  • Output: Lambda and reliability for each block, combined system reliability

{Colors.BOLD}Option 2 - Task 1: Monte Carlo Simulation:{Colors.ENDC}
  • Accounts for uncertainty in component parameters
  • Runs of simulations with random parameter values
  • Provides statistical confidence in reliability estimates
  • Output: Distribution of reliability values, confidence intervals

{Colors.BOLD}Option 3 - Task 2: Sensitivity Analysis:{Colors.ENDC}
  • Identifies which parameters most affect reliability
  • Calculates sensitivity coefficients for each parameter
  • Helps prioritize design improvements and quality control

{Colors.BOLD}Required Files:{Colors.ENDC}
  • Excel file with component data (columns: Reference, Class, Sheet, etc.)
  • reliability_math.py (mathematical functions)
  • task1_monte_carlo.py (your Monte Carlo implementation)
  • task2_sensitivity_analysis.py (your sensitivity analysis implementation)

{Colors.BOLD}Data File Format:{Colors.ENDC}
Your Excel file should have these key columns:
  • Reference: Component identifier (e.g., 'Q5', 'U22')
  • Class: Component type (e.g., 'Integrated Circuit (7)')
  • Sheet: Block/subsystem name (e.g., '/Project Architecture/Power/')
  • Temperature_Junction, Temperature_Ambiant: Operating temperatures
  • Other parameters specific to each component type

{Colors.BOLD}Getting Started:{Colors.ENDC}
  1. Ensure all required files are in the same directory
  2. Install dependencies: pip install numpy pandas matplotlib openpyxl
  3. Run this main.py file
  4. Select option 5 to test your environment
  5. Choose Option 1 to calculate baseline reliability
  6. Proceed to Tasks 1 and 2 for advanced analysis

{Colors.BOLD}Tips:{Colors.ENDC}
  • Always start with Option 1 to verify your data loads correctly
  • Use sub-block processing to analyze entire subsystems at once
  • Test on a small block before analyzing the full system
  • Check the TODO comments in task files for implementation guidance
  • Save your results before running long analyses

{Colors.BOLD}For More Information:{Colors.ENDC}
  • Read the docstrings in each task file
  • Consult the IEC 62380 standard for reliability calculations
"""
    print(help_text)
    
    input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

def run_block_reliability():
    """Execute deterministic block reliability calculation."""
    print_header("BLOCK RELIABILITY CALCULATION")
    
    # Get Excel file
    excel_file = get_excel_file()
    if excel_file is None:
        print_warning("Operation cancelled.")
        return
    
    # Get sheet name
    sheet_name = get_sheet_name(excel_file)
    if sheet_name is None:
        print_warning("Operation cancelled.")
        return
    
    # Ask if user wants to process sub-blocks
    print_info("\nDo you want to process this block and all its sub-blocks?")
    print(f"{Colors.CYAN}Example: If you select '/Power/', it will also process:")
    print(f"  - /Power/Boost/")
    print(f"  - /Power/Deploy/")
    print(f"  - /Power/LDO_3v3_sat/")
    print(f"  - etc.{Colors.ENDC}")
    
    process_subblocks = input(f"{Colors.YELLOW}Process sub-blocks? (y/n): {Colors.ENDC}").lower() == 'y'
    
    # Execute calculation
    print_info("Starting reliability calculation...")
    
    def execute():
        import pandas as pd
        import reliability_math as rm
        
        # Load Excel file
        print_info(f"Loading data from {excel_file}...")
        df = pd.read_excel(excel_file)
        
        if 'Sheet' not in df.columns:
            raise ValueError("Excel file must have a 'Sheet' column")
        
        # Get all matching sheets
        if process_subblocks:
            # Find all sheets that start with the selected sheet name
            all_sheets = df['Sheet'].unique()
            matching_sheets = [s for s in all_sheets if s.startswith(sheet_name)]
            matching_sheets.sort()
            
            if not matching_sheets:
                print_warning(f"No sheets found starting with '{sheet_name}'")
                return
            
            print_success(f"Found {len(matching_sheets)} matching sheets:")
            for sheet in matching_sheets:
                print(f"  {Colors.CYAN}- {sheet}{Colors.ENDC}")
            
            print()
            
            # Calculate reliability for each block
            print(f"\n{Colors.CYAN}Processing {len(matching_sheets)} blocks...{Colors.ENDC}")
            results = []
            for i, sheet in enumerate(matching_sheets, 1):
                # Progress indicator
                print(f"  [{i}/{len(matching_sheets)}] {sheet}...", end='\r')
                
                comp_df, lam, R = rm.calculate_block_reliability(
                    df, sheet, 
                    ni=rm.NI, dt=rm.DT, t_mission=rm.T_MISSION,
                    pi_i=rm.PI_I, leos=rm.LEOS, 
                    verbose=False  # Disable verbose to avoid cluttering output
                )
                results.append({
                    'Block': sheet,
                    'Lambda': lam,
                    'Reliability': R,
                    'Components': len(comp_df)
                })
            
            # Clear progress line
            print(f"  {Colors.GREEN}✓ All blocks processed{Colors.ENDC}" + " " * 50)
            
            # Display summary
            print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}")
            print(f"RELIABILITY ANALYSIS SUMMARY")
            print(f"{'='*80}{Colors.ENDC}\n")
            
            # Create formatted table
            print(f"{Colors.BOLD}{'Block':<55} {'Comp':>6} {'Lambda (FPH)':>15} {'Reliability':>12}{Colors.ENDC}")
            print(f"{Colors.CYAN}{'-'*80}{Colors.ENDC}")
            
            for r in results:
                # Color code by reliability
                if r['Reliability'] > 0.99:
                    color = Colors.GREEN
                elif r['Reliability'] > 0.95:
                    color = Colors.CYAN
                elif r['Reliability'] > 0.90:
                    color = Colors.YELLOW
                else:
                    color = Colors.RED
                
                print(f"{r['Block']:<55} {r['Components']:>6} {r['Lambda']:>15.6e} "
                      f"{color}{r['Reliability']:>12.6f}{Colors.ENDC}")
            
            # Calculate group reliability (all in series)
            lambda_total = sum(r['Lambda'] for r in results)
            R_total = rm.series_reliability([r['Reliability'] for r in results])
            
            print(f"{Colors.CYAN}{'-'*80}{Colors.ENDC}")
            print(f"{Colors.GREEN}{Colors.BOLD}{'SYSTEM TOTAL (Series)':<55} "
                  f"{sum(r['Components'] for r in results):>6} "
                  f"{lambda_total:>15.6e} {R_total:>12.6f}{Colors.ENDC}\n")
            
            # Mission statistics
            years = rm.T_MISSION / (365 * 24)
            print(f"{Colors.CYAN}{'='*80}{Colors.ENDC}")
            print(f"{Colors.BOLD}Mission Parameters:{Colors.ENDC}")
            print(f"  Duration: {rm.T_MISSION:,} hours ({years:.2f} years)")
            print(f"  Cycles per year: {rm.NI:,}")
            print(f"  Temperature cycle amplitude: {rm.DT}°C")
            
            print(f"\n{Colors.BOLD}Interpretation:{Colors.ENDC}")
            print(f"  {Colors.GREEN}Green (R > 0.99){Colors.ENDC}  - Excellent reliability")
            print(f"  {Colors.CYAN}Cyan (R > 0.95){Colors.ENDC}   - Good reliability")
            print(f"  {Colors.YELLOW}Yellow (R > 0.90){Colors.ENDC} - Acceptable reliability")
            print(f"  {Colors.RED}Red (R ≤ 0.90){Colors.ENDC}    - Poor reliability (needs attention)")
            print(f"{Colors.CYAN}{'='*80}{Colors.ENDC}")
            
        else:
            # Single block calculation
            comp_df, lam, R = rm.calculate_block_reliability(
                df, sheet_name,
                ni=rm.NI, dt=rm.DT, t_mission=rm.T_MISSION,
                pi_i=rm.PI_I, leos=rm.LEOS,
                verbose=True
            )
            
            if not comp_df.empty:
                print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}")
                print(f"COMPONENT BREAKDOWN")
                print(f"{'='*80}{Colors.ENDC}\n")
                
                # Format component table nicely
                print(f"{Colors.BOLD}{'Reference':<15} {'Class':<35} {'Lambda (FPH)':>15} {'Reliability':>12}{Colors.ENDC}")
                print(f"{Colors.CYAN}{'-'*80}{Colors.ENDC}")
                
                for idx, row in comp_df.iterrows():
                    # Color code by reliability
                    if pd.isna(row['Reliability']):
                        color = Colors.RED
                        rel_str = "N/A"
                    elif row['Reliability'] > 0.999:
                        color = Colors.GREEN
                        rel_str = f"{row['Reliability']:.6f}"
                    elif row['Reliability'] > 0.99:
                        color = Colors.CYAN
                        rel_str = f"{row['Reliability']:.6f}"
                    else:
                        color = Colors.YELLOW
                        rel_str = f"{row['Reliability']:.6f}"
                    
                    print(f"{row['Reference']:<15} {row['Class']:<35} "
                          f"{row['Failure_rate']:>15.6e} {color}{rel_str:>12}{Colors.ENDC}")
                
                print(f"{Colors.CYAN}{'-'*80}{Colors.ENDC}")
                
                # Block summary
                valid_count = comp_df['Failure_rate'].gt(0).sum()
                print(f"\n{Colors.BOLD}Block Summary:{Colors.ENDC}")
                print(f"  Valid components: {valid_count}/{len(comp_df)}")
                print(f"  Total lambda: {lam:.6e} failures/hour")
                
                # Color code block reliability
                if R > 0.99:
                    color = Colors.GREEN
                elif R > 0.95:
                    color = Colors.CYAN
                elif R > 0.90:
                    color = Colors.YELLOW
                else:
                    color = Colors.RED
                
                print(f"  Block reliability: {color}{R:.6f}{Colors.ENDC}")
            
            # Mission time in years
            years = rm.T_MISSION / (365 * 24)
            print(f"\n{Colors.CYAN}{'='*80}{Colors.ENDC}")
            print(f"{Colors.BOLD}Mission Parameters:{Colors.ENDC}")
            print(f"  Duration: {rm.T_MISSION:,} hours ({years:.2f} years)")
            print(f"  Survival probability: {R*100:.2f}%")
            print(f"{Colors.CYAN}{'='*80}{Colors.ENDC}")
    
    if safe_execute(execute, "Block reliability calculation failed"):
        print_success("\nCalculation completed successfully!")
    else:
        print_error("Calculation failed. Please check the error messages above.")

def run_task1():
    """Execute Task 1: Monte Carlo Simulation."""
    print_header("TASK 1: MONTE CARLO SIMULATION")
    
    # Get Excel file
    excel_file = get_excel_file()
    if excel_file is None:
        print_warning("Task cancelled.")
        return
    
    # Get sheet name
    sheet_name = get_sheet_name(excel_file)
    if sheet_name is None:
        print_warning("Task cancelled.")
        return
    
    # Execute Task 1
    print_info("Starting Monte Carlo analysis...")
    
    def execute():
        mc.run_monte_carlo_analysis(str(excel_file), sheet_name)
    
    if safe_execute(execute, "Monte Carlo analysis failed"):
        print_success("Task 1 completed successfully!")
    else:
        print_error("Task 1 failed. Please check the error messages above.")

def run_task2():
    """Execute Task 2: Sensitivity Analysis."""
    print_header("TASK 2: SENSITIVITY ANALYSIS")
    
    # Get Excel file
    excel_file = get_excel_file()
    if excel_file is None:
        print_warning("Task cancelled.")
        return
    
    # Get sheet name
    sheet_name = get_sheet_name(excel_file)
    if sheet_name is None:
        print_warning("Task cancelled.")
        return
    

    # Execute Task 2
    print_info("Starting sensitivity analysis...")
    
    def execute():
        sa.run_sensitivity_analysis(str(excel_file), sheet_name)
    
    if safe_execute(execute, "Sensitivity analysis failed"):
        print_success("Task 2 completed successfully!")
    else:
        print_error("Task 2 failed. Please check the error messages above.")

def main():
    """Main application loop."""
    print_header("RELIABILITY ANALYSIS STUDENT PROJECT")
    
    print(f"{Colors.CYAN}Welcome to the Reliability Analysis Tool!{Colors.ENDC}")
    print("This tool helps you analyze electronic component reliability using")
    print("Monte Carlo simulation and sensitivity analysis methods.\n")
    
    # Check environment
    if not check_environment():
        print_error("\nEnvironment check failed!")
        print_info("Please resolve the issues above before continuing.")
        proceed = input(f"\n{Colors.YELLOW}Continue anyway? (y/n): {Colors.ENDC}").lower()
        if proceed != 'y':
            print_info("Exiting...")
            return

    # Main loop
    while True:
        try:
            choice = display_menu()
            if choice == '1':
                run_block_reliability()
            elif choice == '2':
                run_task1()
            elif choice == '3':
                run_task2()
            elif choice == '4':
                print("\n")
                check_environment()
            elif choice == '5':
                show_help()
            elif choice == '0':
                print_info("Thank you for using the Reliability Analysis Tool!")
                print_success("Goodbye!")
                break
            else:
                print_error("Invalid choice. Please select 0-5.")
            
            # Pause before showing menu again
            if choice in ['1', '2', '3']:
                input(f"\n{Colors.BOLD}Press Enter to return to menu...{Colors.ENDC}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Interrupted by user.{Colors.ENDC}")
            confirm = input(f"{Colors.YELLOW}Do you want to exit? (y/n): {Colors.ENDC}").lower()
            if confirm == 'y':
                print_info("Exiting...")
                break
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            print(f"{Colors.YELLOW}{traceback.format_exc()}{Colors.ENDC}")
            proceed = input(f"{Colors.YELLOW}Continue? (y/n): {Colors.ENDC}").lower()
            if proceed != 'y':
                break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"Fatal error: {e}")
        print(f"{Colors.YELLOW}{traceback.format_exc()}{Colors.ENDC}")
        sys.exit(1)
