import TradingList as tlist
import CommonEnum as cenum
import xlsxwriter 

trade_list = tlist.gettradinglist(cenum.ExportFrom.JSON)

with xlsxwriter.Workbook('TradingList.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(trade_list):
        colnum = 0
        if row_num == 0:
            worksheet.write_row(row_num, 0, data)

        for item in data:
            worksheet.write(row_num+1, colnum, data[item])
            colnum = colnum + 1

print("**************Final*****************")



