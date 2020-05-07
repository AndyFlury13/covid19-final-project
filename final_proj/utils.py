def get_day_cases(end_date=date.today()):
    """
    Gets day-by-day case numbers.

    Input: end date (optional)
    Output: array of dataframes, indexed from 0 = 4/12/20
    """
    START_DATE = date(2020, 4, 12)
    GIT_REPO_PATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
    num_days = (end_date - START_DATE).days
    dfs = []
    for i in range(num_days):
        print(i)
        year, mo, day = (START_DATE + timedelta(days=i)).isoformat().split('-')
        file_name = '{0}-{1}-{2}.csv'.format(mo, day, year)
        dfs.append(pd.read_csv(GIT_REPO_PATH + file_name, error_bad_lines=False))
    return dfs
