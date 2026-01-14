"""
Reliability Math Library
========================
Mathematical functions for electronic component failure rate calculations
Based on IEC standards for reliability engineering.
"""

import math as mat
import numpy as np
import pandas as pd


# Simple color codes for terminal output (optional, won't break if not used)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# ============================================================================
# CONSTANTS
# ============================================================================
NI = 5256  # Number of cycles per year
DT = 3     # Amplitude of cycles (°C)
T_MISSION = 43800  # Mission time in hours
PI_I = 1   # Overstress factor
LEOS = 40  # Electrical overstress baseline

# ============================================================================
# COMPONENT CHARACTERISTICS (IEC Pages 33-37)
# ============================================================================

def l_1(car):
    """Lambda_1 constant based on component characteristics (IEC page 33)"""
    characteristics = {
        "MOS Standard, Digital circuits, 20000 transistors": 2.7e-4,
        "MOS Standard, Digital circuits, 810 transistors": 2.7e-4,
        "MOS Standard, Digital circuits, 2 gates": 3.4e-6,
        "BICMOS, STAM, Static Read Access Memory, 8-bit": 6.8e-7,
        "MOS Asic, Gate Arrays, 12 gates": 2.0e-5,
        "Bipolar, Linear/Digital circuit low voltage, 15 transistors": 2.7e-4,
        "BICMOS, linear/digital circuits, high voltage, 500 transistors": 2.7e-3,
        "Bipolar circuits, linear/digital circuits, high voltage, 5000 transistors": 2.7e-2,
        "BICMOS, linear/digital circuits, high voltage, 20 transistors": 2.7e-3,
        "BICMOS, linear/digital circuits, low voltage, 20 transistors": 2.7e-4
    }
    return characteristics.get(car, 0)

def l_2(car):
    """Lambda_2 constant based on component characteristics (IEC page 34)"""
    characteristics = {
        "MOS Standard, Digital circuits, 20000 transistors": 20,
        "MOS Standard, Digital circuits, 810 transistors": 20,
        "MOS Standard, Digital circuits, 2 gates": 1.7,
        "BICMOS, STAM, Static Read Access Memory, 8-bit": 8.8,
        "MOS Asic, Gate Arrays, 12 gates": 10,
        "Bipolar, Linear/Digital circuit low voltage, 15 transistors": 20,
        "BICMOS, linear/digital circuits, high voltage, 500 transistors": 20,
        "Bipolar circuits, linear/digital circuits, high voltage, 5000 transistors": 20,
        "BICMOS, linear/digital circuits, high voltage, 20 transistors": 20,
        "BICMOS, linear/digital circuits, low voltage, 20 transistors": 20
    }
    return characteristics.get(car, 0)


def N(car):
    """Number of transistors based on component type"""
    transistor_counts = {
        "MOS Standard, Digital circuits, 20000 transistors": 20000,
        "MOS Standard, Digital circuits, 810 transistors": 810,
        "MOS Standard, Digital circuits, 2 gates": 8,
        "BICMOS, STAM, Static Read Access Memory, 8-bit": 32,
        "MOS Asic, Gate Arrays, 12 gates": 48,
        "Bipolar, Linear/Digital circuit low voltage, 15 transistors": 15,
        "BICMOS, linear/digital circuits, high voltage, 500 transistors": 500,
        "Bipolar circuits, linear/digital circuits, high voltage, 5000 transistors": 5000,
        "BICMOS, linear/digital circuits, high voltage, 20 transistors": 20,
        "BICMOS, linear/digital circuits, low voltage, 20 transistors": 20
    }
    return transistor_counts.get(car, 0)


# ============================================================================
# INTEGRATED CIRCUITS (IEC 7.3, Page 31)
# ============================================================================

def pi_n_i(n_i):
    """Cycling factor for integrated circuits"""
    if n_i <= 8760:
        return n_i ** 0.76
    else:
        return 1.7 * (n_i ** 0.6)


def pi_t_i(t_j, typ):
    """Temperature factor for integrated circuits
    
    Args:
        t_j: Junction temperature (°C)
        typ: Circuit type
    """
    bipolar_types = [
        "Bipolar, Linear/Digital circuit low voltage, 15 transistors",
        "Bipolar circuits, linear/digital circuits, high voltage, 5000 transistors",
        "BICMOS, linear/digital circuits, high voltage, 500 transistors",
        "BICMOS, linear/digital circuits, high voltage, 20 transistors"
    ]
    
    if typ in bipolar_types:
        return mat.exp(4640 * ((1/328) - (1/(273 + t_j))))
    else:
        return mat.exp(3480 * ((1/328) - (1/(273 + t_j))))


def pi_alpha(typs, typc):
    """Thermal expansion mismatch factor
    
    Args:
        typs: Substrate material type
        typc: Component material type
    """
    als = 16 if typs == "Epoxy" else 0
    alc = 21.5 if typc == "FR4" else 0
    return 0.06 * (np.abs(als - alc) ** 1.68)


def lambda_die_i(a, car, t_j, typ):
    """Die failure rate for integrated circuits
    
    Args:
        a: Construction year
        car: Component characteristics
        t_j: Junction temperature
        typ: Circuit type
    """
    return (l_1(car) * N(car) * mat.exp(-0.35 * (a - 1998)) + l_2(car)) * pi_t_i(t_j, typ)


def lambda_package_i(typs, typc, n_i, dt, car2, l3):
    """Package failure rate for integrated circuits
    
    Args:
        typs: Substrate material
        typc: Component material
        n_i: Cycles per year
        dt: Temperature cycle amplitude
        car2: Package characteristics
        l3: Lambda_3 value
    """
    return 2.75e-3 * pi_alpha(typs, typc) * pi_n_i(n_i) * (dt ** 0.68) * l3


def lambda_int(a, t_j, typs, typc, n_i, dt, car, car2, l3):
    """Total failure rate for integrated circuits (IEC 7.3)
    
    Returns:
        Failure rate in failures per hour
    """
    return (lambda_die_i(a, car, t_j, car) + 
            lambda_package_i(typs, typc, n_i, dt, car2, l3) + 40) * 1e-9


# ============================================================================
# DIODES (IEC 8.2 and 8.3, Pages 38-41)
# ============================================================================

def pi_n_d(n_i):
    """Cycling factor for diodes"""
    if n_i <= 8760:
        return n_i ** 0.76
    else:
        return 1.7 * (n_i ** 0.6)


def pi_t_d(t_j):
    """Temperature factor for diodes
    
    Args:
        t_j: Junction temperature (°C)
    """
    return mat.exp(4640 * ((1/313) - (1/(273 + t_j))))


def l_0_dio(car, typ):
    """Base failure rate for diodes based on function and type
    
    Args:
        car: Diode function (signal, recovery, zener, etc.)
        typ: Diode power level (Low power diode (8.2) or Power diodes (8.3))
    """
    rates = {
        "signal": 0.07,
        "recovery": {"Power diodes (8.3)": 0.7, "Low power diode (8.2)": 0.1},
        "zener": {"Power diodes (8.3)": 0.7, "Low power diode (8.2)": 0.4},
        "transient": {"Power diodes (8.3)": 0.7, "Low power diode (8.2)": 2.3},
        "trigger": {"Power diodes (8.3)": 3, "Low power diode (8.2)": 2},
        "gallium": {"Power diodes (8.3)": 1, "Low power diode (8.2)": 0.3},
        "thyristors": {"Power diodes (8.3)": 3, "Low power diode (8.2)": 1}
    }
    
    if car == "signal":
        return rates[car]
    return rates.get(car, {}).get(typ, 0)


def lambda_die_d(car, t_j, typ):
    """Die failure rate for diodes
    
    Args:
        car: Diode function
        t_j: Junction temperature
        typ: Diode type
    """
    pi_u = 10 if car == "thyristors" else 1
    return pi_u * l_0_dio(car, typ) * pi_t_d(t_j)


def lambda_package_d(ni, dt, lb):
    """Package failure rate for diodes"""
    return 2.75e-3 * pi_n_d(ni) * (dt ** 0.68) * lb


def lambda_overstress_d(pi_i, l_eos):
    """Electrical overstress failure rate for diodes"""
    return pi_i * l_eos


def lambda_diode(car, t_j, n_i, dt, lb, pi_i, l_eos, typ):
    """Total failure rate for diodes (IEC 8.2 and 8.3)
    
    Returns:
        Failure rate in failures per hour
    """
    return (lambda_die_d(car, t_j, typ) + 
            lambda_package_d(n_i, dt, lb) + 
            lambda_overstress_d(pi_i, l_eos)) * 1e-9


# ============================================================================
# TRANSISTORS (IEC 8.4 and 8.5, Pages 42-45)
# ============================================================================

def pi_n_t(n_i):
    """Cycling factor for transistors"""
    if n_i <= 8760:
        return n_i ** 0.76
    else:
        return 1.7 * (n_i ** 0.6)


def pi_t_t(t_j, typ1):
    """Temperature factor for transistors
    
    Args:
        t_j: Junction temperature (°C)
        typ1: Transistor type (Bipolar or MOS)
    """
    if typ1 == "Bipolar":
        return mat.exp(4640 * ((1/373) - (1/(t_j + 273))))
    elif typ1 == "MOS":
        return mat.exp(3480 * ((1/373) - (1/(t_j + 273))))
    return 0


def l_0_trans(typ2):
    """Base failure rate for transistors
    
    Args:
        typ2: Power level (low or not low)
    """
    return 0.75 if typ2 == "low" else 2


def pi_s_t(typ1, mce, mice, mds, mids, mgs, migs):
    """Stress factor for transistors
    
    Args:
        typ1: Transistor type (Bipolar or MOS)
        mce: Maximum repetitive applied VCE voltage
        mice: Minimum specified VCE breakdown voltage
        mds: Maximum repetitive applied VDS voltage
        mids: Minimum specified VDS voltage
        mgs: Maximum repetitive applied VGS voltage
        migs: Minimum specified VGS voltage
    """
    if typ1 == "Bipolar":
        s = mce / mice
        return 0.22 * mat.exp(1.7 * s)
    elif typ1 == "MOS":
        s1 = mds / mids
        s1_factor = 0.22 * mat.exp(1.7 * s1)
        s2 = mgs / migs
        s2_factor = 0.22 * mat.exp(3 * s2)
        return s1_factor * s2_factor
    return 0


def lamba_die_trans(t_j, typ1, typ2, mce, mice, mds, mids, mgs, migs):
    """Die failure rate for transistors"""
    s = pi_t_t(t_j, typ1)
    pi_s = pi_s_t(typ1, mce, mice, mds, mids, mgs, migs)
    return pi_s * l_0_trans(typ2) * s


def lambda_package_trans(n_i, dt, lb):
    """Package failure rate for transistors"""
    s = pi_n_t(n_i) * (dt ** 0.68)
    return 2.75e-3 * s * lb


def lambda_overstress_trans(p_I, l_eos):
    """Electrical overstress failure rate for transistors"""
    return p_I * l_eos


def lambda_transistors(n_i, t_j, typ1, typ2, dt, lb, p_I, l_eos, mce, mice, mds, mids, mgs, migs):
    """Total failure rate for transistors (IEC 8.4 and 8.5)
    
    Returns:
        Failure rate in failures per hour
    """
    return (lamba_die_trans(t_j, typ1, typ2, mce, mice, mds, mids, mgs, migs) + 
            lambda_package_trans(n_i, dt, lb) + 
            lambda_overstress_trans(p_I, l_eos)) * 1e-9


# ============================================================================
# CAPACITORS (IEC 10.3 and 10.4, Pages 57-58)
# ============================================================================

def pi_t_c(ta, typ):
    """Temperature factor for capacitors
    
    Args:
        ta: Ambient temperature (°C)
        typ: Capacitor type (dielectrique or tantlum)
    """
    if typ == "dielectrique":
        return mat.exp(1160 * ((1/303) - (1/(273 + ta))))
    elif typ == "tantlum":
        return mat.exp(1740 * ((1/303) - (1/(273 + ta))))
    return 0


def pi_n_c(ni):
    """Cycling factor for capacitors"""
    return ni ** 0.76


def lambda_capacitors(n_i, ta, dt, typ):
    """Total failure rate for capacitors (IEC 10.3 and 10.4)
    
    Args:
        n_i: Cycles per year
        ta: Ambient temperature
        dt: Temperature cycle amplitude
        typ: Capacitor type (dielectrique or tantlum)
    
    Returns:
        Failure rate in failures per hour
    """
    s1 = pi_t_c(ta, typ)
    s2 = pi_n_c(n_i) * (dt ** 0.68)
    
    if typ == "dielectrique":
        return (0.15 * (s1 + 3.3e-3 * s2)) * 1e-9
    elif typ == "tantlum":
        return (0.4 * (s1 + 3.8e-3 * s2)) * 1e-9
    return 0


# ============================================================================
# RESISTORS (IEC 11.1, Page 65)
# ============================================================================

def pi_tr(t_a, op, rp):
    """Temperature factor for resistors
    
    Args:
        t_a: Ambient temperature (°C)
        op: Operating power (W)
        rp: Rated power (W)
    """
    t_r = t_a + 85 * (op / rp)
    return mat.exp(1740 * ((1/303) - (1/(273 + t_r))))


def pi_nr(n_i):
    """Cycling factor for resistors"""
    if n_i <= 8760:
        return n_i ** 0.76
    else:
        return 1.7 * (n_i ** 0.6)


def lambda_resistors(t_a, op, rp, dt, ni):
    """Total failure rate for resistors (IEC 11.1)
    
    Args:
        t_a: Ambient temperature
        op: Operating power
        rp: Rated power
        dt: Temperature cycle amplitude
        ni: Cycles per year
    
    Returns:
        Failure rate in failures per hour
    """
    return (0.1 * (pi_tr(t_a, op, rp) + 1.4e-3 * pi_nr(ni) * (dt ** 0.68))) * 1e-9


# ============================================================================
# INDUCTORS AND TRANSFORMERS (IEC 12, Page 73)
# ============================================================================

def pi_n_tr(n_i):
    """Cycling factor for inductors/transformers"""
    if n_i <= 8760:
        return n_i ** 0.76
    else:
        return 1.7 * (n_i ** 0.6)


def tr(ta, po, sur):
    """Calculate radiating temperature
    
    Args:
        ta: Ambient temperature (°C)
        po: Power loss (W)
        sur: Radiating surface (dm²)
    """
    return ta + 8.2 * (po / sur)


def pi_t_tr(tr_temp):
    """Temperature factor for inductors/transformers
    
    Args:
        tr_temp: Radiating temperature from tr() function
    """
    return mat.exp(1740 * (1/303 - 1/(tr_temp + 273)))


def l_0_i(typ1, typ2):
    """Base failure rate for inductors/transformers
    
    Args:
        typ1: Component type (inductor or tranformer)
        typ2: Subtype (low fixed, low variable, Power Inductor, signal, power)
    """
    rates = {
        "inductor": {
            "low fixed": 0.2,
            "low variable": 0.4,
            "Power Inductor": 0.6
        },
        "tranformer": {
            "signal": 1.5,
            "power": 3
        }
    }
    return rates.get(typ1, {}).get(typ2, 0)


def lambda_inductors(typ1, typ2, n_i, dt, ta, po, sur):
    """Total failure rate for inductors/transformers (IEC 12)
    
    Args:
        typ1: Component type (inductor or tranformer)
        typ2: Subtype
        n_i: Cycles per year
        dt: Temperature cycle amplitude
        ta: Ambient temperature
        po: Power loss
        sur: Radiating surface
    
    Returns:
        Failure rate in failures per hour
    """
    s1 = pi_t_tr(tr(ta, po, sur))
    s2 = pi_n_tr(n_i) * (dt ** 0.68)
    return (l_0_i(typ1, typ2) * (s1 + 7e-3 * s2)) * 1e-9


# ============================================================================
# PRIMARY BATTERIES (IEC 19.1, Page 90)
# ============================================================================

def lambda_primary(typ):
    """Failure rate for primary batteries (IEC 19.1)
    
    Args:
        typ: Battery type (should be "Primary batteries (19.1)")
    
    Returns:
        Failure rate in failures per hour
    """
    if typ == "Primary batteries (19.1)":
        return 20 * 1e-9
    return 0


# ============================================================================
# CONVERTERS (IEC 19.6, Page 90)
# ============================================================================

def pi_n_co(n_i):
    """Cycling factor for converters"""
    if n_i <= 8760:
        return n_i ** 0.76
    else:
        return 1.7 * (n_i ** 0.6)


def lambda_converters(W, n_i, dt):
    """Total failure rate for converters (IEC 19.6)
    
    Args:
        W: Power indicator ("W<10" or other for >10W)
        n_i: Cycles per year
        dt: Temperature cycle amplitude
    
    Returns:
        Failure rate in failures per hour
    """
    l_0 = 100 if W == "W<10" else 130
    s = pi_n_co(n_i) * (dt ** 0.68)
    return (l_0 * (1 + 3e-3 * s)) * 1e-9


# ============================================================================
# RELIABILITY CALCULATION FUNCTIONS
# ============================================================================

def l_b(package_type):
    """
    Lambda_B for package types (IEC page 37)
    
    Args:
        package_type: Package type string from Table 18
    
    Returns:
        Lambda_B value for the package
    """
    # Clean up the input string
    if pd.isna(package_type):
        return 1.0
    
    pkg = str(package_type).strip()
    
    package_values = {
        "D2PACK, 3 pins": 5.7,
        "SOT-23, 3 pins": 1.0,
        "SOD-123, 3 pins": 1.0,
        "TO-220, 3 pins": 5.7,
        "DPACK, 6 pins": 5.1,
        "TO-247, 3 pins": 6.9
    }
    
    return package_values.get(pkg, 1.0)  # Default to 1.0 if not found


def reliability_from_lambda(lambda_value, t):
    """Calculate reliability from failure rate
    
    Args:
        lambda_value: Failure rate (failures per hour)
        t: Time (hours)
    
    Returns:
        Reliability (probability of survival)
    """
    return mat.exp(-lambda_value * t)


def series_reliability(R_list):
    """Calculate reliability of components in series (all must work)
    
    Args:
        R_list: List of individual reliabilities
    
    Returns:
        System reliability
    """
    R = 1.0
    for r in R_list:
        R *= r
    return R


def parallel_reliability(R_list):
    """Calculate reliability of components in parallel (at least one must work)
    
    Args:
        R_list: List of individual reliabilities
    
    Returns:
        System reliability
    """
    P_fail = 1.0
    for r in R_list:
        P_fail *= (1 - r)
    return 1.0 - P_fail


# ============================================================================
# BLOCK RELIABILITY CALCULATION
# ============================================================================

def calculate_block_reliability(df, sheet_name, ni=NI, dt=DT, t_mission=T_MISSION, 
                                pi_i=PI_I, leos=LEOS, verbose=True):
    """
    Calculate reliability for a specific block/sheet.
    
    This function processes all components in a given sheet, calculates their
    individual failure rates, and combines them (assuming series configuration)
    to get the block's total failure rate and reliability.
    
    Args:
        df: DataFrame containing component data from Excel
        sheet_name: Name of the sheet/block to analyze
        ni: Number of cycles per year
        dt: Temperature cycle amplitude (°C)
        t_mission: Mission time (hours)
        pi_i: Overstress factor
        leos: Electrical overstress baseline
        verbose: Print progress messages
    
    Returns:
        Tuple of (component_dataframe, total_lambda, block_reliability)
        - component_dataframe: DataFrame with columns ['Reference', 'Class', 'Failure_rate', 'Reliability']
        - total_lambda: Total failure rate for the block (failures/hour)
        - block_reliability: Block reliability R = exp(-lambda_total * t)
    """
    import pandas as pd
    
    # Filter for the specific block (exact match)
    block_df = df[df['Sheet'] == sheet_name].copy()
    
    if block_df.empty:
        if verbose:
            print(f"WARNING: No components found for sheet '{sheet_name}'")
        return pd.DataFrame(), 0.0, 1.0
    
    if verbose:
        print(f"\n{Colors.CYAN}Processing block: {sheet_name}{Colors.ENDC}")
        print(f"Components found: {len(block_df)}")
    
    # Calculate lambda for each component
    lambdas = []
    errors = []
    
    for idx, row in block_df.iterrows():
        component_class = row.get('Class', '')
        reference = row.get('Reference', 'Unknown')
        lam = None
        
        # Skip if class is NaN or empty
        if pd.isna(component_class) or component_class == '':
            if verbose:
                print(f"  WARNING: {reference} has no Class specified, skipping")
            lam = 0.0
            lambdas.append(lam)
            continue
        
        try:
            # Transistors
            if component_class == 'Low Power transistor (8.4)':
                transistor_type = row.get('Transistor type', '')
                typ1 = "MOS" if 'MOS' in str(transistor_type) else "Bipolar"
                
                # Check for required temperature
                if pd.isna(row.get('Temperature_Junction')):
                    errors.append(f"{reference}: Missing Temperature_Junction")
                    lam = 0.0
                else:
                    # Get package lambda value
                    lb = l_b(row.get('Table 18'))
                    
                    # Get voltage parameters (can default to 0 if NaN)
                    vce_max = 0 if pd.isna(row.get('Max repetitive VCE')) else row['Max repetitive VCE']
                    vce_min = 1 if pd.isna(row.get('Min specified VCE')) else row['Min specified VCE']
                    vds_max = 0 if pd.isna(row.get('Max applied VDS')) else row['Max applied VDS']
                    vds_min = 1 if pd.isna(row.get('Min specified VDS')) else row['Min specified VDS']
                    vgs_max = 0 if pd.isna(row.get('Max applied VGS')) else row['Max applied VGS']
                    vgs_min = 1 if pd.isna(row.get('Min specified VGS')) else row['Min specified VGS']
                    
                    lam = lambda_transistors(
                        ni, row['Temperature_Junction'], typ1, "low", dt,
                        lb, pi_i, leos,
                        vce_max, vce_min, vds_max, vds_min, vgs_max, vgs_min
                    )
            
            elif component_class == 'Power Transistor (8.5)':
                transistor_type = row.get('Transistor type', '')
                typ1 = "MOS" if 'MOS' in str(transistor_type) else "Bipolar"
                
                # Check for required temperature
                if pd.isna(row.get('Temperature_Junction')):
                    errors.append(f"{reference}: Missing Temperature_Junction")
                    lam = 0.0
                else:
                    # Get package lambda value
                    lb = l_b(row.get('Table 18'))
                    
                    # Get voltage parameters (can default to 0 if NaN)
                    vce_max = 0 if pd.isna(row.get('Max repetitive VCE')) else row['Max repetitive VCE']
                    vce_min = 1 if pd.isna(row.get('Min specified VCE')) else row['Min specified VCE']
                    vds_max = 0 if pd.isna(row.get('Max applied VDS')) else row['Max applied VDS']
                    vds_min = 1 if pd.isna(row.get('Min specified VDS')) else row['Min specified VDS']
                    vgs_max = 0 if pd.isna(row.get('Max applied VGS')) else row['Max applied VGS']
                    vgs_min = 1 if pd.isna(row.get('Min specified VGS')) else row['Min specified VGS']
                    
                    lam = lambda_transistors(
                        ni, row['Temperature_Junction'], typ1, "not low", dt,
                        lb, pi_i, leos,
                        vce_max, vce_min, vds_max, vds_min, vgs_max, vgs_min
                    )
            
            # Capacitors
            elif component_class == 'Ceramic Capacitor (10.3)':
                if pd.isna(row.get('Temperature_Ambiant')):
                    errors.append(f"{reference}: Missing Temperature_Ambiant")
                    lam = 0.0
                else:
                    lam = lambda_capacitors(ni, row['Temperature_Ambiant'], dt, "dielectrique")
            
            elif component_class == 'Tantlum Capacitor (10.4)':
                if pd.isna(row.get('Temperature_Ambiant')):
                    errors.append(f"{reference}: Missing Temperature_Ambiant")
                    lam = 0.0
                else:
                    lam = lambda_capacitors(ni, row['Temperature_Ambiant'], dt, "tantlum")
            
            # Resistors
            elif component_class == 'Resistor (11.1)':
                required = {
                    'Temperature_Ambiant': row.get('Temperature_Ambiant'),
                    'Operating_Power': row.get('Operating_Power'),
                    'Rated_Power': row.get('Rated_Power')
                }
                missing = [name for name, val in required.items() if pd.isna(val)]
                
                if missing:
                    errors.append(f"{reference}: Missing {', '.join(missing)}")
                    lam = 0.0
                else:
                    lam = lambda_resistors(
                        row['Temperature_Ambiant'],
                        row['Operating_Power'],
                        row['Rated_Power'],
                        dt, ni
                    )
            
            # Inductors
            elif component_class == 'Inductor (12)':
                required = {
                    'Temperature_Ambiant': row.get('Temperature_Ambiant'),
                    'Power loss': row.get('Power loss'),
                    'Radiating surface': row.get('Radiating surface')
                }
                missing = [name for name, val in required.items() if pd.isna(val)]
                
                if missing:
                    errors.append(f"{reference}: Missing {', '.join(missing)}")
                    lam = 0.0
                else:
                    # Parse radiating surface
                    surface_str = str(row['Radiating surface'])
                    try:
                        if 'x' in surface_str:
                            parts = surface_str.split('x')
                            # Surface is in mm x mm, convert to dm^2
                            w = float(parts[0].strip())
                            h = float(parts[1].strip())
                            sur = (w / 100) * (h / 100)
                        else:
                            errors.append(f"{reference}: Invalid surface format '{surface_str}'")
                            sur = 0.0132  # Fallback
                    except:
                        errors.append(f"{reference}: Could not parse surface '{surface_str}'")
                        sur = 0.0132  # Fallback
                    
                    lam = lambda_inductors(
                        "inductor",
                        row.get("Inductor type", "Power Inductor"),
                        ni, dt,
                        row['Temperature_Ambiant'],
                        row['Power loss'],
                        sur
                    )
            
            # Converters
            elif component_class == 'Converter <10W (19.6)':
                lam = lambda_converters("W<10", ni, dt)
            
            elif component_class == 'Converter >10W (19.6)':
                lam = lambda_converters("W>10", ni, dt)
            
            # Diodes
            elif component_class in ['Low power diode (8.2)', 'Power diodes (8.3)']:
                required = {
                    'diode_type': row.get('diode_type'),
                    'Temperature_Junction': row.get('Temperature_Junction')
                }
                missing = [name for name, val in required.items() if pd.isna(val)]
                
                if missing:
                    errors.append(f"{reference}: Missing {', '.join(missing)}")
                    lam = 0.0
                else:
                    # Get package lambda value
                    lb = l_b(row.get('Table 18'))
                    
                    lam = lambda_diode(
                        row['diode_type'],
                        row['Temperature_Junction'],
                        ni, dt, lb,
                        pi_i, leos,
                        component_class
                    )
            
            # Primary batteries
            elif component_class == 'Primary batteries (19.1)':
                lam = lambda_primary(component_class)
            
            # Integrated circuits
            elif component_class == 'Integrated Circuit (7)':
                # Check for required parameters
                required_params = {
                    'Construction Date': row.get('Construction Date'),
                    'Temperature_Junction': row.get('Temperature_Junction'),
                    'alpha_s': row.get('alpha_s'),
                    'alpha_c': row.get('alpha_c'),
                    'Table 16': row.get('Table 16'),
                    'Table 17a': row.get('Table 17a')
                }
                
                missing = [name for name, val in required_params.items() if pd.isna(val)]
                
                if missing:
                    errors.append(f"{reference}: Missing required IC parameters: {', '.join(missing)}")
                    lam = 0.0
                else:
                    # Only calculate if we have all required data
                    lam = lambda_int(
                        row['Construction Date'],
                        row['Temperature_Junction'],
                        row['alpha_s'],
                        row['alpha_c'],
                        ni, dt,
                        row['Table 16'],
                        row['Table 17a'],
                        row.get('Lam3', 1.3)  # Lam3 is optional, has reasonable default
                    )
            
            else:
                if verbose:
                    errors.append(f"Unknown class '{component_class}' for {reference}")
                lam = 0.0
        
        except Exception as e:
            if verbose:
                errors.append(f"Error calculating lambda for {reference}: {type(e).__name__}: {e}")
            lam = 0.0
        
        lambdas.append(lam if lam is not None else 0.0)
    
    # Print errors if any
    if errors and verbose:
        print(f"\n{Colors.YELLOW}Data Quality Issues:{Colors.ENDC}")
        for err in errors[:10]:  # Limit to first 10 errors
            print(f"  {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
        
        # Count components with zero lambda (missing data)
        zero_count = sum(1 for lam in lambdas if lam == 0.0)
        if zero_count > 0:
            print(f"\n{Colors.RED}WARNING: {zero_count}/{len(lambdas)} components have lambda=0 due to missing data{Colors.ENDC}")
            print(f"These components are being EXCLUDED from reliability calculation.")
            print(f"Fix missing parameters in your Excel file for accurate results.")
    
    # Add lambda column
    block_df = block_df.assign(Failure_rate=lambdas)
    
    # Calculate individual reliabilities
    reliabilities = [mat.exp(-lam * t_mission) if lam > 0 else np.nan for lam in lambdas]
    block_df = block_df.assign(Reliability=reliabilities)
    
    # Calculate block totals (series assumption) - only include components with valid lambda
    valid_lambdas = [lam for lam in lambdas if lam > 0]
    lambda_total = sum(valid_lambdas)
    R_block = mat.exp(-lambda_total * t_mission)
    
    if verbose:
        valid_count = len(valid_lambdas)
        total_count = len(lambdas)
        print(f"\n{Colors.CYAN}Block Results:{Colors.ENDC}")
        print(f"Valid components: {valid_count}/{total_count}")
        print(f"Block lambda: {lambda_total:.6e} failures/hour")
        print(f"Block reliability: {R_block:.6f}")
    
    # Return simplified dataframe with Class column
    result_df = block_df[['Reference', 'Class', 'Failure_rate', 'Reliability']].copy()
    
    return result_df, lambda_total, R_block


def calculate_group_reliability(df, sheet_list, ni=NI, dt=DT, t_mission=T_MISSION,
                                pi_i=PI_I, leos=LEOS, verbose=True):
    """
    Calculate reliability for a group of blocks in series.
    
    Args:
        df: DataFrame containing component data
        sheet_list: List of sheet names to process
        ni: Number of cycles per year
        dt: Temperature cycle amplitude
        t_mission: Mission time (hours)
        pi_i: Overstress factor
        leos: Electrical overstress baseline
        verbose: Print progress messages
    
    Returns:
        Tuple of (R_list, lambda_list, R_group, lambda_group)
        - R_list: List of individual block reliabilities
        - lambda_list: List of individual block failure rates
        - R_group: Combined group reliability (series)
        - lambda_group: Combined group failure rate (sum)
    """
    R_list = []
    lambda_list = []
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Processing group of {len(sheet_list)} blocks")
        print(f"{'='*60}")
    
    for sheet in sheet_list:
        _, lam, R = calculate_block_reliability(df, sheet, ni, dt, t_mission, 
                                               pi_i, leos, verbose)
        R_list.append(R)
        lambda_list.append(lam)
    
    # Series combination
    R_group = series_reliability(R_list)
    lambda_group = sum(lambda_list)
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"GROUP RESULTS:")
        print(f"  Total lambda: {lambda_group:.6e} failures/hour")
        print(f"  Group reliability: {R_group:.6f}")
        print(f"{'='*60}")
    
    return R_list, lambda_list, R_group, lambda_group