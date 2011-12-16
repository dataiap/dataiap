import csv,sys,datetime,collections
import itertools
import matplotlib.pyplot as plt


colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
          '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5']
markers = [None]#, 'o']
styles = ['-', '--']
lineattrs = [(color, m, s) for color in colors for m in markers
             for s in styles]
reader = csv.DictReader(open(sys.argv[1], 'r'))
idx = 0

candtomoney = collections.defaultdict(list)
candreturns = collections.defaultdict(list)

for row in reader:
    name = row['cand_nm']
    datestr = row['contb_receipt_dt']
    amount = float(row['contb_receipt_amt'])
    date = datetime.datetime.strptime(datestr, '%d-%b-%y')
    reason = row['receipt_desc']
    name = name.replace(',', '')
    reason = reason.replace(',', '')
    print ','.join(map(str, [name, date.strftime('%Y-%m-%d'), amount,
    reason]))
    
    candtomoney[name].append((date, amount))
    if amount < 0 and 'REATTRIBUTION' in reason:
        print name, date, amount, reason
        candreturns[name].append((date, -amount))
#    if idx > 50: break
    idx += 1

candtotals = dict([(name, sum(map(lambda p:p[1], val))) for name, val
                   in candtomoney.iteritems()])

fig = plt.figure(figsize=(30, 10))

idx = 0
for name, monies in candtomoney.iteritems():#candreturns.iteritems():
    monies.sort(key=lambda pair: pair[0])
    i = itertools.groupby(monies, key=lambda p: p[0])
    monies = map(lambda (key, pairs): (key, sum([float(pair[1]) for
                                                 pair in pairs])), i)
    total = 0
    newmonies = []
    for pair in monies:
        total += pair[1]
        newmonies.append((pair[0], total ))#/ (candtotals[name]+1)))
    monies = newmonies

    xs,ys = zip(*monies)
    c,m,l = lineattrs[idx]
    plt.plot(xs, ys, 'k-', color=c, marker=m, linestyle=l, label=name)
    idx += 1
plt.legend(loc='upper center', ncol = 4, fancybox=True, shadow=True)
plt.savefig('/tmp/test.png', format='png')
    
