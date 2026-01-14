
#================= PART 1  : Lambdas estimation with Monte Carlo ==================

#===== Importing the libraries ====

import math as mat
import numpy as np
import pandas as pd


#=============== Preliminary calculations =======================

#Here, we give you the probability law of each random parameters. The values of the other parameters are given in the excel file.

#===== LamB (page 37) ====

#LamB for Q5, Q6, D3, D12 and D2 are following an uniform(5.7, 6.9)
#LamB for D10 and D8 are following an uniform(1, 6.9)
#LamB for Q10, Q14, Q17, Q199, Q20, Q22, Q12, Q13, Q16, Q23, Q26, Q32, Q34, Q36, Q9, Q1, Q11, Q15, Q18, Q2, Q21, Q28, Q3, Q4, Q8, D4, D5, D6 and D7 are following an uniform(1, 6.9)
#LamB for Q24, Q25, Q27,  Q33, Q35, Q37, Q7 are following an uniform(5.7, 6.9)

#===== Lam3 (page 34) ====

#Lam3 for U22 has a prob of 0.5 to be 6.479 and a prob 0.5 to be 1.3 
#Lam3 for U17 and U19 are following an unifrom(0.315, 0.627)
#Lam3 for U11, U21, U3 and U7 are following an uniform(0.202,0.371)
#Lam3 for U42 is following an uniform(0.084,0.118)
#Lam3 for U10, U2 and U6 have a prob of 0.5 to be 4.1 and a prob 0.5 to be 1.3 
#Lam3 U12, U4 and U8 are following an  uniform(1.3,4.1)
#Lam3 for U35 is following an uniform(1.3, 2.94)
#Lam3 for U23, U32,U14, U20,U25, U27,U29,U31,U36,U39,U40 and U41 have a prob of 0.5 to be 1.164 and a prob 0.5 to be 0.2808


#======= VDS =====

#VDS for Q5 and Q6 are following an uniform(17,23)
#All the VDS needed are following an uniform(1.5,2.5)


#====== VCE =====

#VCE for Q10, Q14, Q17,  Q19,  Q20 and Q22 are following an uniform(10,15)
#VCE for Q12, Q13, Q16, Q23, Q26, Q32, Q34, Q36 and Q9 are following an uniform(3,3.6)

#===== Operating Power ====

#OP for U42, U23, U32, U41, U33, U34 and U43 are following an uniform(3,5) 
#OP for L1, L2, L3, L4 and L5 are following an uniform(5,15)
#OP for the rest of the components are following an uniform(0.5,1.5)

#======== FUNCTIONS TO CALCULATE THE FAILURE RATES ======

#==== Given constants ====

ni=5256  #number of cycles per year
dt=3   #amplitude of those cycles
t=43800  #time of the mission in hours
pi_i=1  
leos=40

#those values are constants given in the IEC page 33, 34 and 37
#the data car (ex: "MOS Standard, Digital circuits, 20000 transistors") must be given by the user

def l_1(car):
    if car=="MOS Standard, Digital circuits, 20000 transistors" or car=="MOS Standard, Digital circuits, 810 transistors":
        return 2.7*(10**(-4))
    if car=="MOS Standard, Digital circuits, 2 gates":  #bonne valeur ???
        return 3.4*(10**(-6))
    if car=="BICMOS, STAM, Static Read Access Memory, 8-bit":
        return 6.8*(10**(-7))
    if car=="MOS Asic, Gate Arrays, 12 gates":
        return 2.0*(10**(-5))
    if car=="Bipolar, Linear/Digital circuit low voltage, 15 transistors":
        return 2.7*(10**(-4))
    if car=="BICMOS, linear/digital circuits, high voltage, 500 transistors":
        return 2.7*(10**(-3))
    if car=="Bipolar circuits, linear/digital circuits, high voltage, 5000 transistors":
        return 2.7*(10**(-2))
    if  car=="BICMOS, linear/digital circuits, high voltage, 20 transistors":
        return 2.7*(10**(-3))
    if car=="BICMOS, linear/digital circuits, low voltage, 20 transistors":
        return 2.7*(10**(-4))
    
def l_2(car):
    if car=="MOS Standard, Digital circuits, 20000 transistors" or car=="MOS Standard, Digital circuits, 810 transistors":
        return 20
    if car=="MOS Standard, Digital circuits, 2 gates":
        return 1.7
    if car=="BICMOS, STAM, Static Read Access Memory, 8-bit":
        return 8.8
    if car=="MOS Asic, Gate Arrays, 12 gates":
        return 10
    if car=="Bipolar, Linear/Digital circuit low voltage, 15 transistors":
        return 20
    if car=="BICMOS, linear/digital circuits, high voltage, 500 transistors":
        return 20
    if car=="Bipolar circuits, linear/digital circuits, high voltage, 5000 transistors":
        return 20
    if car=="BICMOS, linear/digital circuits, high voltage, 20 transistors":
        return 20
    if car=="BICMOS, linear/digital circuits, low voltage, 20 transistors":
        return 20

def N(car):
    if car=="MOS Standard, Digital circuits, 20000 transistors":
        return 20000
    if car=="MOS Standard, Digital circuits, 810 transistors":
        return 810
    if car=="MOS Standard, Digital circuits, 2 gates":
        return 8
    if car=="BICMOS, STAM, Static Read Access Memory, 8-bit":
        return 32
    if car=="MOS Asic, Gate Arrays, 12 gates":
        return 48
    if car=="Bipolar, Linear/Digital circuit low voltage, 15 transistors":
        return 15
    if car=="BICMOS, linear/digital circuits, high voltage, 500 transistors":
        return 500
    if car=="Bipolar circuits, linear/digital circuits, high voltage, 5000 transistors":
        return 5000
    if car=="BICMOS, linear/digital circuits, high voltage, 20 transistors":
        return 20
    if car=="BICMOS, linear/digital circuits, low voltage, 20 transistors":
        return 20

#==== Calculation of the failure rate for the integrated circuits (7.3), page 31 ======

#the formula for pi_n is given in the IEC page 31. Same goes with pi_t, pi_alpha and all the lambdas
#for everething bellow, the user must give them
#ni : the anual number of cycles
#t_j : temperature of junction 
#typ : the type of circuit
#typs : material type of the substrate
#typc : material type of the componant
#a: year of construction
#dt : amplitude delta Ti

def pi_n_i(n_i):
    if n_i<=8760:
        return n_i**0.76
    else:
        return 1.7*(n_i**0.6)
    
def pi_t_i(t_j,typ):
    if typ=="Bipolar, Linear/Digital circuit low voltage, 15 transistors" or typ=="Bipolar circuits, linear/digital circuits, high voltage, 5000 transistors" or typ=="BICMOS, linear/digital circuits, high voltage, 500 transistors" or typ=="BICMOS, linear/digital circuits, high voltage, 20 transistors":
        return mat.exp(4640*((1/328)-(1/(273+t_j))))
    else:
        return mat.exp(3480*((1/328)-(1/(273+t_j))))

def pi_alpha(typs,typc):
    if typs=="Epoxy":
        als=16
    if typc=="FR4":
        alc=21.5
    return 0.06*(np.abs(als-alc)**1.68)
    
def lambda_die_i(a,car,t_j,typ):
    return (l_1(car)*N(car)*mat.exp(-0.35*(a-1998))+l_2(car))*pi_t_i(t_j,typ)

def lambda_package_i(typs,typc,n_i,dt,car2,l3):
    return 2.75*(10**(-3))*pi_alpha(typs,typc)*pi_n_i(n_i)*(dt**0.68)*l3

def lambda_int(a,t_j,typs,typc,n_i,dt,car,car2,l3):
    return (lambda_die_i(a,car,t_j,car)+lambda_package_i(typs,typc,n_i,dt,car2,l3)+40)*(10**(-9))

#===== Calculation of the failure rate of the low power diodes (8.2) and the power diodes(8.3), page 38 to 41 ======

#all the function describe something given by the IEC. The values in l_0_dio too

#ni : number of cycle per year
def pi_n_d(n_i):
    if n_i<=8760:
        return n_i**0.76
    else:
        return 1.7*(n_i**0.6)

#t_j : temperature of junction
def pi_t_d(t_j):
    return mat.exp(4640*((1/313)-(1/(273+t_j))))

#car: the function of the diode
#typ: the type of diode : either Power or low Power
def l_0_dio(car,typ):
    if car=="signal":
        return 0.07
    if car=="recovery":
        if typ=="Power diodes (8.3)":
            return 0.7
        if typ=="Low power diode (8.2)":
            return 0.1
    if car=="zener":
        if typ=="Power diodes (8.3)":
            return 0.7
        if typ=="Low power diode (8.2)":
            return 0.4
    if car=="transient":
        if typ=="Power diodes (8.3)":
            return 0.7
        if typ=="Low power diode (8.2)":
            return 2.3
    if car=="trigger":
        if typ=="Power diodes (8.3)":
            return 3
        if typ=="Low power diode (8.2)":
            return 2
    if car=="gallium":
        if typ=="Power diodes (8.3)":
            return 1
        if typ=="Low power diode (8.2)":
            return 0.3
    if car=="thyristors":
        if typ=="Power diodes (8.3)":
            return 3
        if typ=="Low power diode (8.2)":
            return 1

#pi_u is given in the IEC, depending on the function of the diode
def lambda_die_d(car,t_j,typ):
    if car=="thyristors":
        pi_u=10
    else:
        pi_u=1
    return pi_u*l_0_dio(car,typ)*pi_t_d(t_j)

def lambda_package_d(ni,dt,lb):
    return 2.75*(10**(-3))*pi_n_d(ni)*(dt**0.68)*lb

def lambda_overstress_d(pi_i,l_eos):
    return pi_i*l_eos

def lambda_diode(car,t_j,n_i,dt,lb,pi_i,l_eos,typ):
    return (lambda_die_d(car,t_j,typ)+lambda_package_d(n_i,dt,lb)+lambda_overstress_d(pi_i,l_eos))*(10**(-9))

#======== Calculation of the failure rate for the low power transistors and power transistors (8.4 et 8.5), page 42 to 45 =

#all the functions describe formulas given by the IEC

#ni: same as before
def pi_n_t(n_i):
    if n_i<=8760:
        return n_i**0.76
    else:
        return 1.7*(n_i**0.6)

#t_j : temperature of junction
#typ1 : type of the transistor whether bipolar or mos 
def pi_t_t(t_j, typ1):
    if typ1=="Bipolar":
        return mat.exp(4640*((1/373)-(1/(t_j+273))))
    if typ1=="MOS":
        return mat.exp(3480*((1/373)-(1/(t_j+273))))

#the thing variating between low and "normal" transistor is lambda 0. This is given in the IEC
#typ2 : low (chapter 8.4) or not low (chapter 8.5)
def l_0_trans(typ2):
    if typ2=="low":
        return 0.75
    if typ2=="not low":
        return 2

#mce : maximum repetitive applied vce voltage
#mice : minimum specified vce breakdown voltage
#mds : maximum repetitive applied vds voltage
#mids : minimum specified vds voltage
#mgs : maximum repetitive applied vgs voltage
#migs : minimum specified vgs voltage
#typ1 : either Bipolar or MOS
#if bipolar : we only use mce and mice. mds, mids, mgs, migs can be given any float
#if mos: we use mds,mids,mgs and migs. mce and mice can be given any float
def pi_s_t(typ1,mce,mice,mds,mids,mgs,migs):
    if typ1=="Bipolar":
        s=mce/mice
        return 0.22*mat.exp(1.7*s)
    if typ1=="MOS":
        s1=mds/mids
        s1=0.22*mat.exp(1.7*s1)
        s2=mgs/migs
        s2=0.22*mat.exp(3*s2)
        return s1*s2

def lamba_die_trans(t_j,typ1,typ2,mce,mice,mds,mids,mgs,migs):
    s=pi_t_t(t_j,typ1)
    pi_s=pi_s_t(typ1,mce,mice,mds,mids,mgs,migs)
    if typ1=="Bipolar":
        return pi_s*l_0_trans(typ2)*s
    if typ1=="MOS":
        return pi_s*l_0_trans(typ2)*s

def lambda_package_trans(n_i,dt,lb):
    s=pi_n_t(n_i)*(dt**0.68)
    return 2.75*(10**(-3))*s*lb

def lambda_overstress_trans(p_I,l_eos):
    return p_I*l_eos

def lambda_transistors(n_i,t_j,typ1,typ2,dt,lb,p_I,l_eos,mce,mice,mds,mids,mgs,migs):
    return (lamba_die_trans(t_j,typ1,typ2,mce,mice,mds,mids,mgs,migs)+lambda_package_trans(n_i,dt,lb)+lambda_overstress_trans(p_I,l_eos))*(10**(-9))

#======== Calculation of the failure rate of the fixed ceramic dielectric capacitors, tantalum capacitors (10.3,10.4), page 57 and 58 ====

#the functions describe formulas given in the IEC

#ta : ambiant temperature
#type : to determine if we work with a ceramic dielectric capacitor or a tantlum capacitor
def pi_t_c(ta,typ):
    if typ=="dielectrique":
        return mat.exp(1160*((1/303)-(1/(273+ta))))
    if typ=="tantlum":
        return mat.exp(1740*((1/303)-(1/(273+ta))))

def pi_n_c(ni):
    return (ni**0.76)

def lambda_capacitors(n_i,ta,dt,typ):
    s1=pi_t_c(ta,typ)
    s2=pi_n_c(n_i)*(dt**0.68)
    if typ=="dielectrique":
        return (0.15*(s1+3.3*(10**(-3))*s2))*(10**(-9))
    if typ=="tantlum":
        return (0.4*(s1+3.8*(10**(-3))*s2))*(10**(-9))

#===== Calculation of the failure rate of the fixed, low dissipation film resistors (11.1), page 65 ====

#the following values must be given by the user
#t_a : ambiant temperature
#op : operating power
#rp : rated power

def pi_tr(t_a,op,rp):
    t_r=t_a+85*(op/rp)
    return mat.exp(1740*((1/303)-(1/(273+t_r))))

def pi_nr(n_i):
    if n_i<=8760:
        return n_i**0.76
    else:
        return 1.7*(n_i**0.6)

def lambda_resistors(t_a,op,rp,dt,ni):
    return (0.1*(pi_tr(t_a,op,rp)+1.4*(10**(-3))*pi_nr(ni)*(dt**0.68)))*(10**(-9))

#==== Calculation of the failure rate of the inductors and transformers (12), page 73 ===

def pi_n_tr(n_i):
    if n_i<=8760:
        return n_i**0.76
    if n_i>8760:
        return 1.7*(n_i**0.6)

#calculation of tr
#ta : ambiant temperature
#po : power loss (in watt)
#sur : radiating surface (in dm^2)
def tr(ta,po,sur):
    return ta+8.2*(po/sur)

#calculation of pi_t given the tr calculted with the previous function
def pi_t_tr(tr):
    return mat.exp(1740*(1/303-1/(tr+273)))

#low current inductors fixed
#low current inductors variable
#power inductors

#signal transformers
#power transformers

#typ1 : assess if it is an inductor or a transformer
#typ2 : what type of componant
def l_0_i(typ1,typ2):
    if typ1=="inductor":
        if typ2=="low fixed":
            return 0.2
        if typ2=="low variable":
            return 0.4
        if typ2=="Power Inductor":
            return 0.6
    if typ1=="tranformer":
        if typ2=="signal":
            return 1.5
        if typ2=="power":
            return 3

def lambda_inductors(typ1,typ2,n_i,dt,ta,po,sur):
    s1=pi_t_tr(tr(ta,po,sur))
    s2=pi_n_tr(n_i)*(dt**0.68)
    return (l_0_i(typ1,typ2)*(s1+7*(10**(-3))*s2))*(10**(-9)) 

#=== Calculation failure rate of the primary battery (19.1), page 90 ===

#20 is used because the table page 90 gives it

def lambda_primary(typ):
    if typ=="Primary batteries (19.1)":
        return 20*(10**(-9))

#=== Calculation of the failure rate of the converters (19.6), page 90 ===

def pi_n_co(n_i):
    if n_i<=8760:
        return n_i**0.76
    if n_i>8760:
        return 1.7*(n_i**0.6)

#W is an indicator to assess if the converter is <10W or >10W
def lambda_converters(W,n_i,dt):
    if W=="W<10":
        l_0=100
    else:
        l_0=130
    s=pi_n_co(n_i)*(dt**0.68)
    return (l_0*(1+3*(10**(-3))*s))*(10**(-9))

#============= PART 2 : SENSITIVITY ANALISYS =====

# We give you a function to calculte the reliability of each bloc. YOU MUST MODIFY IT FOR IT TO WORK, THE FUNCTION NEED TO BE ADAPTED TO YOUR NEW TYPE OF DATA 


#==== The reliability function =====

#here, we define a new reliability function, so that we can calculate the result faster

def relia(sheet,ni=5256,dt=3,t=43800,pi_i=1,lameos=40):
    proba=[]
    #we import the excel
    tab=pd.read_excel('Reliability_Total.xlsx')
    #we drop the columns that are not needed
    tab=tab.drop('Value', axis=1) 

    typ=sheet
    #typ must be the exact name of the bloc indicated in the excel : ex "/Project Architecture/Control/"
    tab=tab[tab['Sheet']==typ]
    #we now have a table for the specific bloc
    for i,row  in tab.iterrows():
        
        #for the transistors
        if row['Class']=='Low Power transistor (8.4)':
            #type of transistors
            if row['Transistor type']=='MOS P channel':
                proba.append(lambda_transistors(ni,row['Temperature_Junction'],"MOS","low",dt,row['Table 18'],pi_i,lameos,row['Max repetitive VCE'],row['Min specified VCE'],row['Max applied VDS'],row['Min specified VDS'],row['Max applied VGS'],row['Min specified VGS']))
            else:
                proba.append(lambda_transistors(ni,row['Temperature_Junction'],"Bipolar","low",dt,row['Table 18'],pi_i,lameos,row['Max repetitive VCE'],row['Min specified VCE'],row['Max applied VDS'],row['Min specified VDS'],row['Max applied VGS'],row['Min specified VGS']))
        if row['Class']=='Power Transistor (8.5)':
            #type of transistors
            if row['Transistor type']=='MOS P channel' or row['Transistor type']=='MOS N channel':
                proba.append(lambda_transistors(ni,row['Construction Date'],"MOS","not low",dt,row['Table 18'],pi_i,lameos,row['Max repetitive VCE'],row['Min specified VCE'],row['Max applied VDS'],row['Min specified VDS'],row['Max applied VGS'],row['Min specified VGS']))
            else:
                proba.append(lambda_transistors(ni,row['Construction Date'],"Bipolar","not low",dt,row['Table 18'],pi_i,lameos,row['Max repetitive VCE'],row['Min specified VCE'],row['Max applied VDS'],row['Min specified VDS'],row['Max applied VGS'],row['Min specified VGS']))
        
        #for the capacitors
        if row['Class']=='Ceramic Capacitor (10.3)':
            typ="dielectrique"
            proba.append(lambda_capacitors(ni,row['Temperature_Ambiant'],dt,typ))
        if row['Class']=='Tantlum Capacitor (10.4)':
            typ="tantlum"
            proba.append(lambda_capacitors(ni,row['Temperature_Ambiant'],dt,typ))
            
        #for the resitors
        if row['Class']=='Resistor (11.1)':
            proba.append(lambda_resistors(row['Temperature_Ambiant'],row['Operating_Power'],row['Rated_Power'],dt,ni))
        
        #for the inductors/transformers
        if row['Class']=='Inductor (12)':
            if row['Radiating surface']=="16.2 x 15.2":
                sur=0.162*0.152
            if row['Radiating surface']=="10.6 x 13.2":
                sur=0.106*0.132
            if row['Radiating surface']=="12 x 11":
                sur=0.12*0.11
            proba.append(lambda_inductors("inductor",row["Inductor type"],ni,dt,row['Temperature_Ambiant'],row['Power loss'],sur))
                
        #for the converters
        if row['Class']=='Converter <10W (19.6)':
            proba.append(lambda_converters(8,ni,dt))  #here, 8 is chosen just to inform the code that we are under 10. It has no impact on the result
        
        #for the diodes
        if row['Class']=='Low power diode (8.2)' or row['Class']=='Power diodes (8.3)':
            proba.append(lambda_diode(row['diode_type'],row['Temperature_Junction'],ni,dt,row['Table 18'],pi_i,lameos,row['Class']))
        
        #for the primary battery
        if row['Class']=='Primary batteries (19.1)':
            proba.append(lambda_primary(row['Class']))
            
        #for the integrated circuit
        if row['Class']=='Integrated Circuit (7)':
            proba.append(lambda_int(row['Construction Date'],row['Temperature_Junction'],row['alpha_s'],row['alpha_c'],ni,dt,row['Table 16'],row['Table 17a']))
      
    
    #we add a column for the failure rate
    tab=tab.assign(Failure_rate=proba)
    proba_indiv=[]
    #we now calculate the individual failure rate
    for i in range(len(proba)):
        proba_indiv.append(mat.exp(-t*proba[i]))
    #we add a column that gives the fiability of each component
    tab=tab.assign(Reliability=proba_indiv)
    #calculation of the global lambda
    lambda_global=sum(proba)
    #gives the reliability of the bloc
    P=mat.exp(-lambda_global*t)
    print("The reliability of the bloc is :", P)
    tab=tab[['Reference','Failure_rate','Reliability']]
    return tab,lambda_global,P


#The previous function gives you the reliability of ONE BLOC. The reliability of the system is given by : 

#calculation for blocs connected in series
def serie(list):
    R=1
    for i in list:
        R=R*i
    return R

#feel free to create your own series function if you don't want to work with lists !

relia('/Project Architecture/Power/')