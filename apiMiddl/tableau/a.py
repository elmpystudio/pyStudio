from urllib.parse import quote_plus

ticket = ("PjVRxt1xRo-FibfaXtjpGA==:Ca--2RzgOYxEsnX_3xAd_clR")
workbook_name = "test_workbook"
last = "dataset_csv"
a = ("http://tab.entomu.com:8999/trusted/%s/t/API/authoringNewWorkbook/%s/%s" % (ticket, workbook_name, last))
print(a)
