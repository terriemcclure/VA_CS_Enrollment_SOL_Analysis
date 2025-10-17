# tmcclur-M8_final_project.py: using Python
# ===============================================

# import needed libraries
import sys # to print console output
import pandas as pd  # for data frame creation
import numpy as np # for numeric library
from titlecase import titlecase # for Title case for proper nouns
import os  # for OS interface (to get/change directory)
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress, t


sys.stdout = open("../code_output/tmcclur-M8_final_project_console_output.txt", "w")  # Send all prints to a file
# (Then sys.stdout = sys.__stdout__ to restore normal printing.)
print('=======================================================\n')
print('Assignment: M8.1: Final Project - Python')
print('Name: Terrie McClure') 
print('Email: tmcclur@gmu.edu') 
print('GNumber: G00239649') 
print('Course section: Analytics Big Data to Info, AIT 580, Section 011')
print('\n=======================================================')

# uncomment these 2 lines for full display of output
pd.set_option('display.max_rows', 500)
pd.set_option('display.max.columns', 20)
pd.set_option('display.width', 500)

# display and set working/data directory
os.chdir(r".")
print(os.getcwd())

#########################################
#
# Clean and merge CRDC Computer Science enrollment data with VDOE Virginia SOL assessment data
# First section covers CRDC files
# Second section for VDOE files
# Lastly, merge for analysis
#
############################################

# ===============================================
# read in the CSV files from CRDC
# save original dataframe as backup
CRDC_computer_science_orig = pd.read_csv("../raw_data/CRDC_2021_2022_Computer Science.csv", sep=",", skiprows=0, dtype=str)
CRDC_enrollment_orig = pd.read_csv("../raw_data/CRDC_2021_2022_Enrollment.csv", sep=",", skiprows=0, dtype=str)

# use working file
CRDC_computer_science = pd.read_csv("../raw_data/CRDC_2021_2022_Computer Science.csv", sep=",", skiprows=0, dtype=str)
CRDC_enrollment = pd.read_csv("../raw_data/CRDC_2021_2022_Enrollment.csv", sep=",", skiprows=0, dtype=str)

# clean CRDC column names
CRDC_computer_science.columns = (
    CRDC_computer_science.columns
    .str.strip()            # remove leading/trailing spaces
    .str.lower()            # make lowercase
    .str.replace(' ', '_')  # replace spaces with underscores
    .str.replace(r'[^\w]', '', regex=True)  # remove special characters
)

CRDC_enrollment.columns = (
    CRDC_enrollment.columns
    .str.strip()            # remove leading/trailing spaces
    .str.lower()            # make lowercase
    .str.replace(' ', '_')  # replace spaces with underscores
    .str.replace(r'[^\w]', '', regex=True)  # remove special characters
)

# keep only the columns needed from CRDC_enrollment
crdc_enr_cols_to_keep = [
'lea_state',
'lea_name',
'sch_name',
'sch_enr_hi_m',
'sch_enr_hi_f',
'sch_enr_hi_x',
'sch_enr_am_m',
'sch_enr_am_f',
'sch_enr_am_x',
'sch_enr_as_m',
'sch_enr_as_f',
'sch_enr_as_x',
'sch_enr_hp_m',
'sch_enr_hp_f',
'sch_enr_hp_x',
'sch_enr_bl_m',
'sch_enr_bl_f',
'sch_enr_bl_x',
'sch_enr_wh_m',
'sch_enr_wh_f',
'sch_enr_wh_x',
'sch_enr_tr_m',
'sch_enr_tr_f',
'sch_enr_tr_x',
'tot_enr_m',
'tot_enr_f',
'tot_enr_x',
'sch_enr_idea_m',
'sch_enr_idea_f',
'sch_enr_idea_x',
'sch_enr_el_m',
'sch_enr_el_f',
'sch_enr_el_x'
]

CRDC_enrollment = CRDC_enrollment[crdc_enr_cols_to_keep]

# show year as integer (from school_year) (NOIR = Interval)
CRDC_computer_science['year'] = 2022  
CRDC_enrollment['year'] = 2022

# filter CRDC files for Virginia
CRDC_computer_science = CRDC_computer_science[CRDC_computer_science['lea_state'].str.upper().eq('VA')] 
CRDC_enrollment = CRDC_enrollment[CRDC_enrollment['lea_state'].str.upper().eq('VA')] 

# convert to best data type
CRDC_computer_science = CRDC_computer_science.convert_dtypes()
CRDC_enrollment = CRDC_enrollment.convert_dtypes()

# Convert all relevant columns to integers (or NaN if not convertible)
crdc_cs_cols_to_convert = [
    "sch_compenr_csci_am_f", "sch_compenr_csci_am_m",
    "sch_compenr_csci_as_f", "sch_compenr_csci_as_m",
    "sch_compenr_csci_bl_f", "sch_compenr_csci_bl_m",
    "sch_compenr_csci_hi_f", "sch_compenr_csci_hi_m",
    "sch_compenr_csci_tr_f", "sch_compenr_csci_tr_m",
    "sch_compenr_csci_wh_f", "sch_compenr_csci_wh_m",
    "sch_compenr_csci_hp_f", "sch_compenr_csci_hp_m",
    "sch_compclasses_csci", "tot_compenr_csci_m", "tot_compenr_csci_f",
    "sch_compenr_csci_idea_m", "sch_compenr_csci_idea_f",
    "sch_compenr_csci_el_m", "sch_compenr_csci_el_f"
]

CRDC_computer_science[crdc_cs_cols_to_convert] = (
    CRDC_computer_science[crdc_cs_cols_to_convert]        # Remove commas
      .replace({",": ""}, regex=True)                     # Convert to numeric
      .apply(pd.to_numeric, errors="coerce")
      .apply(lambda col: col.mask(col < 0))               # Replace negatives with NaN
      .astype("Int64")                              
)

# Convert all relevant columns to integers (or NaN if not convertible)
crdc_enr_cols_to_convert = [
    "sch_enr_am_f", "sch_enr_am_m", "sch_enr_am_x",
    "sch_enr_as_f", "sch_enr_as_m", "sch_enr_as_x",
    "sch_enr_bl_f", "sch_enr_bl_m", "sch_enr_bl_x",
    "sch_enr_hi_f", "sch_enr_hi_m", "sch_enr_hi_x",
    "sch_enr_tr_f", "sch_enr_tr_m", "sch_enr_tr_x",
    "sch_enr_wh_f", "sch_enr_wh_m", "sch_enr_wh_x",
    "sch_enr_hp_f", "sch_enr_hp_m", "sch_enr_hp_x",
    "tot_enr_m", "tot_enr_f", "tot_enr_x",
    "sch_enr_idea_m", "sch_enr_idea_f", "sch_enr_idea_x",
    "sch_enr_el_m", "sch_enr_el_f", "sch_enr_el_x"
]

CRDC_enrollment[crdc_enr_cols_to_convert] = (
    CRDC_enrollment[crdc_enr_cols_to_convert]             # Remove commas
      .replace({",": ""}, regex=True)                     # Convert to numeric
      .apply(pd.to_numeric, errors="coerce")
      .apply(lambda col: col.mask(col < 0))               # Replace negatives with NaN
      .astype("Int64")                              
)

# don't differentiate races, sos, or el by gender (get total for each race, sos, or el)
# (but keep the separate gender counts)
CRDC_computer_science['sch_compenr_csci_am'] = CRDC_computer_science['sch_compenr_csci_am_f'] + CRDC_computer_science['sch_compenr_csci_am_m']
CRDC_computer_science['sch_compenr_csci_as'] = CRDC_computer_science['sch_compenr_csci_as_f'] + CRDC_computer_science['sch_compenr_csci_as_m']
CRDC_computer_science['sch_compenr_csci_bl'] = CRDC_computer_science['sch_compenr_csci_bl_f'] + CRDC_computer_science['sch_compenr_csci_bl_m']
CRDC_computer_science['sch_compenr_csci_hi'] = CRDC_computer_science['sch_compenr_csci_hi_f'] + CRDC_computer_science['sch_compenr_csci_hi_m']
CRDC_computer_science['sch_compenr_csci_tr'] = CRDC_computer_science['sch_compenr_csci_tr_f'] + CRDC_computer_science['sch_compenr_csci_tr_m']
CRDC_computer_science['sch_compenr_csci_wh'] = CRDC_computer_science['sch_compenr_csci_wh_f'] + CRDC_computer_science['sch_compenr_csci_wh_m']
CRDC_computer_science['sch_compenr_csci_hp'] = CRDC_computer_science['sch_compenr_csci_hp_f'] + CRDC_computer_science['sch_compenr_csci_hp_m']
CRDC_computer_science['sch_compenr_csci_idea'] = CRDC_computer_science['sch_compenr_csci_idea_f'] + CRDC_computer_science['sch_compenr_csci_idea_m']
CRDC_computer_science['sch_compenr_csci_el'] = CRDC_computer_science['sch_compenr_csci_el_f']+ CRDC_computer_science['sch_compenr_csci_el_m']
CRDC_computer_science['tot_compenr_csci'] = CRDC_computer_science['tot_compenr_csci_f']+ CRDC_computer_science['tot_compenr_csci_m']

CRDC_enrollment['sch_enr_am'] = CRDC_enrollment['sch_enr_am_m'] + CRDC_enrollment['sch_enr_am_f'] + CRDC_enrollment['sch_enr_am_x']
CRDC_enrollment['sch_enr_as'] = CRDC_enrollment['sch_enr_as_m'] + CRDC_enrollment['sch_enr_as_f'] + CRDC_enrollment['sch_enr_as_x']
CRDC_enrollment['sch_enr_bl'] = CRDC_enrollment['sch_enr_bl_m'] + CRDC_enrollment['sch_enr_bl_f'] + CRDC_enrollment['sch_enr_bl_x']
CRDC_enrollment['sch_enr_hi'] = CRDC_enrollment['sch_enr_hi_m'] + CRDC_enrollment['sch_enr_hi_f'] + CRDC_enrollment['sch_enr_hi_x']
CRDC_enrollment['sch_enr_tr'] = CRDC_enrollment['sch_enr_tr_m'] + CRDC_enrollment['sch_enr_tr_f'] + CRDC_enrollment['sch_enr_tr_x']
CRDC_enrollment['sch_enr_wh'] = CRDC_enrollment['sch_enr_wh_m'] + CRDC_enrollment['sch_enr_wh_f'] + CRDC_enrollment['sch_enr_wh_x']
CRDC_enrollment['sch_enr_hp'] = CRDC_enrollment['sch_enr_hp_m'] + CRDC_enrollment['sch_enr_hp_f'] + CRDC_enrollment['sch_enr_hp_x']
CRDC_enrollment['sch_enr_idea'] = CRDC_enrollment['sch_enr_idea_m'] + CRDC_enrollment['sch_enr_idea_f'] + CRDC_enrollment['sch_enr_idea_x']
CRDC_enrollment['sch_enr_el'] = CRDC_enrollment['sch_enr_el_m']+ CRDC_enrollment['sch_enr_el_f'] + CRDC_enrollment['sch_enr_el_x']
CRDC_enrollment['tot_enr'] = CRDC_enrollment['tot_enr_m'] + CRDC_enrollment['tot_enr_f']

# remove gender from race, sos, and el in CRDC_enrollment dataframe
crdc_enr_cols_to_keep = [
'year',
'lea_state',
'lea_name',
'sch_name',
'sch_enr_hi',
'sch_enr_am',
'sch_enr_as',
'sch_enr_hp',
'sch_enr_bl',
'sch_enr_wh',
'sch_enr_tr',
'tot_enr_m',
'tot_enr_f',
'sch_enr_idea',
'sch_enr_el',
'tot_enr'
]

CRDC_enrollment = CRDC_enrollment[crdc_enr_cols_to_keep]

# remove gender from race, sos, and el in CRDC_computer_science dataframe
crdc_cs_cols_to_keep = [
'year',
'lea_state',
'lea_name',
'sch_name',
'sch_compenr_csci_hi',
'sch_compenr_csci_am',
'sch_compenr_csci_as',
'sch_compenr_csci_hp',
'sch_compenr_csci_bl',
'sch_compenr_csci_wh',
'sch_compenr_csci_tr',
'tot_compenr_csci_m',
'tot_compenr_csci_f',
'sch_compenr_csci_idea',
'sch_compenr_csci_el',
'sch_compclasses_csci',
'tot_compenr_csci'
]

CRDC_computer_science = CRDC_computer_science[crdc_cs_cols_to_keep]

# merge the 2 CRDC files on the string fields
CS_merged = pd.merge(
    CRDC_computer_science,
    CRDC_enrollment,
    on=["year", "lea_state", "lea_name", "sch_name"],
    how="inner"
)

# calculate cs enrollment rates by gender, race, sos, and el
CS_merged['sch_hi_cs_enr_rate'] = CS_merged['sch_compenr_csci_hi'] / CS_merged['sch_enr_hi'] * 100
CS_merged['sch_am_cs_enr_rate'] = CS_merged['sch_compenr_csci_am'] / CS_merged['sch_enr_am'] * 100
CS_merged['sch_as_cs_enr_rate'] = CS_merged['sch_compenr_csci_as'] / CS_merged['sch_enr_as'] * 100
CS_merged['sch_hp_cs_enr_rate'] = CS_merged['sch_compenr_csci_hp'] / CS_merged['sch_enr_hp'] * 100
CS_merged['sch_bl_cs_enr_rate'] = CS_merged['sch_compenr_csci_bl'] / CS_merged['sch_enr_bl'] * 100
CS_merged['sch_wh_cs_enr_rate'] = CS_merged['sch_compenr_csci_wh'] / CS_merged['sch_enr_wh'] * 100
CS_merged['sch_tr_cs_enr_rate'] = CS_merged['sch_compenr_csci_tr'] / CS_merged['sch_enr_tr'] * 100
CS_merged['tot_m_cs_enr_rate'] = CS_merged['tot_compenr_csci_m'] / CS_merged['tot_enr_m'] * 100
CS_merged['tot_f_cs_enr_rate'] = CS_merged['tot_compenr_csci_f'] / CS_merged['tot_enr_f'] * 100
CS_merged['sch_idea_cs_enr_rate'] = CS_merged['sch_compenr_csci_idea'] / CS_merged['sch_enr_idea'] * 100
CS_merged['sch_el_cs_enr_rate'] = CS_merged['sch_compenr_csci_el'] / CS_merged['sch_enr_el'] * 100
CS_merged['tot_cs_enr_rate'] = CS_merged['tot_compenr_csci'] / CS_merged['tot_enr'] * 100

# ==================================================================================
# prepare CS_merged for join with SOL_assessments
# join will be on year, school division, and school name
# ==================================================================================

# set divion and school name to title case
CS_merged['sch_name'] = CS_merged['sch_name'].apply(titlecase).astype('string')
CS_merged['lea_name'] = CS_merged['lea_name'].apply(titlecase).astype('string')

# clean division and school name for extra whitespace
CS_merged['lea_name'] = CS_merged['lea_name'].astype(str).str.replace(r'\s+', ' ', regex=True).str.replace(r"^['\"]|['\"]$", "", regex=True).str.replace(r"^['\"]|['\"]$", "", regex=True).str.replace(r'[\t\u00A0]+', ' ', regex=True).str.strip().astype('string')
CS_merged['sch_name'] = CS_merged['sch_name'].astype(str).str.replace(r'\s+', ' ', regex=True).str.replace(r"^['\"]|['\"]$", "", regex=True).str.replace(r'[\t\u00A0]+', ' ', regex=True).str.strip().astype('string')


# apply series of fixes to division names and school names so they match between SOL file and CS enrollment file (normalize join keys)
# most fixes are to the CS_merged file so it matches the SOL file (but not all)

# Dictionary of bad -> good names
cs_division_fix1 = {
    r'\sPBLC SCHS$': ''           # remove public schools from division name. SOL data is only public schools
}

cs_division_fix2 = {
    r'\bCty\b': 'City',             # normalize spelling of City and County
    r'\bCo\b': 'County'
}

cs_division_fix3 = {  # manual fixes of division names that don't fit usual rules
    'Va Beach City': 'Virginia Beach City',  
    'Williamsburg-James City':'Williamsburg-James City County',
    'King Geo County':'King George County'
}

cs_school_fix1 = {           # fixes by rule of CS enrollment school names
    r'\bHigh School$': 'High',
    r'\bMiddle School$': 'Middle',
    r'\bElementary School$': 'Elementary',
    r'\bElem\b' : 'Elementary',
    r'\bSr\b\.?': 'Senior',  # change Sr to Senior
    r'\bHs\b\.?': 'High',  # change Hs to High
    r'\bCo\b\.?': 'County',  # "Co" or "Co."
    r'(\b\w{2,}\s)([A-Za-z])(?!\.)(\s\w+\b)': r'\1\2.\3' # Add period to middle initial
}

cs_school_fix2 = {    # manual fix of school names in CS enrollment data that don't fit usual rules
   "Washington Liberty High": "Washington-Liberty High",
   "Jefferson-Houston Pk-8 Ib" : "Jefferson-Houston PK-8 School",
   "Patrick Henry K-8" : "Patrick Henry K-8 School",
   "Ft Defiance High" : "Fort Defiance High",
   "S Gordon Stewart Middle" : "S. Gordon Stewart Middle",
   "Hugo a. Owens Middle" : "Hugo A. Owens Middle",
   "Dinwiddie High" : "Dinwiddie County High",
   "Dinwiddie Middle" : "Dinwiddie County Middle",
   "Freeman High" : "Douglas S. Freeman High",
   "Kettle Run High SCH" : "Kettle Run High",
   "Paul Laurence Dunbar Mid. For Innov." : "Paul Laurence Dunbar Middle for Innovation",
   "Azalea Middle" : "Azalea Gardens Middle",
   "Booker T. Washington High" : "Booker T Washington High",
   "Ghent School" : "Ghent K-8",
   "Ruffner Middle" : "William H. Ruffner Middle",
   "Southside Stem Academy at Campostella" : "Southside STEM Academy at Campostella",
   "Wm. E. Waters Middle" : "William E. Waters Middle",
   "Charles J. Colgan Sr High" : "Charles J. Colgan Sr. High",
   "Pennington" : "Pennington Traditional",
   "John N. Dalton Int." : "John N. Dalton Intermediate",
   "Moody Middle" : "George H. Moody Middle",
   "Tucker High" : "John Randolph Tucker High",
   "Rolfe Middle" : "John Rolfe Middle",
   "Godwin High" : "Mills E. Godwin High",
   "Maury High" : "Matthew Fontaine Maury High",
   "Charles J. Colgan Senior High" : "Charles J. Colgan Sr. High",
   "Richmond Alternative School" : "Richmond Alternative",
   "Lucy Addison Aerospace Magnet Middle" : "Addison Aerospace Magnet Middle",
   "J.M. Dozier Middle" : "Ella J. Fitzgerald Middle"
}

# apply standardization rules
CS_merged['lea_name'] = CS_merged['lea_name'].replace(cs_division_fix1, regex=True)
CS_merged['lea_name'] = CS_merged['lea_name'].replace(cs_division_fix2, regex=True)
CS_merged['lea_name'] = CS_merged['lea_name'].replace(cs_division_fix3, regex=False)
CS_merged['sch_name'] = CS_merged['sch_name'].replace(cs_school_fix1, regex=True)
CS_merged['sch_name'] = CS_merged['sch_name'].replace(cs_school_fix2, regex=False)

# only rename Thomas Jefferson High if it is in Fairfax County
CS_merged.loc[
    (CS_merged["lea_name"] == "Fairfax County") & (CS_merged["sch_name"] == "Thomas Jefferson High"),
    "sch_name"
] = "Thomas Jefferson High for Science and Technology"

print('====================info===============================\n')
print('\n==CRDC_computer_science=====================================================\n')
print(CRDC_computer_science.info())
print('\n==CRDC_enrollment=====================================================\n')
print(CRDC_enrollment.info())
print('\n==CS_merged=====================================================\n')
print(CS_merged.info())

# ===============================================
# read in the CSV files from VDOE
# save original dataframe as backup
SOL_assessments_orig = pd.read_csv("../raw_data/SOL_assessment_statistics_2021_2022.csv", sep=",", skiprows=0, dtype=str)
SOL_assessments_by_gender_orig = pd.read_csv("../raw_data/SOL_assessment_statistics_2021_2022_by_gender.csv", sep=",", skiprows=0, dtype=str)
SOL_assessments_by_race_orig = pd.read_csv("../raw_data/SOL_assessment_statistics_2021_2022_by_race.csv", sep=",", skiprows=0, dtype=str)

# use working file
SOL_assessments = pd.read_csv("../raw_data/SOL_assessment_statistics_2021_2022.csv", sep=",", skiprows=0, dtype=str)
SOL_assessments_by_gender = pd.read_csv("../raw_data/SOL_assessment_statistics_2021_2022_by_gender.csv", sep=",", skiprows=0, dtype=str)
SOL_assessments_by_race = pd.read_csv("../raw_data/SOL_assessment_statistics_2021_2022_by_race.csv", sep=",", skiprows=0, dtype=str)

# ===========================================
# Common SOL prep for all SOL files
# ===========================================
def prep_sol_data(sol_df):
    # Clean names, fix math, enforce types, set school_level, filter HS & valid totals.
    df = sol_df.copy()

    df.columns = (
       df.columns
       .str.strip()            # remove leading/trailing spaces
       .str.lower()            # make lowercase
       .str.replace(' ', '_')  # replace spaces with underscores
       .str.replace(r'[^\w]', '', regex=True)  # remove special characters
     )

    # --- clean division and school column names ---
    for col in ["division_name", "school_name"]:
         df[col] = (df[col].astype(str)
                            .str.replace(r'\s+', ' ', regex=True)
                            .str.replace(r"^['\"]|['\"]$", "", regex=True)
                            .str.replace(r'[\t\u00A0]+', ' ', regex=True)
                            .str.strip()
                            .apply(titlecase))

    # ==================================================================================
    # prepare SOL_assessment files for join with CRDC data
    # join will be on year, school division, and school name
    # ==================================================================================
    # manual SOL fixes
    sol_division_fix1 = {
        'Alleghany Highlands': 'Alleghany County'   
    }

    sol_school_fix1 = { # manual fix of school name in SOL file to match convention
       "Alexandria City High School": "Alexandria City High",  
       "Richmond Alternative School" : "Richmond Alternative",
       "Ruffner School" : "William H. Ruffner Middle",
       "Jack Jouett Middle" : "Journey Middle",
       "Prince Edward Middle" : "Prince Edward County Middle",
       "Washington & Lee High" : "Westmoreland High"
    }

    df['division_name'] = df['division_name'].replace(sol_division_fix1, regex=False)
    df['school_name'] = df['school_name'].replace(sol_school_fix1, regex=False)

    # Convert all relevant columns to integers (or NaN if not convertible)
    sol_cols_to_convert = [
    "pass_advanced_count",
    "pass_count",
    "pass_proficient_count",
    "fail_count",
    "total_count"
    ]

    df[sol_cols_to_convert] = (
        df[sol_cols_to_convert]                # Remove commas
          .replace({",": ""}, regex=True)                     # Convert to numeric
          .apply(pd.to_numeric, errors="coerce")
          .apply(lambda col: col.mask(col < 0))               # Replace negatives with NaN
          .astype("Int64")                              
    )

    # fix the bad math by replacing pass_count with pass_proficient_count + pass_advanced_count
    # and total_count with pass_count + fail_count
    df["pass_count"] = df["pass_proficient_count"] + df["pass_advanced_count"]
    df["total_count"] = df["pass_count"] + df["fail_count"]

    df['division_name'] = df['division_name'].astype(str).str.replace(r'\s+', ' ', regex=True).str.replace(r"^['\"]|['\"]$", "", regex=True).str.replace(r'[\t\u00A0]+', ' ', regex=True).str.strip()
    df['school_name'] = df['school_name'].astype(str).str.replace(r'\s+', ' ', regex=True).str.replace(r"^['\"]|['\"]$", "", regex=True).str.replace(r'[\t\u00A0]+', ' ', regex=True).str.strip()

    # create NOIR=ordinal school_level with High School and Middle School based on school_name

    cond_elementary = df["school_name"].str.contains(
        r"\b(?:Elementary|Elem)\b",
        case=False, na=False
    )

    cond_middle = df["school_name"].str.contains(
        r"\bJunior[\s-]?High\b|\bMiddle\b|\bIntermediate\b|\bTraditional\b|\bK[-–]8\b|\bPK[-–]8\b",
        case=False, na=False
    )

    cond_high = df["school_name"].str.contains(
        r"\bHigh\b|\bTraditional\b|\bSecondary\b|\bCombined\b|\bAlternative\b|\bAcademy\b|\bCollegiate\b",
        case=False, na=False)

    df["school_level"] = np.select(
        [cond_elementary, cond_middle, cond_high],
        ["Elementary School", "Middle School", "High School"],
        default="Other",
    )

    # manually set school_level for the schools that were not assigned based on the above conditions/rules

    school_level_dictionary = {
        "Hunter B. Andrews" : "Middle School",
        "Lake Taylor" : "High School",
        "The Nokesville School" : "Middle School",
        "Old Donation School" : "Middle School",
        "Community Lab School" : "High School",
        "J.W. Adams Combined" : "Middle School"
    }

    df.loc[df["school_name"].isin(school_level_dictionary), "school_level"] = df["school_name"].map(school_level_dictionary)

    # set key fields to string
    df = df.astype({
         "division_name": "string",
         "school_name": "string",
         "school_level": "string"
     }) 

    # filter out schools where total_count (of SOL test takers) is greater than 0    
    mask = df["total_count"].gt(0).fillna(False)
    df = df[mask]

    # Keep only High Schools
    df = df[df["school_level"].eq("High School")]

    # show year as integer (from school_year) (NOIR = Interval)
    df['year'] = df['school_year'].str.split('-').str[1].astype(int)

    # convert to best data type
    df = df.convert_dtypes()

    print('====================info===============================\n')   
    print('\n==SOL_assessments=====================================================\n')
    print(df.info())

    return df

# ===========================================
# calculate STEM counts and non-STEM counts
# ===========================================
def _split_stem_nonstem(df):
    # create stem flag and create counts by stem and non-stem
    df = df.copy()

    # list of STEM subjects
    stem_subjects = ['Mathematics', 'Science']

    # Calculate derived fields

    # create stem_flag (True if subject is in STEM subjects) (NOIR = Nominal)
    df['stem_flag'] = df['subject'].isin(stem_subjects)

    # create stem_flag_int for loading into database
    df['stem_flag_int'] = df['stem_flag'].astype('Int8')

    # split counts by STEM and Non-STEM
    df['pass_advanced_count_stem']     = df['pass_advanced_count'].where(df['stem_flag_int'].eq(1))
    df['pass_advanced_count_non_stem'] = df['pass_advanced_count'].where(df['stem_flag_int'].eq(0))
    df['pass_count_stem']     = df['pass_count'].where(df['stem_flag_int'].eq(1))
    df['pass_count_non_stem'] = df['pass_count'].where(df['stem_flag_int'].eq(0))
    df['total_count_stem']     = df['total_count'].where(df['stem_flag_int'].eq(1))
    df['total_count_non_stem'] = df['total_count'].where(df['stem_flag_int'].eq(0))

    return df

def _agg_by_school_and_demographic(df, demographic=None):
    # Aggregate to one row per (school_year, division_name, school_name [, demographic])
    demographic = demographic or []
    group_keys = ["school_year", "division_name", "school_name"] + demographic

    sum_cols = [
        "total_count","total_count_stem","total_count_non_stem",
        "pass_advanced_count","pass_advanced_count_stem","pass_advanced_count_non_stem",
        "pass_proficient_count", "fail_count",
        "pass_count","pass_count_stem","pass_count_non_stem",
    ]
    max_cols = ["year","test_level","test_source","school_level","CS_enrollment_rate"]  # these are the same per school

    agg_dict = {**{c: (lambda s: s.sum(min_count=1)) for c in sum_cols},
                **{c: "max" for c in max_cols}}

    df_grouped = (df.groupby(group_keys, as_index=False).agg(agg_dict))

    # calculate pass rates at grouped level
    df_grouped['pass_advanced_rate'] = df_grouped['pass_advanced_count'] / df_grouped['total_count'] * 100
    df_grouped['pass_advanced_rate_stem'] = df_grouped['pass_advanced_count_stem'] / df_grouped['total_count_stem'] * 100
    df_grouped['pass_advanced_rate_non_stem'] = df_grouped['pass_advanced_count_non_stem'] / df_grouped['total_count_non_stem'] * 100
    df_grouped['pass_rate'] = df_grouped['pass_count'] / df_grouped['total_count'] * 100
    df_grouped['pass_rate_stem']  = df_grouped['pass_count_stem'] / df_grouped['total_count_stem'] * 100
    df_grouped['pass_rate_non_stem'] = df_grouped['pass_count_non_stem'] / df_grouped['total_count_non_stem'] * 100

    return df_grouped

# --- columns & titles ---
# use same PANELS / charts for all demographic groups
PANELS = [
    ("pass_rate",               "SOL Pass Rate (%)",                  "CS Enrollment vs SOL Pass Rate"),
    ("pass_advanced_rate",      "SOL Pass Advanced Rate (%)",         "CS Enrollment vs SOL Pass Advanced Rate"),
    ("pass_rate_stem",          "STEM SOL Pass Rate (%)",             "CS Enrollment vs STEM SOL Pass Rate"),
    ("pass_advanced_rate_stem", "STEM SOL Pass Advanced (%)",         "CS Enrollment vs STEM SOL Pass Advanced Rate"),
    ("pass_rate_non_stem",      "Non-STEM SOL Pass Rate (%)",         "CS Enrollment vs Non-STEM SOL Pass Rate"),
    ("pass_advanced_rate_non_stem","Non-STEM SOL Pass Advanced (%)",  "CS Enrollment vs Non-STEM SOL Pass Advanced Rate"),
]

# x axis is the same for all scatterplots
XCOL = "CS_enrollment_rate"

# set pink for girls and blue for boys on gender graph
GENDER_PALETTE = {
    "F": "#ff69b4",  # hot pink
    "M": "#1f77b4",  # matplotlib blue
}

def _plot_panels(df, hue=None, title_suffix="", savepath=None, palette=None):

    # 3x2 panel plot. If hue is provided, draw colored points & a separate fit per level.
    # Returns a tidy stats DataFrame with r, R2, beta, CI per panel and per hue level (if any).

    # Collect stats for export
    stats_rows = []

    fig, axes = plt.subplots(3, 2, figsize=(14, 16), sharex=True, sharey=True)
    axes = axes.ravel()

    for ax, (ycol, ylab, title) in zip(axes, PANELS):
        ax.set_xlim(0, 100); ax.set_ylim(0, 100)
        ax.set_xlabel("CS Enrollment Rate (%)") 
        ax.set_ylabel(ylab)
        ax.set_title(f"{title}{title_suffix}") #title
        ax.grid(True, alpha=0.25)

        data = df[[XCOL, ycol] + ([hue] if hue else [])].dropna()

        if hue is None:
            # scatter + regression (seaborn)
            sns.regplot(data=data, x=XCOL, y=ycol, ax=ax,
                        scatter_kws={"alpha": 0.35, "s": 12},
                        line_kws={"lw": 2},
                        robust=True, truncate=False, ci=None)

            # compute regression stats
            xv = data[XCOL].astype(float).to_numpy()
            yv = data[ycol].astype(float).to_numpy()
            res = linregress(xv, yv)

            beta = res.slope
            r    = res.rvalue
            p    = res.pvalue
            se   = res.stderr

            dfree = len(xv) - 2
            if dfree > 0 and np.isfinite(se):
                tcrit = t.ppf(0.975, dfree); ci_lo = beta - tcrit*se; ci_hi = beta + tcrit*se
            else:
                ci_lo = ci_hi = np.nan
            ax.text(0.04, 0.96, 
                    f"r = {r:.2f}\nR² = {r**2:.2f}\np = {p:.3g}\nβ = {beta:.3f} (95% CI {ci_lo:.3f}, {ci_hi:.3f})",
                    transform=ax.transAxes, ha="left", va="top", fontsize=11,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6", alpha=0.8))


            ax.text(0.96, 0.04, f"N = {len(data)}", transform=ax.transAxes,
                    ha="right", va="bottom", fontsize=10)

            stats_rows.append({
                "panel": ycol, "group": "ALL", "n": len(data),
                "r": r, "R2": r**2, "beta": beta, "p": p, "ci_lo": ci_lo, "ci_hi": ci_hi
            })
        else:
            # Multi-group: colored scatter + line per group
            levels = [g for g in sorted(data[hue].dropna().unique())]
            
            # if no palette provided, make one automatically
            if palette is None:
               # fallback: build a color cycle for the number of levels
               cyc = plt.rcParams['axes.prop_cycle'].by_key().get('color', [])
               # repeat/extend if needed
               colors = (cyc * ((len(levels) // max(1, len(cyc))) + 1))[:len(levels)]
               palette = {g: c for g, c in zip(levels, colors)}


            stat_block = []
            for g in levels:
                gdat = data[data[hue] == g]
                if len(gdat) < 3:
                    continue
                
                color = palette.get(g, None)
                
                # scatter for this group
                h = ax.scatter(
                    gdat[XCOL], gdat[ycol], 
                    alpha=0.45, s=18, label=str(g),
                    color=color, edgecolor="none",
                    marker="o" if str(g).upper()=="F" else "^"  # shape by gender
                )
                
                # stats + line
                xv = gdat[XCOL].astype(float).to_numpy()
                yv = gdat[ycol].astype(float).to_numpy()
                res = linregress(xv, yv)
                beta, r, p, se, intercept = res.slope, res.rvalue, res.pvalue, res.stderr, res.intercept

                # 95% CI for the slope

                dfree = len(xv) - 2
                if dfree > 0 and np.isfinite(se):
                    tcrit = t.ppf(0.975, dfree)
                    ci_lo = beta - tcrit*se 
                    ci_hi = beta + tcrit*se
                else:
                    ci_lo = ci_hi = np.nan

                # fitted line
                xx = np.linspace(0, 100, 200)
                yy = intercept + beta * xx
                
                ax.plot(xx, yy, lw=2, color=color)

                stat_block.append(f"{g}: r={r:.2f}, β={beta:.3f}, p={p:.3g}")
                stats_rows.append({
                    "panel": ycol, "group": str(g), "n": len(gdat),
                    "r": r, "R2": r**2, "beta": beta, "p": p, "ci_lo": ci_lo, "ci_hi": ci_hi
                })
            ax.legend(title=hue, fontsize=9, title_fontsize=10, frameon=True)

            # annotations

            ax.text(0.04, 0.96, "\n".join(stat_block[:5]),  # avoid over-crowding
                    transform=ax.transAxes, ha="left", va="top", fontsize=11,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6", alpha=0.8))

    plt.tight_layout()
    if savepath:
        plt.savefig(savepath, dpi=300, bbox_inches="tight")
    plt.show()

    stats_df = pd.DataFrame(stats_rows)
    return stats_df



##########################################################################################

# #################################################
# remove outliers - function to remove outliers with Z-score >= 3 (to match AWS Glue DataBrew default profile method)
# ################################################

def remove_outliers_zscore(df, cols, z=3.0, by=None):
    """
    Drop rows where ANY of `cols` has |z| > z.
    If `by` is provided (e.g., ['gender'] or ['race']), compute z within each subgroup.
    """
    def _mask(g):
        keep = pd.Series(True, index=g.index)
        for c in cols:
            x = g[c].astype(float)
            mu = x.mean()
            sd = x.std(ddof=0)  # population SD; close to what profilers typically use
            if pd.isna(sd) or sd == 0:
                continue
            zscores = (x - mu) / sd
            keep &= zscores.abs() <= z
        return g.loc[keep]
    return df.groupby(by, group_keys=False, dropna=False).apply(_mask) if by else _mask(df)


# ===========================================
# SOL_CS (no subgroup)
# ===========================================
def build_SOL_CS(SOL_assessments, CS_merged):
    sol = prep_sol_data(SOL_assessments)
    # join
    merged = sol.merge(
        CS_merged,
        left_on=['division_name','school_name','year'],
        right_on=['lea_name','sch_name','year'],
        how='inner'
    )
    merged["CS_enrollment_rate"] = merged["tot_cs_enr_rate"]
    merged = _split_stem_nonstem(merged)
    overall = _agg_by_school_and_demographic(merged)
    return overall

# ===========================================
# SOL_CS BY GENDER
# ===========================================
def build_SOL_CS_by_gender(SOL_assessments_by_gender, CS_merged):
    solg = prep_sol_data(SOL_assessments_by_gender)
    
    # make CS rates long by gender
    cs_gender = CS_merged[["year","lea_name","sch_name","tot_m_cs_enr_rate","tot_f_cs_enr_rate"]].copy()
    cs_gender = cs_gender.melt(id_vars=["year","lea_name","sch_name"],
                               var_name="gvar", value_name="CS_enrollment_rate")
    cs_gender["gender"] = cs_gender["gvar"].map({"tot_m_cs_enr_rate":"M","tot_f_cs_enr_rate":"F"}).astype('string')

    merged = solg.merge(
        cs_gender,
        left_on=["year","division_name","school_name","gender"],
        right_on=["year","lea_name","sch_name","gender"],
        how="inner"
    )
    merged = _split_stem_nonstem(merged)
    gdf = _agg_by_school_and_demographic(merged, demographic=["gender"])
    return gdf

# ===========================================
# SOL_CS BY RACE
# ===========================================
def build_SOL_CS_by_race(SOL_assessments_by_race, CS_merged):
    solr = prep_sol_data(SOL_assessments_by_race)

    race_to_cs_col = {
        "American Indian or Alaska Native": "sch_am_cs_enr_rate",
        "Asian": "sch_as_cs_enr_rate",
        "Black, not of Hispanic origin": "sch_bl_cs_enr_rate",
        "Hispanic": "sch_hi_cs_enr_rate",
        "Non-Hispanic, two or more races": "sch_tr_cs_enr_rate",
        "White, not of Hispanic origin": "sch_wh_cs_enr_rate",
        "Native Hawaiian/Pacific Islander": "sch_hp_cs_enr_rate",
    }
    race_cols = list(race_to_cs_col.values())
    cs_race_long = (CS_merged[["year","lea_name","sch_name"] + race_cols]
                    .melt(id_vars=["year","lea_name","sch_name"],
                          var_name="race_rate_col", value_name="CS_enrollment_rate"))
    inv_map = {v:k for k,v in race_to_cs_col.items()}
    cs_race_long["race"] = cs_race_long["race_rate_col"].map(inv_map).astype('string')

    merged = solr.merge(
        cs_race_long,
        left_on=["year","division_name","school_name","race"],
        right_on=["year","lea_name","sch_name","race"],
        how="inner"
    )
    merged = _split_stem_nonstem(merged)
    rdf = _agg_by_school_and_demographic(merged, demographic=["race"])
    return rdf

######################################################################################

# Build the three analysis datasets
SOL_CS_df = build_SOL_CS(SOL_assessments, SOL_merged := CS_merged)
SOL_CS_by_gender_df  = build_SOL_CS_by_gender(SOL_assessments_by_gender, CS_merged)
SOL_CS_by_race_df    = build_SOL_CS_by_race(SOL_assessments_by_race, CS_merged)

# Save to cleaned CSV files
SOL_CS_df.to_csv("../code_output/SOL_CS.csv", index=False)
SOL_CS_by_gender_df.to_csv("../code_output/SOL_CS_by_gender.csv", index=False)
SOL_CS_by_race_df.to_csv("../code_output/SOL_CS_by_race.csv", index=False)

# Write info about cleaned CSV files to console output
print('====================cleaned info===============================\n')
print('\n==SOL_CS=====================================================\n')
print(SOL_CS_df.info())
print('\n==SOL_CS_by_gender=====================================================\n')
print(SOL_CS_by_gender_df.info())
print('\n==SOL_CS_by_race=====================================================\n')
print(SOL_CS_by_race_df.info())


###############################
# Plot graphs
##############################
# SOL_CS (no breakout by demographic)
SOL_CS_stats = _plot_panels(SOL_CS_df, hue=None,        title_suffix=" (High Schools)",
                             savepath="../code_output/fig_SOL_CS_panels.png")
SOL_CS_by_gender_stats  = _plot_panels(SOL_CS_by_gender_df,  hue="gender",    title_suffix=" (High Schools, by Gender)",
                             savepath="../code_output/fig_SOL_CS_by_gender_panels.png",
                             palette=GENDER_PALETTE,   # <- pink for F, blue for M palette=GENDER_PALETTE,   # <- pink for F, blue for M
                             )
SOL_CS_by_race_stats    = _plot_panels(SOL_CS_by_race_df,    hue="race",      title_suffix=" (High Schools, by Race)",
                             savepath="../code_output/fig_SOL_CS_by_race_panels.png")

# ###################################
# Remove outliers and plot again
# #################################

rate_cols = ["CS_enrollment_rate"] + [y for y,_,_ in PANELS]

# No subgroup
SOL_CS_df_no_outliers = remove_outliers_zscore(SOL_CS_df, rate_cols, z=3.0)

# By gender (z computed within each gender, like separate profiles)
SOL_CS_by_gender_df_no_outliers = remove_outliers_zscore(SOL_CS_by_gender_df, rate_cols, z=3.0, by=["gender"])

# By race
SOL_CS_by_race_df_no_outliers = remove_outliers_zscore(SOL_CS_by_race_df, rate_cols, z=3.0, by=["race"])

# plot with no outliers
SOL_CS__no_outliers_stats = _plot_panels(SOL_CS_df_no_outliers, hue=None,        title_suffix=" (High Schools)",
                             savepath="../code_output/fig_SOL_CS_no_outliers_panels.png")
SOL_CS_by_gender_no_outliers_stats  = _plot_panels(SOL_CS_by_gender_df_no_outliers,  hue="gender",    title_suffix=" (High Schools, by Gender)",
                             savepath="../code_output/fig_SOL_CS_by_gender_no_outliers_panels.png",
                             palette=GENDER_PALETTE,   # <- pink for F, blue for M palette=GENDER_PALETTE,   # <- pink for F, blue for M
                             )
SOL_CS_by_race_no_outliers_stats    = _plot_panels(SOL_CS_by_race_df_no_outliers,    hue="race",      title_suffix=" (High Schools, by Race)",
                             savepath="../code_output/fig_SOL_CS_by_race_no_outliers_panels.png")

