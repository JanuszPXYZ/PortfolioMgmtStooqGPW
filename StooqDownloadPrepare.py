import pandas as pd
from gazpacho import get, Soup
import re
import urllib


#url_query = "http://stooq.pl/q/d/"
#csv_download_query = "l/?s=mwig40&i=d"
#full_query = url_query + csv_download_query


def get_index_components(query: str):
    '''
    Returns components of an index that is specified for a given
    index (in the case of Polish Stock Exchange (GPW) that would be
    for example mWig40)

    '''
    htmlContents = []
    companies = []
    html = get(query)
    soup = Soup(html)

    data_table = soup.find('tbody')

    for i in data_table:
        if i.find('font') == None:
            continue
        htmlContents.append(i.find('font'))

    for element in htmlContents[0]:
        if element.find('a') == None:
            continue

        companies.append(re.findall(">(.*)</a>",str(element.find('a')))[0])

    return companies


def download_ticker_data(ticker: str, sep: str = ','):
    '''
    Returns a DataFrame for a specified ticker.
    '''
    ticker_url = f"https://stooq.pl/q/d/l/?s={ticker}&i=d"
    ticker_data = pd.DataFrame(pd.read_table(ticker_url, sep = sep))
    ticker_data.name = ticker
    ticker_data = ticker_data.set_index("Data")

    return ticker_data


def closing_prices_for_index_components(tickers: list):
    '''
    Returns a full dataset containing the closing prices for the companies within
    an index.
    '''
    companies_closing_price = []
    for company in tickers:
        companies_closing_price.append(download_ticker_data(company)['Zamkniecie'])

    full_df = pd.concat(companies_closing_price, axis = 1, sort = True)
    full_df.columns = tickers

    return full_df
