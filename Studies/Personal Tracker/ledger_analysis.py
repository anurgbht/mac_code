import sys
import arrow
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# 1 wine = 4 beers
WINETOBEER = 4

################################################################################################
################################################################################################
################################################################################################


def find_alco(tt):
    try:
        a, b = tt.split("-")
        if a == "Beer":
            return float(b)
        else:
            return float(b) * WINETOBEER
    except:
        return 0


def find_act(x):
    # return 1
    if "-" in x:
        return 0
    else:
        return len(x.split(","))


def find_gym(x):
    gym_equivalent = ["Gym", "10k", "150P", "S", "Kajak"]
    if any([any([t in s for t in gym_equivalent]) for s in x.split(",")]):
        return 1
    else:
        return 0


def make_date(x):
    # 2020-08-02 00:00:00
    if type(x) == str:
        return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    else:
        return x


def make_plotly(gpa, ppa, bqa, tt):
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(
        go.Scatter(x=tt, y=bqa, mode="lines+markers", name="Alcohol consumption"),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=tt, y=gpa, mode="lines+markers", name="Gym activity"), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=tt, y=ppa, mode="lines+markers", name="Physical activity"),
        row=2,
        col=1,
    )
    # Edit the layout
    fig.update_layout(
        title=f"Activity and Consumption tracker<br>Last updated: {arrow.get(tt[-1]).humanize()}",
        template="plotly_white",
    )
    fig.show()


################################################################################################
################################################################################################
################################################################################################


def main(NDAYS, ledger_path):

    data = pd.read_excel(ledger_path).dropna()

    data["datetime"] = data["Date"].apply(make_date)
    data["all activity"] = (
        100 * data["Physical Activity"].apply(find_act).rolling(NDAYS).sum() / NDAYS
    )
    data["gym activity"] = (
        100 * data["Physical Activity"].apply(find_gym).rolling(NDAYS).sum() / NDAYS
    )
    data["alcohol consumption"] = (
        7 * data["Alcohol"].apply(find_alco).rolling(NDAYS).sum() / NDAYS
    )

    make_plotly(
        list(data["gym activity"]),
        list(data["all activity"]),
        list(data["alcohol consumption"]),
        list(data["datetime"]),
    )


def test():
    main(10, Path(Path(__file__).parent, "TestLedger.xlsx"))


if __name__ == "__main__":
    user_days = int(sys.argv[1])
    main(user_days, Path(Path(__file__).parent, "DailyLedger.xlsx"))
    # test()
