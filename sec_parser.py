from bs4 import BeautifulSoup

def parse_form4_txt(txt_content):
    soup = BeautifulSoup(txt_content, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        if "nonDerivativeTable" in str(table):
            return True
    return False
