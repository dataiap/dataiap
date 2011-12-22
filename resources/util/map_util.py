from collections import defaultdict
import json, os

blues = ['#FFF7FB', '#ECE7F2', '#D0D1E6', '#A6BDDB', '#74A9CF',
         '#3690C0', '#0570B0', '#045A8D', '#023858']
_color_idx = 0


# state name -> [ polygon, ... ]
state2poly = defaultdict(list)
# county fips id -> [ polygon, ... ]
fips2poly = defaultdict(list)

data = json.load(file('../datasets/geo/us-states.json'))
for f in data['features']:
    state = f['properties']['name']
    geo = f['geometry']
    if geo['type'] == 'Polygon':
        for coords in geo['coordinates']:
            state2poly[state].append(coords)
    elif geo['type'] == 'MultiPolygon':
        for polygon in geo['coordinates']:
            state2poly[state].extend(polygon)

data = json.load(file('../datasets/geo/us-counties.json'))
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
        raise RuntimeError, "state %s not found" % names
    if 'color' not in kwargs:
        color = blues[_color_idx]
        _color_idx = (_color_idx+1) % len(blues)
        kwargs['color'] = color
    for polygon in state2poly[name]:
        draw_polygon(subplot, polygon, **kwargs)

def draw_county(subplot, fips, **kwargs):
    """
    draw_county(subplot, fips, color=..., **kwargs)
    
    Automatically draws a filled shape representing the county with id fips in
    subplot.  The color keyword argument specifies the fill color.  It accepts keyword
    arguments that plot() accepts

    The fips id is described at http://en.wikipedia.org/wiki/FIPS_county_code
    """
    global _color_idx
    if fips not in fips2poly:
        raise RuntimeError, 'County fips %d not found' % fips
    if 'color' not in kwargs:
        color = blues[_color_idx]
        _color_idx = (_color_idx+1) % len(blues)
        kwargs['color'] = color
    for polygon in fips2poly[fips]:
        draw_polygon(subplot, polygon, **kwargs)
    


