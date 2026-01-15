# Reliability_Analysis

In this repository you will find:
1. Reliability_Total - Contains all of the components for the entire project, can be filtered using the Sheet tab (i.e for components in the Power Block you will take anything that has /Project Architecture/Power/*)
2. Reliability_Max_Min - Contains the max and min values for the components that have values that can alternate. Note this is not all components. Also note for the tables there is no Max for Table 17 and no min for Table 18. This is due to constraints from the manufacturer.

## How to use Main and where do I code?
There is a User_guide.pdf in the repo that shows you the workflow of the main.py and the project.

The code contains the following files:
```
Reliability_Analysis/
├── main.py                             # Main execution code
├── reliability_math.py                 # Math library from standard
├── task1_monte_calo.py                 # Task1 file
├── task2_sensitivity_analysis.py       # Task2 file
```

The idea is to have a decoupled and independant workflow. Each group can work directly in the file allocated to them (task1_monte_carlo.py or task2_sensitivity_analysis.py)
without worrying about the main.py at the beginning. For each task I have already defined a function that is already called in the main (do not change the signature! If you 
do you will need to change the main.py).

The main objective here is to allow students to focus initially on the mathematics of the task and the code in their own sandbox. Once they are more advanced and start to automate, the choice is given to either change the main.py or directly automate within their own files in the function already defined. I strongly recommend students take a 
look at the run_block_reliability() in main.py for the automation. 

### For any automation question or code questions, please open an issue.

## How to ask questions?
Click on Issues at the top (next to 'Code' tab) -> New Issue -> Your problem -> Create
If you have code feel free to add it as well.

## How will your code be used?
For those of you who are interested you can take a look at this repo: https://github.com/Eliot-Abramo/Space-Grade-Reliability-Test

This is our Kicad API that will integrate your work eventually. 

