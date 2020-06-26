import os
import csv

# app.py
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

months = ['January', 'February' , 'March', 'April' , 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def writeToCSV(filename, updatedDate, invoiceNumber, vendorName, item,
               GSTNumber, salePurchase, basicAmount, IGSTRate, IGSTAmount,
               CGSTRate, CGSTAmount, SGSTRate, SGSTAmount, TotalAmount):
    newRow = [updatedDate,
              invoiceNumber,
              vendorName,
              item,
              GSTNumber,
              salePurchase,
              basicAmount,
              IGSTRate,
              IGSTAmount,
              CGSTRate,
              CGSTAmount,
              SGSTRate,
              SGSTAmount,
              TotalAmount]
    
    if os.path.isfile(filename)==False:
        with open(filename, 'w') as f:
            dataWriter = csv.writer(f, delimiter=',')
            dataWriter.writerow(["Date",
                                 "Invoice Number",
                                 "Vendor Name",
                                 "Item",
                                 "GST Number",
                                 "Sale/Purchase",
                                 "Basic Amount",
                                 "IGST Rate",
                                 "IGST Amount",
                                 "CGST Rate",
                                 "CGST Amount",
                                 "SGST Rate",
                                 "SGST Amount",
                                 "Total Amount"])
            dataWriter.writerow(newRow)

    else:
        with open(filename, 'a') as f:
            dataWriter = csv.writer(f, delimiter=',')
            dataWriter.writerow(newRow)

def writeToVendorCSV(filename, updatedDate, invoiceNumber, vendorName, item,
               GSTNumber, salePurchase, basicAmount, IGSTRate, IGSTAmount,
               CGSTRate, CGSTAmount, SGSTRate, SGSTAmount, TotalAmount,
                     paymentDone, paymentDue):
    newRow = [updatedDate,
              invoiceNumber,
              vendorName,
              item,
              GSTNumber,
              salePurchase,
              basicAmount,
              IGSTRate,
              IGSTAmount,
              CGSTRate,
              CGSTAmount,
              SGSTRate,
              SGSTAmount,
              TotalAmount]
    if os.path.isfile(filename)==False:
        with open(filename, 'w') as f:
            dataWriter = csv.writer(f, delimiter=',')
            dataWriter.writerow(["Date",
                                 "Invoice Number",
                                 "Vendor Name",
                                 "Item",
                                 "GST Number",
                                 "Sale/Purchase",
                                 "Basic Amount",
                                 "IGST Rate",
                                 "IGST Amount",
                                 "CGST Rate",
                                 "CGST Amount",
                                 "SGST Rate",
                                 "SGST Amount",
                                 "Total Amount"])
            dataWriter.writerow(newRow)
            dataWriter.writerow([])
            dataWriter.writerow(["",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "Total",
                                 TotalAmount])
            dataWriter.writerow(["",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "Amount Paid",
                                 paymentDone])
            dataWriter.writerow(["",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "Amount Due",
                                 paymentDue])
    else:
        data = []
        with open(filename, 'r') as f:
            dataReader = csv.reader(f)
            for row in dataReader:
                dataPresent = 0
                for i in range(len(row)):
                    if row[i]!='':
                        dataPresent = 1
                        break
                if dataPresent:
                    if row[12]=='Total':
                        row[13] = float(row[13]) + newRow[13]
                    elif row[12]=='Amount Paid':
                        row[13] = float(row[13]) + paymentDone
                    elif row[12]=='Amount Due':
                        row[13] = float(row[13]) + paymentDue
                    data.append(row)
                else:
                    data.append(newRow)
                    data.append(row)

        with open(filename, 'w') as f:
            dataWriter = csv.writer(f)
            for i in range(len(data)):
                dataWriter.writerow(data[i])


def updateData(monthFile, data, IGSTAmount, CGSTAmount, SGSTAmount):
    rows = []
    newTotalAmount = 0.0
    with open(monthFile, 'r') as f:
        dataReader = csv.reader(f)
        for row in dataReader:
            if matching(row, data):
                prevBasicAmount = float(row[6])
                prevIGSTAmount = float(row[8])
                prevCGSTAmount = float(row[10])
                prevSGSTAmount = float(row[12])
                prevTotalAmount = float(row[13])

                if IGSTAmount!=0.0:
                    newIGSTAmount = IGSTAmount
                else:
                    newIGSTAmount = prevIGSTAmount
                
                if CGSTAmount!=0.0:
                    newCGSTAmount = CGSTAmount
                else:
                    newCGSTAmount = prevCGSTAmount

                if SGSTAmount!=0.0:
                    newSGSTAmount = SGSTAmount
                else:
                    newSGSTAmount = prevSGSTAmount

                newTotalAmount = round(prevBasicAmount + newIGSTAmount + newCGSTAmount + newSGSTAmount, 3)  

                # IGST amount, CGST amount, SGST amount, total amount update
                row[8] = newIGSTAmount
                row[10] = newCGSTAmount
                row[12] = newSGSTAmount
                row[13] = newTotalAmount
                
            rows.append(row)
    return rows, newTotalAmount

def matching(row, data):
    #print(row)
    if row[0]==data['Date'] and row[1]==data['Invoice Number'] and row[2]==data['Vendor Name'] and row[3]==data['Item'] and row[4]==data['GST Number'] and row[5]==data['Sale/Purchase'] and row[6]==data['Basic Amount'] and row[7]==data['IGST Rate'] and row[9]==data['CGST Rate'] and row[11]==data['SGST Rate']:
        return True
    print(row)
    return False


def updateVendorData(vendorFile, data, IGSTAmount, CGSTAmount, SGSTAmount):
    vendorRows = []
    prevTotalAmount = 0.0
    newTotalAmount = 0.0
    with open(vendorFile, 'r') as f:
        dataReader = csv.reader(f)
        for row in dataReader:
            if len(row)==0:
                vendorRows.append(row)
                continue
    
            elif row[12]=='Total':
                row[13] = float(row[13]) - prevTotalAmount + newTotalAmount
                vendorRows.append(row)
                
            elif row[12]=='Amount Due':
                row[13] = float(row[13]) - prevTotalAmount + newTotalAmount
                vendorRows.append(row)
                
            elif matching(row, data):
                prevBasicAmount = float(row[6])
                prevIGSTAmount = float(row[8])
                prevCGSTAmount = float(row[10])
                prevSGSTAmount = float(row[12])
                prevTotalAmount = float(row[13])

                if IGSTAmount!=0.0:
                    newIGSTAmount = IGSTAmount
                else:
                    newIGSTAmount = prevIGSTAmount
                
                if CGSTAmount!=0.0:
                    newCGSTAmount = CGSTAmount
                else:
                    newCGSTAmount = prevCGSTAmount

                if SGSTAmount!=0.0:
                    newSGSTAmount = SGSTAmount
                else:
                    newSGSTAmount = prevSGSTAmount

                newTotalAmount = round(prevBasicAmount + newIGSTAmount + newCGSTAmount + newSGSTAmount, 3)  

                # IGST amount, CGST amount, SGST amount, total amount update
                row[8] = newIGSTAmount
                row[10] = newCGSTAmount
                row[12] = newSGSTAmount
                row[13] = newTotalAmount

                vendorRows.append(row)
            else:
                vendorRows.append(row)
    return vendorRows


# A welcome message to test our server
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_account', methods=['GET', 'POST'])
def addAccount():
    if request.method == 'POST':
        firmName = request.form.get('firmName')
        date = request.form.get('date')
        invoiceNumber = request.form.get('invoice')
        vendorName = request.form.get('vendor')
        item = request.form.get('item')
        GSTNumber = request.form.get('gstNumber')
        saleFlag = request.form.get('sale')
        purchaseFlag = request.form.get('purchase')
        basicAmount = request.form.get('basicAmount')
        IGSTRate = request.form.get('igstRate')
        CGSTRate = request.form.get('cgstRate')
        SGSTRate = request.form.get('sgstRate')

        [year, month, day] = date.split('-')

        if saleFlag==None:
            salePurchase = 'Purchase'
        else:
            salePurchase = 'Sale'

        if len(item)!=0:
            item = item.replace(',', ';')

        basicAmount = basicAmount.strip()
        if len(basicAmount)==0:
            basicAmount = 0.0
        else:
            basicAmount = float(basicAmount)
        
        IGSTRate = IGSTRate.strip()
        if len(IGSTRate)==0:
            IGSTRate = 0.0
        else:
            IGSTRate = float(IGSTRate)

        CGSTRate = CGSTRate.strip()
        if len(CGSTRate)==0:
            CGSTRate = 0.0
        else:
            CGSTRate = float(CGSTRate)

        SGSTRate = SGSTRate.strip()
        if len(SGSTRate)==0:
            SGSTRate = 0.0
        else:
            SGSTRate = float(SGSTRate)

        # Calculate amount
        IGSTAmount = round(basicAmount * (IGSTRate/100), 3)
        CGSTAmount = round(basicAmount * (CGSTRate/100), 3)
        SGSTAmount = round(basicAmount * (SGSTRate/100), 3)
        TotalAmount = round(float(basicAmount) + float(IGSTAmount) + float(CGSTAmount) + float(SGSTAmount), 3)


        # Create directory if not present
        accountFolder = "Documents/Accounts/"
        if os.path.exists(accountFolder)==False:
            os.makedirs(accountFolder)

        # Create directory if not present
        firmFolder = accountFolder + firmName + "/"
        if os.path.exists(firmFolder)==False:
            os.makedirs(firmFolder)
        
        # Create directory if not present
        dataFolder = firmFolder + "Data/"
        if os.path.exists(dataFolder)==False:
            os.makedirs(dataFolder)

        # Create year folder if not present
        yearFolder = dataFolder + year + "/"
        if os.path.exists(yearFolder)==False:
            os.makedirs(yearFolder)
        
        # Month file
        monthName = months[int(month)-1]
        monthFile = yearFolder + monthName + ".csv"

        updatedDate = monthName + ' ' + day + ', ' + year 
        
        
        writeToCSV(monthFile, updatedDate, invoiceNumber, vendorName, item,
               GSTNumber, salePurchase, basicAmount, IGSTRate, IGSTAmount,
               CGSTRate, CGSTAmount, SGSTRate, SGSTAmount, TotalAmount)

        # Create directory if not present
        vendorFolder = firmFolder + "VendorData/"
        if os.path.exists(vendorFolder)==False:
            os.makedirs(vendorFolder)

        # Vendor file
        vendorFileName = vendorName.lower() + '_' + GSTNumber
        vendorFile = vendorFolder + vendorFileName + ".csv"
        writeToVendorCSV(vendorFile, updatedDate, invoiceNumber, vendorName, item,
                   GSTNumber, salePurchase, basicAmount, IGSTRate, IGSTAmount,
                   CGSTRate, CGSTAmount, SGSTRate, SGSTAmount, TotalAmount,
                         0.0, TotalAmount)
        result = {}
        result['Firm Name'] = firmName
        result['Vendor Name'] = vendorName
        result['Date'] = updatedDate
        result['Invoice Number'] = invoiceNumber
        result['Item'] = item
        result['GST Number'] = GSTNumber
        result['Sale/Purchase'] = salePurchase
        result['Basic Amount'] = basicAmount
        result['IGST Rate'] = IGSTRate
        result['IGST Amount'] = IGSTAmount
        result['CGST Rate'] = CGSTRate
        result['CGST Amount'] = CGSTAmount
        result['SGST Rate'] = SGSTRate
        result['SGST Amount'] = SGSTAmount
        result['Total Amount'] = TotalAmount
        return render_template('results.html', result=result)
    else:
        return render_template('add_account.html')


@app.route('/update_account', methods=['GET', 'POST'])
def updateAccount():
    if request.method == 'POST':
        firmName = request.form.get('firmName')
        date = request.form.get('date')
        invoiceNumber = request.form.get('invoice')
        vendorName = request.form.get('vendor')
        item = request.form.get('item')
        GSTNumber = request.form.get('gstNumber')
        salePurchase = request.form.get('salePurchase')
        basicAmount = request.form.get('basicAmount')
        IGSTRate = request.form.get('igstRate')
        CGSTRate = request.form.get('cgstRate')
        SGSTRate = request.form.get('sgstRate')
        IGSTAmount = request.form.get('igstAmount')
        CGSTAmount = request.form.get('cgstAmount')
        SGSTAmount = request.form.get('sgstAmount')

        date = date.replace(',', '')
        [monthName, day, year] = date.split(' ')

        if len(item)!=0:
            item = item.replace(',', ';')
        
        IGSTAmount = IGSTAmount.strip()
        if len(IGSTAmount)==0:
            IGSTAmount = 0.0
        else:
            IGSTAmount = float(IGSTAmount)

        CGSTAmount = CGSTAmount.strip()
        if len(CGSTAmount)==0:
            CGSTAmount = 0.0
        else:
            CGSTAmount = float(CGSTAmount)

        SGSTAmount = SGSTAmount.strip()
        if len(SGSTAmount)==0:
            sGSTAmount = 0.0
        else:
            SGSTAmount = float(SGSTAmount)

        
        accountFolder = "Documents/Accounts/"
        firmFolder = accountFolder + firmName + "/"
        dataFolder = firmFolder + "Data/"
        yearFolder = dataFolder + year + "/"
        monthFile = yearFolder + monthName + ".csv"

        updatedDate = monthName + ' ' + day + ', ' + year 

        result = {}
        result['Firm Name'] = firmName
        result['Vendor Name'] = vendorName
        result['Date'] = updatedDate
        result['Invoice Number'] = invoiceNumber
        result['Item'] = item
        result['GST Number'] = GSTNumber
        result['Sale/Purchase'] = salePurchase
        result['Basic Amount'] = basicAmount
        result['IGST Rate'] = IGSTRate
        result['CGST Rate'] = CGSTRate
        result['SGST Rate'] = SGSTRate
        
        
        rows, TotalAmount = updateData(monthFile, result, IGSTAmount, CGSTAmount, SGSTAmount)
        with open(monthFile, 'w') as f:
            dataWriter = csv.writer(f, delimiter=',')
            for row in rows:
                dataWriter.writerow(row)


        vendorFolder = firmFolder + "VendorData/"
        vendorFileName = vendorName.lower() + '_' + GSTNumber
        vendorFile = vendorFolder + vendorFileName + ".csv"
        vendorRows = updateVendorData(vendorFile, result, IGSTAmount, CGSTAmount, SGSTAmount)
        with open(vendorFile, 'w') as f:
            dataWriter = csv.writer(f, delimiter=',')
            for row in vendorRows:
                dataWriter.writerow(row)


        result['IGST Amount'] = IGSTAmount
        result['CGST Amount'] = CGSTAmount
        result['SGST Amount'] = SGSTAmount
        result['Total Amount'] = TotalAmount
        return render_template('results.html', result=result)
        


@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        firmName = request.form.get('firmName')
        date = request.form.get('date')
        invoiceNumber = request.form.get('invoice')
        vendorName = request.form.get('vendor')
        item = request.form.get('item')
        GSTNumber = request.form.get('gstNumber')
        saleFlag = request.form.get('sale')
        purchaseFlag = request.form.get('purchase')
        basicAmount = request.form.get('basicAmount')
        IGSTRate = request.form.get('igstRate')
        CGSTRate = request.form.get('cgstRate')
        SGSTRate = request.form.get('sgstRate')


        # Create directory if not present
        accountFolder = "Documents/Accounts/"
        if os.path.exists(accountFolder)==False:
            os.makedirs(accountFolder)

        # Create directory if not present
        firmFolder = accountFolder + firmName + "/"
        if os.path.exists(firmFolder)==False:
            os.makedirs(firmFolder)
        
        # Create directory if not present
        dataFolder = firmFolder + "Data/"
        if os.path.exists(dataFolder)==False:
            os.makedirs(dataFolder)

         
        return render_template('home.html')
    else:
        return render_template('add_payment.html')
        

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
