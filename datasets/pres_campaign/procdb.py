import csv,sys,datetime,collections,sqlite3
import itertools
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
markers = [None, 'o', '+', 'x', 'D']
styles = ['-', '--']
lineattrs = [(color, m, s)  for s in styles for m in markers for color in colors ]

# def convert_datetime(d):
#     return datetime.datetime.strptime(d, '%Y-%m-%d')
# sqlite3.register_converter('date',  convert_datetime)
db = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES)

cur = db.execute('select distinct name from donations')
names = [row[0] for row in cur.fetchall()]

print names


#
# process individual negative donations
#

maxnegativereturn = db.execute("""select date, -sum(amount) from donations where
                                  amount < 0 group by date order by date desc limit
                                  1""").fetchone()[1]


for idx, name in enumerate(names):
    print name

    fig = plt.figure(figsize=(30, 10))
    ax = fig.add_subplot(111, ylim = [0, maxnegativereturn / 1000.0])
    
    cur = db.execute("select sum(amount) from donations where name = ? and amount < 0",
                     (name,))
    returns = cur.fetchone()[0]
    cur = db.execute("""select distinct reason from donations where
                        name = ? and amount < 0""", (name,))
    allreasons = set()
    for row in cur.fetchall():
        reason = row[0]
        if reason == '':
            allreasons.add(reason)
        elif reason.startswith('*'):
            allreasons.add(reason.split()[1])
        else:
            allreasons.add(reason.split()[0])
    
    if not len(allreasons): continue
    legenditems = []
    legendtitles = []
    for idx, reason in enumerate(allreasons):
        if reason == '':
            cur = db.execute("""select date, -sum(amount) / 1000.0 from donations where
                                name = ? and reason like ? and amount < 0 group by date order by
                                date asc""", (name, reason))
            reason = 'No Reason'
        else:
            cur = db.execute("""select date, -sum(amount) / 1000.0 from donations where
                                name = ? and reason like ? and amount < 0 group by date order by
                                date asc""", (name, '%%%s%%' % reason))
            
        data = cur.fetchall()
        xs, ys = zip(*data)
        c,m,l = lineattrs[idx % len(lineattrs)]
        legenditems.append(Rectangle((0, 0), 1, 1, fc=c))
        legendtitles.append(reason)
        ax.scatter(xs, ys, color=c,  s=15)#, label=reason)
    ax.legend(legenditems, legendtitles, loc='upper center', ncol = 4, fancybox=True,
                     shadow=True)
    ax.set_title("Negative Donations %s" % name, size=20)    
    ax.set_ylabel('-dollars in thousands')
    plt.savefig('./figs/negativedonations_%s.png' % ''.join(name.strip()),
                     format='png')
    plt.cla()
    plt.clf()


lineattrs = [(color, m, s)  for m in markers for s in styles  for color in colors ]

fig = plt.figure(figsize=(30, 10))
ax = fig.add_subplot(111)
for idx, name in enumerate(names):
    cur = db.execute("""select date, -sum(amount) / 1000.0 from donations
                      where name = ? and amount < 0 group by date
                      order by date asc""", (name,))
    data = cur.fetchall()
    if len(data) == 0: continue
    xs, ys = zip(*data)
    ys = [sum(ys[:i]) for i in xrange(1,len(ys)+1) ]
    c,m,l = lineattrs[idx]
    ax.plot(xs, ys, 'k-', color=c, marker=m, linestyle=l, label=name)
ax.legend(loc='upper center', ncol = 4, fancybox=True, shadow=True)
ax.set_ylabel('-dollars in thousands')
ax.set_title("Negative Donations Total", size=20)    
plt.savefig('./figs/negativedonations_all.png', format='png')




fig = plt.figure(figsize=(30, 10))
ax = fig.add_subplot(111)
for idx, name in enumerate(names):
    cur = db.execute("select date, sum(amount) / 1000000.0 from donations where name = ? group by date order by date asc", (name,))
    xs, ys = zip(*cur.fetchall())
    ys = [sum(ys[:i]) for i in xrange(1,len(ys)+1) ]
    c,m,l = lineattrs[idx]
    ax.plot(xs, ys, 'k-', color=c, marker=m, linestyle=l, label=name)
ax.legend(loc='upper center', ncol = 4, fancybox=True, shadow=True)
ax.set_ylabel('dollars in millions')
ax.set_title("Total Donations", size=20)    
plt.savefig('./figs/totaldonations.png', format='png')
#plt.show()







db.close()
