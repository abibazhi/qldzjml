import requests
from bs4 import BeautifulSoup


def extract_table_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    new_table = soup.new_tag('table')
    headers = ['部名', '经名']
    header_row = soup.new_tag('tr')
    for header in headers:
        th = soup.new_tag('th')
        th.string = header
        header_row.append(th)
    new_table.append(header_row)

    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        i = 0
        while i < len(rows):
            row = rows[i]
            cols = row.find_all('td')
            if len(cols) >= 3:
                part_name = cols[0].get_text(strip=True)
                scripture_name = cols[2].get_text(strip=True)
                new_row = soup.new_tag('tr')
                td1 = soup.new_tag('td')
                td1.string = part_name
                new_row.append(td1)
                td2 = soup.new_tag('td')
                td2.string = scripture_name
                new_row.append(td2)
                new_table.append(new_row)
                i += 1
                while i < len(rows) and len(rows[i].find_all('td')) >= 3 and rows[i].find_all('td')[0].get_text(
                        strip=True) == part_name:
                    i += 1
            else:
                i += 1

    return new_table


def save_to_html(table, output_path):
    html_content = f'<!DOCTYPE html><html><body>{table.prettify()}</body></html>'
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


if __name__ == '__main__':
    url = 'http://www.qldzj.com/html/qldzj-ml.htm'
    result_table = extract_table_data(url)
    save_to_html(result_table, 'extracted_table.html')

