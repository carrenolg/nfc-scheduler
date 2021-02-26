from openpyxl import Workbook
from openpyxl.styles import NamedStyle
from openpyxl.styles import Font, Color, Alignment, Border, Side, colors
import datetime


def create(data):
    workbook = Workbook()
    sheet = workbook.active
    file_name = 'utils/tugs_scheduler.xlsx'

    # setting
    sheet.title = "scheduler"
    sheet["A1"] = "ID"
    sheet["B1"] = "REMOLCADOR"
    sheet["C1"] = "ACTUAL"
    sheet["D1"] = "PRÓXIMA"
    sheet["E1"] = "TIPO"
    # Let's create a style template for the header row
    header = NamedStyle(name="header")
    header.font = Font(bold=True)
    header.border = Border(bottom=Side(border_style="thin"))
    header.alignment = Alignment(horizontal="center", vertical="center")
    header_row = sheet[1]
    for cell in header_row:
        cell.style = header

    # put data into the file
    for item in data:
        sheet.append(item)

    # validate date (coming date <= today date)
    # whether validation is TRUE, add RED color to date
    big_red_text = Font(color=colors.BLUE)
    for i in sheet["D"][1:]:
        if i.value <= datetime.date.today():
            i.font = big_red_text
        i.value = i.value.strftime("%d/%m/%Y")

    # save data into the file
    workbook.save(filename=file_name)
