import csv
import ols
import numpy

dependent = ["YPLL Rate"]
independent = ["Population", "< 18", "65 and over", "African American", "Female", "Rural", "%Diabetes" , "HIV rate", "Physical Inactivity" , "mental health provider rate", "median household income", "% high housing costs", "% Free lunch", "% child Illiteracy", "% Drive Alone"]
#dependent = ["% Free lunch",]
#independent = ["median household income",]

def read(file, cols, check_reliable):
    reader = csv.DictReader(open(file, 'rU'))
    rows = {}
    for row in reader:
        if check_reliable and row['Unreliable'] == "x":
            continue
        if row['County'] == "":
            continue
        rname = "%s__%s" % (row['State'], row['County'])
        try:
            rows[rname] = [float(row[col]) for col in cols]
        except:
            pass
    return rows

def get_arrs():
    ypll = read("ypll.csv", dependent, True)
    adtl = read("additional_measures_cleaned.csv", independent, False)

    ypll_arr = []
    adtl_arr = []
    for k,v in ypll.iteritems():
        if k in adtl:
            ypll_arr.append(v[0])
            adtl_arr.append(adtl[k])
    return (numpy.array(ypll_arr), numpy.array(adtl_arr))

if __name__ == "__main__":
    ypll_arr, adtl_arr = get_arrs()
    model = ols.ols(ypll_arr, adtl_arr, dependent[0], independent)
    print model.summary()
