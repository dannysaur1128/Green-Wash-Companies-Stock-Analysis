import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

Fast_Food = ["MCD.csv", "ChipotleMG.csv"]
Food_Processing = ["NSRGY.csv","Pepsico.csv"]
Automotive = ["VOW3.DE.csv","Ford.csv"]
Retail = [ "WMT.csv","Target.csv"]
Oil_and_Gas = ["BP.csv", "Exxon.csv", "CVX.csv"]

scandal_dates = {
    "MCD.csv": pd.to_datetime("2022-04-21"),
    "VOW3.DE.csv": pd.to_datetime("2015-09-18"),
    "WMT.csv": pd.to_datetime("2019-06-20"),
    "BP.csv": pd.to_datetime("2010-04-20"),
    "NSRGY.csv": pd.to_datetime("2023-01-27")
    }

# Specify the path to your folder containing the files
folder_path = '/Users/sallypigott/library/CloudStorage/OneDrive-NortheasternUniversity/DS 2000/GROUP PROJECT/*.csv'



def read_files_to_dict(file_list):
   
    # Use glob to get a list of file paths matching a pattern (e.g., all CSV files)
    file_paths = glob.glob(folder_path)
   
    # Create an empty dictionary to store DataFrames
    dfs_dict = {}
   
    columns_to_keep = ["Date", "Adj Close"]
   
    # Loop through the file paths and read each file into a DataFrame
    for file_path in file_paths:
        # Extract the file name from the path
        file_name = os.path.basename(file_path)
       
        if file_name in file_list:
            df = pd.read_csv(file_path)
            df = df[columns_to_keep]
            df["Date"] = pd.to_datetime(df["Date"])
           
            # Store the DataFrame in the dictionary with the file name as the key
            dfs_dict[file_name] = df
   
    # Now, dfs_dict contains DataFrames from the specified files in the folder
    return dfs_dict


def plot_category(category_files, category_name):
  # Call the function to get the dictionary of DataFrames for the specified category
  result_dict = read_files_to_dict(category_files)
 
  # Plot the data from files in the category on the same graph
 
 
  for file_name, df in result_dict.items():
      if file_name in category_files:
          # Assume "Date" is the x-axis and "Adj Close" is the y-axis
          plt.plot(df["Date"], df["Adj Close"], label=file_name)
 
  plt.title(f"{category_name} Stocks - Adj Close Prices Over Time")
  plt.xlabel("Date")
  plt.ylabel("Adj Close")
  plt.legend()
  plt.show()
   
# Plot the Fast_Food category
plt.figure(figsize=(10, 6))
plot_category(Fast_Food, "Fast Food")
plot_category(Food_Processing, "Food Manufacter")
plot_category(Automotive, "Automotive")
plot_category(Retail, "Retail")
plot_category(Oil_and_Gas, "Oil and Gas")

plt.show()



#Using for loops we created two lists,
#one for before scandal(before_max) and one for after (after_max)
#We use this to find the closest stock price after the scandal
#with a corresponding date

def find_closest_price(after_prices, max_before_val):
    initial_price = after_prices[0]
    for p in after_prices:
        curr_closest_price = 0
        curr_closest_val = initial_price
        if abs(p - max_before_val) < curr_closest_val:
            curr_closest_val = abs(p - max_before_val)
            curr_closest_price = p

    return curr_closest_price


def calculate_days_difference(date1, date2):
    return (date2 - date1).days


def calculate_years_difference(date1, date2):
    days_difference = calculate_days_difference(date1, date2)
    return days_difference / 365.25  # Accounting for leap years


# Modify the plot_category function to include the new functionality
def print_category_info(category_files, category_name):
    # Call the function to get the dictionary of DataFrames for the specified category
    result_dict = read_files_to_dict(category_files)

    for file_name, df in result_dict.items():
        if file_name in category_files:
            if file_name == category_files[0]:  # Apply the scandal date code only for the first company in each category
                # Find the maximum value and date before the scandal
                max_before_date = df.loc[df["Date"] < scandal_dates[file_name]]["Date"].max()
                max_before_val = df.loc[df["Date"] == max_before_date, "Adj Close"].values[0]

                # Create a list of prices after the scandal
                after_max_list = df.loc[df["Date"] > scandal_dates[file_name], "Adj Close"].tolist()

                # Find the closest price after the scandal to the maximum before the scandal
                closest_after_price = find_closest_price(after_max_list, max_before_val)

                # Find the date corresponding to the closest price after the scandal
                closest_after_date = df.loc[df["Adj Close"] == closest_after_price, "Date"].values[0]

                # Calculate the number of years between the two dates
                years_difference = calculate_years_difference(max_before_date, closest_after_date)

                print(f"For {file_name} in {category_name}:")
                print(f"Maximum before scandal: {max_before_val} on {max_before_date}")
                print(f"Closest price after scandal: {closest_after_price} on {closest_after_date}")
                print(f"Time difference: {years_difference:.2f} years\n")

# Print information for each category
print_category_info(Fast_Food, "Fast Food")
print_category_info(Food_Processing, "Food Manufacturing")
print_category_info(Automotive, "Automotive")
print_category_info(Retail, "Retail")
print_category_info(Oil_and_Gas, "Oil and Gas")
