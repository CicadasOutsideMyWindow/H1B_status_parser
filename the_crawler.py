import csv
import time
from selenium import webdriver

total_pages = 498
timer = 10
datafile = 'data.csv'

service_center_location = ''    # California, Nebraska, Texas, Vermont
# case_priority = 'regular'              # premium, regular
# application_status = 'approved'         # approved, denied, pending, withdrawn
application_year = ''               # 2016, 2017, 2018
application_month = ''                #01,02,03...10,11,12


def _url(path):
    return 'https://www.trackitt.com/usa-immigration-trackers/h1b/page/%s' % path


def mine_data(url):

    driver = webdriver.Chrome()
    driver.get(url)

    table = driver.find_element_by_xpath('//*[@id="trackers_table"]/tbody')
    count = 0

    for row in table.find_elements_by_xpath(".//tr"):
        data = [td.text.encode('utf-8') for td in row.find_elements_by_xpath(".//td")]
        write_to_csv(data)
        count += 1
        print 'Getting row: %s' % count
 
    driver.close()


def write_to_csv(row):
    f = csv.writer(open("data.csv", "a"))
    f.writerow(row)


def read_csv():
    with open(datafile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            case_type = line[4]
            service_center = line[5]
            priority = line[6]
            app_filed = line[7]
            app_received = line[8]
            rfe = line[10]
            rfe_received =line[11]
            rfe_replied = line[13]
            app_status = line[14]
            resol_data = line[15]
            processing_time = line[18]

            if service_center == service_center_location:
                if len(app_received) > 0:
                    date = app_received.split('/')
                    month = date[0]
                    year = date[2]
                    if month == application_month and year == application_year:
                        row = case_type, priority, app_received, app_status, resol_data, processing_time
                        print row
                else:
                    print '...'


def crawl():
    for index in range(1,total_pages):
        url = _url('/%s') % index
        mine_data(url)
        print 'Page %s of %s processed' %(index,total_pages)
        time.sleep(timer)

read_csv()
