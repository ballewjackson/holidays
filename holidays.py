import pandas as pd

def CheckHoliday(row):
    # first let's do all that are the fixed date
    # dec 31
    # jan 1
    # june 19 ???
    # july 4
    # nov 11
    # dec 24
    # dec 25
    fixedDates = ["01-01", "06-19", "07-04", "11-11", "12-24", "12-25", "12-31"]
    for date in fixedDates:
        if row["MMDD"] == date:
            if row["dayOfWeekName"] == "Saturday":
                return "previous_day"
            if row["dayOfWeekName"] == "Sunday":
                return "next_day"
            return "current_day"
    # variable dates
    # 3rd Monday of Jan
    # 3rd Monday of Feb
    # Last Monday of May
    # 1st monday of sept
    # 2nd monday of Oct
    # 4th thursday of nov
    conditions = (
        (row["MMDD"][:2] == "01" or row["MMDD"][:2] == "02" ) and row["dayOfWeekName"] == "Monday" and row["weekOfMonth"] == 3,
        row["MMDD"][:2] == "05" and row["dayOfWeekName"] == "Monday" and int(row["MMDD"][3:]) > 24,
        row["MMDD"][:2] == "09" and row["dayOfWeekName"] == "Monday" and row["weekOfMonth"] == 1,
        row["MMDD"][:2] == "10" and row["dayOfWeekName"] == "Monday" and row["weekOfMonth"] == 2,
        row["MMDD"][:2] == "11" and row["dayOfWeekName"] == "Thursday" and row["weekOfMonth"] == 4,
        row["MMDD"][:2] == "11" and row["dayOfWeekName"] == "Friday" and row["weekOfMonth"] == 4,
    )
    if any(conditions):
        return "current_day"
    # Need to check multiple days for Thanksgiving, Dec 31, Dec 24, Election Day, Easter Monday, Good Friday
    # I asked chelsea

    return ""
            

start_year = 2020
end_year = 2050

date_range = pd.date_range(start=f"{start_year}-01-01", end=f"{end_year}-12-31")
df = pd.DataFrame(date_range, columns=["Date"])
df["MMDD"] = df["Date"].dt.strftime('%m-%d')
df["weekOfMonth"] = df["Date"].apply(lambda d: (d.day-1) // 7 + 1)
# Monday = 0
df["dayOfWeekNumber"] = df["Date"].dt.dayofweek
df["dayOfWeekName"] = df["Date"].dt.day_name()

#df["holiday"] = df.apply(CheckHoliday, axis=1)

for index in range(len(df)):
    holidayStatus = CheckHoliday(df.iloc[index])
    match holidayStatus:
        case "previous_day":
            df.at[index-1, "holiday"] = True
        case "current_day":
            df.at[index, "holiday"] = True
        case "next_day":
            df.at[index+1, "holiday"] = True
        case "":
            df.at[index, "holiday"] = False
        case _:
            raise("Exemption in Match based on return of CheckHoliday()")

print(df)
df.to_csv(r"C:\Users\jballew\OneDrive - Digicorner\Documents\holidays\holidays.csv", sep=",", header=True, index=False)
