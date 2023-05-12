import csv
import datetime

# Dictionary defining 1 month minimum values by crew position
one_month_dict = {
  "KAN": 2,
  "KAE": 1,
  "EAN": 2,
  "EAE": 1,
  "PAE": 2,
  "PAN": 3,
  "CAE": 2,
  "CAN": 3,
  "NAE": 2,
  "NAN": 3,
  "EBE": 1,
  "PBE": 1,
  "KBE": 1,
  "ISS": 10, #Folks missing their crew codes should stand out...
  "PIN": 0
}

# Dictionary defining 3 month minimum values by crew position
three_month_dict = {
  "KAN": 5,
  "KAE": 3,
  "EAN": 5,
  "EAE": 3,
  "PAE": 5,
  "PAN": 8,
  "CAE": 5,
  "CAN": 8,
  "NAE": 5,
  "NAN": 8,
  "EBE": 3,
  "PBE": 2,
  "KBE": 2,
  "ISS": 30, #Folks missing their crew codes should stand out...
  "PIN": 0,
}

# Setting month numbers based on Federal fiscal year.
month_nums = {
  "October":1,
  "November":2,
  "December":3,
  "January":4,
  "February":5,
  "March":6,
  "April":7,
  "May":8,
  "June":9,
  "July":10,
  "August":11,
  "September":12
}

# Date handling 
today = datetime.date.today()
first_day_of_this_month = datetime.date(today.year, today.month, 1)
last_day_of_previous_month = first_day_of_this_month - datetime.timedelta(days=1)
previous_month = last_day_of_previous_month.strftime('%B')

# NOTE: Someone is on probation if they have failed their one and three month. If the member fails again, then they are on regression.

def one_month_lookback(flight_counts:str, crew_code:str) -> str:
  '''
  
  This function determines whether or not someone has met their one-month lookback (if they have flow the correct number of times in 1 month.)
  
  Args: 
  - flight_counts: a list of integers indicating the number of flights flown each month-to-date.
  - crew_code: a string representing a crew members crew code.  
  
  Returns:
  - A string indicating whether a member has pass or failed their one-month lookback, or that there was an error computing the one-month lookback.
  
  '''
  if crew_code in one_month_dict:
    flights_required = one_month_dict[crew_code]
    month_number = month_nums[previous_month] - 1 # Element numbers start with 0, so set the month # back 1...
    flights_flown = int(flight_counts[month_number]) # Process row list with the flight counts using the month #.
    if flights_flown < flights_required: # If the flights flown is less than the flights required...
      return "FAIL"
    elif flights_flown >= flights_required:
      return "PASS"
    else:
      return "ERROR"


def three_month_lookback(flight_counts:list[int], crew_code:str) -> str:
  '''
  
  This function is designed to determine whether someone has met their three-month lookback (the number of flights required in a 3-month period).
  
  Args:
  - flight_counts: a list of integers indicating the number of flights flown each month-to-date.
  - crew_code: a string representing the member's crew code, which is used to determine the number of times they need to fly within a three-month period.
  
  Returns:
  - A string indicating whether someone has or has not met their three-month looback (PASS/FAIL), or if there was an error computing the three-month lookback result. 
  
  '''
  if crew_code in three_month_dict:
    flights_required = three_month_dict[crew_code]
    month1 = month_nums[previous_month] - 1
    month2 = month_nums[previous_month] - 2
    month3 = month_nums[previous_month] - 3
    flights_flown_month1 = int(flight_counts[month1])
    flights_flown_month2 = int(flight_counts[month2])
    flights_flown_month3 = int(flight_counts[month3])
    flights_flown_sum = flights_flown_month1 + flights_flown_month2 + flights_flown_month3
    if flights_flown_sum < flights_required:
      return "FAIL"
    elif flights_flown_sum >= flights_required:
      return "PASS"
    else:
      return "ERROR"


def probation(flight_counts:list[int], crew_code:str) -> str:
  
  '''
  
  This function determines if someone is on "probation," or has failed both their one-month and three-month lookback for one-month.
  
  Args:
  - flight_counts: a list of integers indicating the number of flights flown each month-to-date.
  - crew_code: a string representing the member's crew code, which is used to determine the number of times they need to fly within a three-month period.
  
  Returns:
  - A string indicating whether that person is on probation (yes/no), or if there was an error computing the result. 
  
  '''
  
  # Check and set one_month_status
  if one_month_lookback(flight_counts, crew_code) == "PASS":
    one_month_status = "PASS"
  elif one_month_lookback(flight_counts, crew_code) == "FAIL":
    one_month_status = "FAIL"
  else:
    one_month_status = "ERROR"
    
  # Check and set three_month_status
  if three_month_lookback(flight_counts, crew_code) == "PASS":
    three_month_status = "PASS"
  elif three_month_lookback(flight_counts, crew_code) == "FAIL":
    three_month_status = "FAIL"
  else:
    three_month_status = "ERROR"
    
  # Primary logic, check if both one-month_status and three_month_status are FAIL
  if one_month_status and three_month_status == "FAIL":
    probation_status = "YES"
    return probation_status
  else:
    probation_status = "NO"
    return probation_status

# TODO: (NOT RELATED TO FINAL PROJECT, THIS IS A PRODUCTION EDIT) Add a remove_from_probation function.

# TODO: (NOT RELATED TO FINAL PROJECT, THIS IS A PRODUCTION EDIT) Add a remove_from_regression function.

def regression(flight_counts, crew_code) -> str:
  
  '''
  
  This function determines whether or not someone is on regression (failing their one-month and three-month lookback 2 months in a row), and returns the result.
  
  Args:
  - flight_counts: a list of integers indicating the number of flights flown each month-to-date.
  - crew_code: a string representing the member's crew code, which is used to determine the number of times they need to fly within a three-month period.
  
  Returns:
  - A string indicating whether or not someone is on regression (YES/NO), or if there was an error caluclating the result.
  
  '''
  
  if one_month_lookback(flight_counts,crew_code) and three_month_lookback(flight_counts,crew_code) == "FAIL":
    flights_required = three_month_dict[crew_code]
    prev_month1 = month_nums[previous_month] - 2 
    prev_month2 = month_nums[previous_month] - 3
    prev_month3 = month_nums[previous_month] - 4
    month1_flights = int(flight_counts[prev_month1])
    month2_flights = int(flight_counts[prev_month2])
    month3_flights = int(flight_counts[prev_month3])
    sum = month1_flights + month2_flights + month3_flights
    if sum < flights_required:
      return "YES"
    else:
      return "NO"
  else:
    return "NO"    

def main() -> None:
  
  '''
  
  This is the main function, it contains a simple number based menu currently populated with the programs only option, to run the EOM (End of Month) RAP report.
  
  The EOM RAP report logic accepts as its input a csv file. This csv file contains all flight data from the begining of the fiscal year to the previous month for each crew member.
  
  Based on these numbers, each member is checked against the one_month_lookback, three_month_lookback, probation, and regression functions.
  
  Args:
  - flight_counts: the list of the number of flights that the member has flown by month-to-date of the fiscal year as extracted from the CSV file.
  - crew_code: the members crew code as extracted from the CSV file.
  - one_month_dict: A distionary of one-month minimum flight numbers by crew position.
  - three_month_dict: A dictionary of three-month minimum flight numbers by crew position.
  - month_nums: A dictionary of month names and their corresponding position in the fiscal year.
  
  Outputs:
  - Raw output from print statements executed on every row starting at the third row (skipping the CSV headers).
  - one_month_list: A list of members failing their one-month lookback by name.
  - three_month_list: A list of members failing their three-month lookback by name.
  - regression_list: A list of members on regression by name.
  - probation_list: A list of members on probation by name.
  - missing_list: A list of members with MISSING as their crew code. 
  
  Returns: None
  
  '''
  
  print("1: Run EOM RAP Report")
  selection = int(input("Select an operation: "))
  while selection in [1, 2, 3, 4]:
    if selection == 1:
      print(f"Running EOM RAP Report for {previous_month}")
      try: # TODO: (NOT RELATED TO FINAL PROJECT, THIS IS A PRODUCTION EDIT) This need to be moved to a separate function. 
        input_file: str = input("Enter input file name (.csv): ")
        with open(input_file, 'r') as csvfile: #Open input file.Open inp
          reader = csv.reader(csvfile) #Generate csv read file.
          i = 0

          ### INITIALIZE LISTS ###

          one_month_list: list[str] = []
          three_month_list: list[str] = []
          regresssion_list: list[str] = []
          probation_list: list[str] = []
          missing_list: list[str]= []

          # Iterate through the CSV file and start processing lines...
          for row in reader:
            i += 1
            if i >= 3: # Skip the headers in the CSV file.
              
              name: str = row[0]
              
              # Extract crew code from the first element of the row
              crew_code: str = row[1][1:4]
              full_crew_code: str = row[1]
              
              # Extract flight counts for each month starting from October (the start of the fiscal year)
              flight_counts: list[str] = row[2:14]

              ### OUTPUT LIST HANDLING ###

              # If the person has failed their 1-month lookback, append them to the 1-month lookback list.
              if one_month_lookback(flight_counts,crew_code) == "FAIL": 
                one_month_list.append(name)

              # If the person has failed their 3-month, append their name to the 3-month list.
              if three_month_lookback(flight_counts,crew_code) == "FAIL": 
                three_month_list.append(name)

              # If the person is on probation, add them to the list.
              if probation(flight_counts,crew_code) == "YES": 
                probation_list.append(name)
                if name in one_month_list:
                  one_month_list.remove(name)

              # If the person is on regression, add them to the list. 
              if regression(flight_counts,crew_code) == "YES": 
                regresssion_list.append(name)
                if name in probation_list:
                  probation_list.remove(name)
                if name in one_month_list:
                  one_month_list.remove(name)
              
              if crew_code == "MISSING":
                missing_list.append(name)

              # Output the raw calculations
              print(f"{i - 2} Name: {name}, Code: {full_crew_code}, 1-Month: {one_month_lookback(flight_counts,crew_code)}, 3-Month: {three_month_lookback(flight_counts, crew_code)}, Probation: {probation(flight_counts, crew_code)}, Regression: {regression(flight_counts, crew_code)}")
          
          # Print the total number of members...
          print("\n")
          print(f"Total Members: {i - 2}")
          print("\n")
          #total_members = i - 2 # Assign total members to variable for later graphing functions...


          # Check if each list is populated and print the respective names.
          # Check if the one-month list is populated, if so, print each name. 
          if len(one_month_list) > 0:
            print("One Month Failures:\n")
            for e in one_month_list:
              print(e)

          # Check if the probation list is populated, if so, print each name. 
          if len(probation_list) > 0:
            print("\n")
            print("Probation List:\n")
            for e in probation_list:
              print(e)

          # Check if the regression list is populated, if so, print each name. 
          if len(regresssion_list) > 0: 
            print("\n")
            print("Regression List:\n")
            for e in regresssion_list:
              print(e)

          # Check if the missing list is populated, if so, print each name.
          if len(missing_list) > 0:
            print("\n")
            print("Missing List: ")
            for e in missing_list:
              print(name)
            print("\n")
          else:
            print("\n")

      # Exception handling...
      except FileNotFoundError:
        print("File not found. Please check the file name and try again...")
      except Exception as e:
        print(f"An error occurred: {e}. Please check the file format and try again...")
      break
    
    ### END EXPORT ###
    else:
      print("Please enter a valid selection: [1,2,3,4]")
      break