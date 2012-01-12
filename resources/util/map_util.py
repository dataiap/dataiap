from collections import defaultdict
import json, os

blues = ['#FFF7FB', '#ECE7F2', '#D0D1E6', '#A6BDDB', '#74A9CF',
         '#3690C0', '#0570B0', '#045A8D', '#023858']
_color_idx = 0
MYDIR = os.path.dirname(globals()['__file__'])

# state name -> [ polygon, ... ]
state2poly = defaultdict(list)
# county fips id -> [ polygon, ... ]
fips2poly = defaultdict(list)

data = json.load(file(os.path.join(MYDIR, 'us-states.json')))
for f in data['features']:
    state = f['properties']['name']
    geo = f['geometry']
    if geo['type'] == 'Polygon':
        for coords in geo['coordinates']:
            state2poly[state].append(coords)
    elif geo['type'] == 'MultiPolygon':
        for polygon in geo['coordinates']:
            state2poly[state].extend(polygon)

data = json.load(file(os.path.join(MYDIR, './us-counties.json')))
for f in data['features']:
    fips = f['id']
    geo = f['geometry']
    if geo['type'] == 'Polygon':
        for coords in geo['coordinates']:
            fips2poly[fips].append(coords)
    elif geo['type'] == 'MultiPolygon':
        for polygon in geo['coordinates']:
            fips2poly[fips].extend(polygon)


def draw_polygon(subplot, coords, **kwargs):
    xs, ys = zip(*coords)
    subplot.fill(xs, ys, **kwargs)
    # kwargs = dict(kwargs)
    # kwargs['color'] = 'grey'
    # if 'linewidth' not in kwargs:
    #     kwargs['linewidth'] = 0
    # subplot.plot(xs, ys, **kwargs)



def draw_state(subplot, name, **kwargs):
    """
    draw_state(subplot, state, color=..., **kwargs)
    
    Automatically draws a filled shape representing the state in
    subplot.  *state* is the full name of the state, as defined by USPS
    (https://www.usps.com/send/official-abbreviations.htm).
    The color keyword argument specifies the fill color.  It accepts keyword
    arguments that plot() accepts
    """
    global _color_idx
    if name not in state2poly:
        if get_statename(name) in state2poly:
            name = get_statename(name)
        else:
            print "state %s not found" % name
            return
    if 'color' not in kwargs:
        color = blues[_color_idx]
        _color_idx = (_color_idx+1) % len(blues)
        kwargs['color'] = color
    for polygon in state2poly[name]:
        draw_polygon(subplot, polygon, **kwargs)
    subplot.set_xlim(-200, -50)
    subplot.set_ylim(15, 80)

def draw_county(subplot, fips, **kwargs):
    """
    draw_county(subplot, fips, color=..., **kwargs)
    
    Automatically draws a filled shape representing the county with id fips in
    subplot.  The color keyword argument specifies the fill color.  It accepts keyword
    arguments that plot() accepts

    The fips id is described at http://en.wikipedia.org/wiki/FIPS_county_code
    """
    global _color_idx
    fips = str(fips)
    if fips not in fips2poly:
        #raise RuntimeError, 'County fips %s not found' % fips
        print 'County fips %s not found' % fips
        return
    if 'color' not in kwargs:
        color = blues[_color_idx]
        _color_idx = (_color_idx+1) % len(blues)
        kwargs['color'] = color
    for polygon in fips2poly[fips]:
        draw_polygon(subplot, polygon, **kwargs)
    subplot.set_xlim(-200, -50)
    subplot.set_ylim(15, 80)
    


from collections import defaultdict

statenames = """Alabama	Ala.	AL	Montgomery
Alaska	Alaska	AK	Juneau
Arizona	Ariz.	AZ	Phoenix
Arkansas	Ark.	AR	Little Rock
California	Calif.	CA	Sacramento
Colorado	Colo.	CO	Denver
Connecticut	Conn.	CT	Hartford
Delaware	Del.	DE	Dover
Florida	Fla.	FL	Tallahassee
Georgia	Ga.	GA	Atlanta
Hawaii	Hawaii	HI	Honolulu
Idaho	Idaho	ID	Boise
Illinois	Ill.	IL	Springfield
Indiana	Ind.	IN	Indianapolis
Iowa	Iowa	IA	Des Moines
Kansas	Kans.	KS	Topeka
Kentucky	Ky.	KY	Frankfort
Louisiana	La.	LA	Baton Rouge
Maine	Maine	ME	Augusta
Maryland	Md.	MD	Annapolis
Massachusetts	Mass.	MA	Boston
Michigan	Mich.	MI	Lansing
Minnesota	Minn.	MN	St. Paul
Mississippi	Miss.	MS	Jackson
Missouri	Mo.	MO	Jefferson City
Montana	Mont.	MT	Helena
Nebraska	Nebr.	NE	Lincoln
Nevada	Nev.	NV	Carson City
New Hampshire	N.H.	NH	Concord
New Jersey	N.J.	NJ	Trenton
New Mexico	N.M.	NM	Santa Fe
New York	N.Y.	NY	Albany
North Carolina	N.C.	NC	Raleigh
North Dakota	N.D.	ND	Bismarck
Ohio	Ohio	OH	Columbus
Oklahoma	Okla.	OK	Oklahoma City
Oregon	Ore.	OR	Salem
Pennsylvania	Pa.	PA	Harrisburg
Rhode Island	R.I.	RI	Providence
South Carolina	S.C.	SC	Columbia
South Dakota	S.D.	SD	Pierre
Tennessee	Tenn.	TN	Nashville
Texas	Tex.	TX	Austin
Utah	Utah	UT	Salt Lake City
Vermont	Vt.	VT	Montpelier
Virginia	Va.	VA	Richmond
Washington	Wash.	WA	Olympia
West Virginia	W.Va.	WV	Charleston
Wisconsin	Wis.	WI	Madison
Wyoming	Wyo.	WY	Cheyenne
American Samoa	n/a	AS	Pago Pago
District of Columbia	D.C.	DC	Washington
Federated States of Micronesia	FSM	FM	Palikir
Guam	Guam	GU	Hagatna
Marshall Islands	n/a	MH	Majuro
Northern Mariana Islands	n/a	MP	Saipan
Palau	Palau	PW	Koror
Puerto Rico	P.R.	PR	San Juan
Virgin Islands	V.I.	VI	Charlotte Amalie
Armed Forces Europe	n/a	AE	n/a
Armed Forces Pacific	n/a	AP	n/a
Armed Forces Americas	n/a	AA	n/a""".split('\n')
statenames = [line.split('\t') for line in statenames]
abbrtoname = defaultdict(lambda:"Other")
abbrtoname.update(dict([(row[-2].lower(), row[0]) for row in statenames]))

def get_statename(abbr):
   return abbrtoname[abbr.strip().lower()] 
