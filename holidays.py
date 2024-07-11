import pandas as pd
import math

def gaussEaster(Y):
    A = Y % 19
    B = Y % 4
    C = Y % 7
    P = math.floor(Y / 100)
    Q = math.floor((13 + 8 * P) / 25)
    M = (15 - Q + P - P // 4) % 30
    N = (4 + P - P // 4) % 7
    D = (19 * A + M) % 30
    E = (2 * B + 4 * C + 6 * D + N) % 7
    days = (22 + D + E)
    if ((D == 29) and (E == 6)):
        return f"{Y}-04-19"
    elif ((D == 28) and (E == 6)):
        return f"{Y,}-04-18"
    else:
        if (days > 31):
            return f"{Y}-04-{days - 31}"
        else:
            return f"{Y}-03-{days}"

def CheckHoliday(row):
    """
    Returns a string : {"easter", "previous_day", "current_day", "next_day"} based on whether the date of the input row is a Holiday
    """
    if row["dayOfWeekName"] == "Sunday" and (row["MMDD"][:2] == "03" or row["MMDD"][:2] == "04") and gaussEaster(int(row["Date"].strftime('%Y-%m-%d')[:4])) == row["Date"].strftime('%Y-%m-%d'):
        return "easter"
    fixedDates = ["01-01", "07-04", "12-24", "12-25"]
    for date in fixedDates:
        if row["MMDD"] == date:
            if row["dayOfWeekName"] == "Saturday":
                return "previous_day"
            if row["dayOfWeekName"] == "Sunday":
                return "next_day"
            return "current_day"
    conditions = (
        row["MMDD"][:2] == "05" and row["dayOfWeekName"] == "Monday" and int(row["MMDD"][3:]) > 24,
        row["MMDD"][:2] == "09" and row["dayOfWeekName"] == "Monday" and row["weekOfMonth"] == 1,
        row["MMDD"][:2] == "11" and row["dayOfWeekName"] == "Thursday" and row["weekOfMonth"] == 4,
        row["MMDD"][:2] == "11" and row["dayOfWeekName"] == "Friday" and row["weekOfMonth"] == 4,
    )
    if any(conditions):
        return "current_day"
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
        case "easter":
            df.at[index-2, "holiday"] = True
            df.at[index, "holiday"] = True
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

df.to_csv(r"C:\Users\jballew\OneDrive - Digicorner\Documents\holidays\holidays.csv", sep=",", header=True, index=False)
