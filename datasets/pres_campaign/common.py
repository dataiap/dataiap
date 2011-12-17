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
abbrtoname.update(dict([(row[-2], row[0]) for row in statenames]))
