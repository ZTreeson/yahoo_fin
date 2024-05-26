import yahoo_fin.stock_info as si
import xlwings as xw

def fillup_StockInfo_formula(ws,latest_row,col,cur_row):
    col_cur_row=col+str(cur_row)
    formula = ws.range(col_cur_row).formula
    formula_range=col_cur_row+':'+col+str(latest_row)
    ws.range(formula_range).formula = formula

def update_StockInfo_sheet(ticker,start_date,ws):
    stock_framedata=si.get_data(ticker=ticker,start_date=start_date)
    # Update workbook at specified range
    ws.range("A1").options(index=True).value = stock_framedata
    rowa = ws.range('A1').end('down').row
    col_list = ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y']
    for x in col_list:
        start_row = x + '1'
        latest_row = ws.range(start_row).end('down').row
        fillup_StockInfo_formula(ws, rowa, x, latest_row)
#print(tsla,type(tsla))
#tsla.to_excel('/Users/treeson/Documents/Workbook1.xlsx',sheet_name='Sheet1',startrow=1,startcol=3)
#excel_book = pd.read_excel('/Users/treeson/Documents/Workbook1.xlsx')

app = xw.App(visible=False)
wb = xw.Book('/Users/treeson/Documents/Template.xlsx')
ws = wb.sheets['FDX']
update_StockInfo_sheet('tsla','2022-05-01',ws)

#sheet Charts
#ws_chart=wb.sheets['Charts']
#ws_chart['B26'].value='{=N(OFFSET(FDX!$Y$265,MATCH(LARGE(ABS(FDX!$Y$265:FDX!$Y$495),A28),ABS(FDX!$Y$265:FDX!$Y$495),0)-1,))}'

#=N(OFFSET(FDX!$Y$265,MATCH(LARGE(ABS(FDX!$Y$265:FDX!$Y$495),A26),ABS(FDX!$Y$265:FDX!$Y$495),0)-1,))
#=N(OFFSET(FDX!$Y$265,MATCH(LARGE(ABS(FDX!$Y$265:FDX!$Y$495),A26),ABS(FDX!$Y$265:FDX!$Y$495),0)-1,))
wb.save()
wb.close()
app.quit()