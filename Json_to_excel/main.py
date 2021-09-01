 
import requests
import pandas as pd


def main():
    url = 'https://606f76d385c3f0001746e93d.mockapi.io/api/v1/auditlog'
    req = requests.get(url)
    d_frame = pd.DataFrame(req.json())
    d_frame.to_excel('test.xlsx', sheet_name='Sheet1')


if __name__ == '__main__':
    main()
