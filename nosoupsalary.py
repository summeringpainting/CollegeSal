import pandas as pd

# URL to get table from
URL = ("https://www.payscale.com/college-salary-report"
       "/majors-that-pay-you-back/bachelors")


def scraper(URL):
    '''scrapes salary data'''
    dfs = pd.read_html(URL)
    df = dfs[0]

    # make copy to keep appending during iteration
    df = df.copy()
    df.columns = ["Rank",
                  "Major",
                  "Type",
                  "EarlyCareerPay",
                  "MidCareerPay",
                  "HighMeaning"]

    # append DataFrames made from tables of all pages
    for i in range(2, 35):
        URL = ("https://www.payscale.com/college-salary-report/"
               f"majors-that-pay-you-back/bachelors/page/{i}")

        orig_table = pd.read_html(URL)
        page_df = orig_table[0].copy()
        page_df.columns = ["Rank",
                           "Major",
                           "Type",
                           "EarlyCareerPay",
                           "MidCareerPay",
                           "HighMeaning"]

        df = df.append(page_df,
                       ignore_index=True)

    # Get only columns we need
    df = df[["Major",
             "EarlyCareerPay",
             "MidCareerPay"]]

    # debloat some of the strings
    df.replace({"^Major:": "",
                "^Early Career Pay:\$": "",
                "^Mid-Career Pay:\$": "",
                ",": ""},
               regex=True,
               inplace=True)

    # convert strings to numbers
    df[["EarlyCareerPay",
        "MidCareerPay"]] = df[["EarlyCareerPay",
                               "MidCareerPay"]].apply(pd.to_numeric)

    return df


df = scraper(URL)

print(df)
df.to_csv('collegesals.csv')
