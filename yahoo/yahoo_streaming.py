from yahoo_finance import Share
import time


if __name__ == '__main__':
    
    
    
    yahoo_prices = []
    google_prices = []
    ibm_prices = []
    microsoft_prices = []
    oracle_prices = []
    
    
    yahoo = Share('YHOO')
    google = Share('GOOGL')
    ibm = Share('IBM')
    microsoft = Share('MSFT')
    oracle = Share('ORCL')
    
    for i in range(0,30):
        yahoo.refresh()
        google.refresh()
        ibm.refresh()
        microsoft.refresh()
        oracle.refresh()
        yahoo_prices.append(yahoo.get_price())
        google_prices.append(google.get_price())
        ibm_prices.append(ibm.get_price())
        microsoft_prices.append(microsoft.get_price())
        oracle_prices.append(oracle.get_price())
        time.sleep(60)

    print 'yahoo',
    for x in yahoo_prices:
        print ' ',
        print x,
    print '\n',

    print 'google',
    for x in google_prices:
        print ' ',
        print x,
    print '\n',

    print 'ibm',
    for x in ibm_prices:
        print ' ',
        print x,
    print '\n',

    print 'microsoft',
    for x in microsoft_prices:
        print ' ',
        print x,
    print '\n',


    print 'oracle',
    for x in oracle_prices:
        print ' ',
        print x,
    print '\n',
























