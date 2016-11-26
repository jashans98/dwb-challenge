# I'm using a super primitive trading algorithm for this

f = open('in.csv', 'r')

out = open('out.csv', 'w')

# writes out the date and the number of shares to buy at the time
def writeOut(date, numshares):
    out.write('{0}, {1}\n'.format(date, numshares))

boughtshares = 0
totalprofit = 0

prevPrices = []

# computes standard deviation
def stddev(prices):
    n = float(len(prices))
    return (sum([a*a for a in prices])/n - (sum(prices)/n)**2) ** 0.5

# index to determine how much to buy or sell today
def buy_index(prevPrices, today):

    # compute the average as a useful variable
    mean = sum(prevPrices)/(float(len(prevPrices)))

    # we want to buy when today's price is below average, sell when above average
    # the amount we buy or sell is determined based on the weight we give it, and how much we own

    # just some generic index to use
    if stddev(prevPrices) == 0:
        return 0.3
    elif today < mean:
        return - ((mean - stddev(prevPrices)) / stddev(prevPrices))
    else:
        return (mean - stddev(prevPrices)) / 3*stddev(prevPrices)

def makePurchase(index, ownedshares, date):
    remaining = 1000 - ownedshares
    toBuy = min(remaining, abs(index) * remaining)
    if index < 0:
        toBuy = -toBuy

    toBuy = int(toBuy)
    writeOut(date, toBuy)
    return ownedshares + toBuy

for line in f:
    date = line.split(',')[0]
    try:
        price = float(line.split(',')[1])
        prevPrices.append(price)
        boughtshares = makePurchase(buy_index(prevPrices, price), boughtshares, date)
    except ValueError:
        pass

f.close()
out.close()
