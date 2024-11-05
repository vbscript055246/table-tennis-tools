from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class Product:
    def __init__(self, name, price, url, _type):
        self.name = name
        self.price = price
        self.url = url
        self.type = _type
        self.Speed = -1
        self.Spin = -1          # rubber, pips
        self.Control = -1
        self.Deception = -1     # pips
        self.Reversal = -1      # pips
        self.Tackiness = -1     # rubber
        self.Weight = -1        # rubber, pips
        self.Sitffness = -1     # blade
        self.Hardness = -1
        self.Gears = -1         # rubber
        self.Angle = -1         # rubber
        self.Consistency = -1
        self.Durability = -1    # rubber, pips

    def get_data(self):
        if self.type == 'blade':
            return {
                'Name': self.name,
                'Speed': self.Speed,
                'Control': self.Control,
                'Sitffness': self.Sitffness,
                'Hardness': self.Hardness,
                'Price': self.price
            }
        elif self.type == 'rubber':
            return {
                'Name': self.name,
                'Speed': self.Speed,
                'Spin': self.Spin,
                'Control': self.Control,
                'Tackiness': self.Tackiness,
                'Weight': self.Weight,
                'Hardness': self.Hardness,
                'Gears': self.Gears,
                'Angle': self.Angle,
                'Durability': self.Durability,
                'Price': self.price
            }
        elif self.type == 'pips':
            return {
                'Name': self.name,
                'Speed': self.Speed,
                'Spin': self.Spin,
                'Control': self.Control,
                'Deception': self.Deception,
                'Reversal': self.Reversal,
                'Weight': self.Weight,
                'Hardness': self.Hardness,
                'Durability': self.Durability,
                'Price': self.price
            }
        else:
            exit(87)


class Comparator:
    def __init__(self, _df, _type, mode=0):
        self.df = _df
        self.type = _type
        self.mode = mode

    def apply_mask(self):
        if self.type == 'blade':
            mask = (
                (self.df['Speed'] == -1) |
                (self.df['Control'] == -1) |
                (self.df['Sitffness'] == -1) |
                (self.df['Hardness'] == -1)
            )
        elif self.type == 'rubber':
            mask = (
                    (self.df['Speed'] == -1) |
                    (self.df['Spin'] == -1) |
                    (self.df['Control'] == -1) |
                    (self.df['Tackiness'] == -1) |
                    (self.df['Hardness'] == -1) |
                    (self.df['Gears'] == -1) |
                    (self.df['Angle'] == -1)
            )
        elif self.type == 'pips':
            mask = (
                (self.df['Speed'] == -1) |
                (self.df['Spin'] == -1) |
                (self.df['Control'] == -1) |
                (self.df['Deception'] == -1) |
                (self.df['Reversal'] == -1) |
                (self.df['Hardness'] == -1)
            )
        # print(f'Total: {len(self.df)}, Removed: {len(self.df[mask])}')
        self.df = self.df[~mask]

    def caluclate_STD(self, product_name):
        select_item = self.df[(self.df['Name'] == product_name)]
        if len(select_item) != 1:
            print('Name error')
            exit(87)
        else:
            if self.type == 'blade':
                Speed = float(select_item['Speed'])
                Control = float(select_item['Control'])
                Sitffness = float(select_item['Sitffness'])
                Hardness = float(select_item['Hardness'])
                self.df['Speed Var'] = (self.df['Speed'] - Speed) ** 2
                self.df['Control Var'] = (self.df['Control'] - Control) ** 2
                self.df['Sitffness Var'] = (self.df['Sitffness'] - Sitffness) ** 2
                self.df['Hardness Var'] = (self.df['Hardness'] - Hardness) ** 2

                if self.mode:
                    # Calculate Customized Weighting STD
                    self.df['Total Std'] = (
                        (
                           self.df['Speed Var'] * 0.3+
                           self.df['Control Var'] * 0.5+
                           self.df['Sitffness Var'] * 0.1+
                           self.df['Hardness Var'] * 0.1
                        )
                    ) ** 0.5

                    # Apply Customized MASK
                    # mask = (self.df['Control'] >= Control)
                    # self.df = self.df[mask]
                else:
                    self.df['Total Std'] = (
                        (
                            self.df['Speed Var'] +
                            self.df['Control Var'] +
                            self.df['Sitffness Var'] +
                            self.df['Hardness Var']
                        ) / 4
                    ) ** 0.5

            elif self.type == 'rubber':
                Speed = float(select_item['Speed'])
                Spin = float(select_item['Spin'])
                Control = float(select_item['Control'])
                Tackiness = float(select_item['Tackiness'])
                Hardness = float(select_item['Hardness'])
                Gears = float(select_item['Gears'])
                Angle = float(select_item['Angle'])

                self.df['Speed Var'] = (self.df['Speed'] - Speed) ** 2
                self.df['Spin Var'] = (self.df['Spin'] - Spin) ** 2
                self.df['Control Var'] = (self.df['Control'] - Control) ** 2
                self.df['Tackiness Var'] = (self.df['Tackiness'] - Tackiness) ** 2
                self.df['Hardness Var'] = (self.df['Hardness'] - Hardness) ** 2
                self.df['Gears Var'] = (self.df['Gears'] - Gears) ** 2
                self.df['Angle Var'] = (self.df['Angle'] - Angle) ** 2

                if self.mode:
                    # Calculate Customized Weighting STD
                    self.df['Total Std'] = (
                        (
                            self.df['Speed Var'] +
                            self.df['Spin Var'] +
                            self.df['Control Var'] +
                            self.df['Tackiness Var'] +
                            self.df['Hardness Var'] +
                            self.df['Angle Var']
                        ) / 6
                    ) ** 0.5

                    # Apply Customized MASK
                    mask = (self.df['Speed'] <= Speed)
                    self.df = self.df[mask]
                else:
                    self.df['Total Std'] = (
                        (
                            self.df['Speed Var'] +
                            self.df['Spin Var'] +
                            self.df['Control Var'] +
                            self.df['Tackiness Var'] +
                            self.df['Hardness Var'] +
                            self.df['Gears Var'] +
                            self.df['Angle Var']
                        ) / 7
                    ) ** 0.5

            elif self.type == 'pips':
                Speed = float(select_item['Speed'])
                Spin = float(select_item['Spin'])
                Control = float(select_item['Control'])
                Deception = float(select_item['Deception'])
                Reversal = float(select_item['Reversal'])
                Hardness = float(select_item['Hardness'])

                self.df['Speed Var'] = (self.df['Speed'] - Speed) ** 2
                self.df['Spin Var'] = (self.df['Spin'] - Spin) ** 2
                self.df['Control Var'] = (self.df['Control'] - Control) ** 2
                self.df['Deception Var'] = (self.df['Deception'] - Deception) ** 2
                self.df['Reversal Var'] = (self.df['Reversal'] - Reversal) ** 2
                self.df['Hardness Var'] = (self.df['Hardness'] - Hardness) ** 2

                if self.mode:
                    # Calculate Customized Weighting STD
                    self.df['Total Std'] = (
                       (
                           self.df['Speed Var'] +
                           self.df['Spin Var'] +
                           self.df['Control Var'] +
                           self.df['Deception Var']
                       ) / 4
                    ) ** 0.5
                else:
                    self.df['Total Std'] = (
                        (
                            self.df['Speed Var'] +
                            self.df['Spin Var'] +
                            self.df['Control Var'] +
                            self.df['Deception Var'] +
                            self.df['Reversal Var'] +
                            self.df['Hardness Var']
                        ) / 6
                    ) ** 0.5

            self.df['Total Std'] = round(self.df['Total Std'], 4)
            return self.df.sort_values('Total Std')

    def customized_STD(self, product_name, option):

        select_item = self.df[(self.df['Name'] == product_name)]

        column_set = []
        if self.type == 'blade':
            column_set = ['Speed', 'Control', 'Sitffness', 'Hardness']
        elif self.type == 'rubber':
            column_set = ['Speed', 'Spin', 'Control', 'Tackiness', 'Hardness', 'Gears', 'Angle']
        elif self.type == 'pips':
            column_set = ['Speed', 'Spin', 'Control', 'Deception', 'Reversal', 'Hardness']

        flag = sum([int(option.get(f'{self.type}_{col.lower()}') == '4') for col in column_set])

        for col in column_set:
            if option.get(f'{self.type}_{col.lower()}') == '1':
                mask = (self.df[col] >= float(select_item[col]))
                self.df = self.df[mask]
            elif option.get(f'{self.type}_{col.lower()}') == '2':
                mask = (self.df[col] == float(select_item[col]))
                self.df = self.df[mask]
            elif option.get(f'{self.type}_{col.lower()}') == '3':
                mask = (self.df[col] <= float(select_item[col]))
                self.df = self.df[mask]

            self.df[f'{col} Var'] = (self.df[col] - float(select_item[col])) ** 2 if (option.get(f'{self.type}_{col.lower()}') == '4' or ~flag) else 0
        # TODO implement none selection
        self.df['Total Std'] = (
            (
                sum([self.df[f'{col} Var'] for col in column_set])
            ) / (
                flag if flag else len(column_set)
            )
        ) ** 0.5

        self.df['Total Std'] = round(self.df['Total Std'], 4)
        return self.df.sort_values('Total Std')


class Modifier:
    def __init__(self, type_name):
        self.type = type_name

    def do(self, df):
        if self.type == 'blade':
            df = df[
                [
                    'Name',
                    'Speed',
                    'Control',
                    'Sitffness',
                    'Hardness',
                    'Total Std',
                    'Price'
                ]
            ]
        elif self.type == 'rubber':
            df = df[
                [
                    'Name',
                    'Speed',
                    'Spin',
                    'Control',
                    'Tackiness',
                    'Hardness',
                    'Gears',
                    'Angle',
                    'Total Std',
                    'Price',
                    'Durability'
                ]
            ]
        elif self.type == 'pips':
            df = df[
                [
                    'Name',
                    'Speed',
                    'Spin',
                    'Control',
                    'Deception',
                    'Reversal',
                    'Hardness',
                    'Total Std',
                    'Price',
                    'Durability'
                ]
            ]

        if 'Durability' in df.columns:
            df['Durability'] = df['Durability'].replace(-1, 'Unknown')
        df['Price'] = df['Price'].str.replace('$', '').replace('-', 'Unknown')
        return df


def SimpleWorker(item_obj):
    def get_direct_text(element):
        tmp = next(element.stripped_strings, '').strip()
        if tmp == '(not rated)':
            return -1
        else:
            return tmp

    while True:
        res = requests.get(
            item_obj.url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
            }
        )
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            table = soup.find('table', {'id': 'UserRatingsTable'})
            tr_elements = table.find_all('tr')
            if item_obj.type == 'blade':
                item_obj.Speed = float(tr_elements[0].find_all('td')[1].text.strip())
                item_obj.Control = float(tr_elements[1].find_all('td')[1].text.strip())
                item_obj.Sitffness = float(get_direct_text(tr_elements[2].find_all('td')[1]))
                item_obj.Hardness = float(get_direct_text(tr_elements[3].find_all('td')[1]))
                item_obj.Consistency = float(get_direct_text(tr_elements[4].find_all('td')[1]))

            elif item_obj.type == 'rubber':
                item_obj.Speed = float(tr_elements[0].find_all('td')[1].text.strip())
                item_obj.Spin = float(tr_elements[1].find_all('td')[1].text.strip())
                item_obj.Control = float(tr_elements[2].find_all('td')[1].text.strip())

                item_obj.Tackiness = float(get_direct_text(tr_elements[3].find_all('td')[1]))
                item_obj.Weight = float(get_direct_text(tr_elements[4].find_all('td')[1]))
                item_obj.Hardness = float(get_direct_text(tr_elements[5].find_all('td')[1]))
                item_obj.Gears = float(get_direct_text(tr_elements[6].find_all('td')[1]))
                item_obj.Angle = float(get_direct_text(tr_elements[7].find_all('td')[1]))
                item_obj.Consistency = float(get_direct_text(tr_elements[8].find_all('td')[1]))
                item_obj.Durability = float(get_direct_text(tr_elements[9].find_all('td')[1]))

            elif item_obj.type == 'pips':
                item_obj.Speed = float(tr_elements[0].find_all('td')[1].text.strip())
                item_obj.Spin = float(tr_elements[1].find_all('td')[1].text.strip())

                item_obj.Control = float(get_direct_text(tr_elements[2].find_all('td')[1]))
                item_obj.Deception = float(get_direct_text(tr_elements[3].find_all('td')[1]))
                item_obj.Reversal = float(get_direct_text(tr_elements[4].find_all('td')[1]))
                item_obj.Weight = float(get_direct_text(tr_elements[5].find_all('td')[1]))
                item_obj.Hardness = float(get_direct_text(tr_elements[6].find_all('td')[1]))
                item_obj.Consistency = float(get_direct_text(tr_elements[7].find_all('td')[1]))
                item_obj.Durability = float(get_direct_text(tr_elements[8].find_all('td')[1]))

            break
        else:
            time.sleep(1)


def GetNewData(page_name, force=False):
    from tqdm import tqdm
    import os
    if os.path.exists(f'{page_name}_full_data.xlsx') and not force:
        return

    print("Start Getting Data...")
    base_url = 'https://revspin.net/'
    response = requests.get(base_url + page_name, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
    })

    st = time.process_time()
    soup = BeautifulSoup(response.text, 'html.parser')
    table_elements = soup.find_all('table', {'class': 'specscompare'})

    items = []
    for table in table_elements:
        tr_elements = table.find_all('tr')[1:]

        for tr in tr_elements:
            td_elements = tr.find_all('td')
            if td_elements[1].text.strip() != '-' and td_elements[2].text.strip() != '-' and td_elements[3] != '-':
                items.append(
                    Product(
                        td_elements[0].text.strip(),
                        td_elements[5].text.strip(),
                        base_url + td_elements[0].a['href'],
                        page_name
                    )
                )

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(
            tqdm(
                executor.map(
                    SimpleWorker,
                    items
                ),
                total=len(items),
                desc='Getting Data'
            )
        )

    df = pd.DataFrame([item.get_data() for item in items])
    df.to_excel(f'{page_name}_full_data.xlsx', index=False)
    print(f'[{datetime.now().strftime("%H:%M:%S")}]: Done, Exec time: {time.process_time() - st:<4.2f} Seconds')


if __name__ == '__main__':
    type_name = 'rubber'
    GetNewData(type_name, force=False)
    df = pd.read_excel(f'{type_name}_full_data.xlsx', sheet_name='Sheet1')
    st = time.process_time()
    # Change mode to 1, using customized weighting STD
    comparator = Comparator(df, type_name, mode=0)
    comparator.apply_mask()

    # Product name must be same on revspin website
    df = comparator.caluclate_STD(
        product_name='DHS Hurricane 3 National (Blue Sponge)'
    )
    # FileSaver(type_name).save(df)
    print(f'[{datetime.now().strftime("%H:%M:%S")}] Exec time: {time.process_time()-st:<4.2f} Seconds')
    exit(0)