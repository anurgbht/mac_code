import io
import pandas as pd
import msoffcrypto

passwd = '5Rq32))&'
person = "Anurag"

sheet_lookup = {
    "Anurag": ['Records-INR', 'Records-EUR', 'Records-GBP', 'Records-CZK'],
    "Aditi": ['Records-INR', 'Records-CZK']
}

path_to_your_file = f'/home/anurag/Documents/Financials/financial statement - {person}.xlsx'

decrypted_workbook = io.BytesIO()
with open(path_to_your_file, 'rb') as file:
    office_file = msoffcrypto.OfficeFile(file)
    office_file.load_key(password=passwd)
    office_file.decrypt(decrypted_workbook)

for sheet_name in sheet_lookup[person]:
    print(f"Processing {sheet_name}")
    df = pd.read_excel(decrypted_workbook, sheet_name=sheet_name)
    df.to_parquet(f'/home/anurag/Documents/Financials/Records-INR-{person}.parquet')