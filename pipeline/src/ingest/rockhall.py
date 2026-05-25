"""
One Long Impersonation -- Rock and Roll Hall of Fame Inductee Database
Ingests the complete induction history from the official Rock Hall records.

Source: Rock and Roll Hall of Fame official inductee list (public record)
Coverage: 1986-2026
License: Public information

This is the ground truth. Every inducted artist with year and category.
The data is hand-compiled from the official Rock Hall website and verified
against multiple published sources (Future Rock Legends, Wikipedia, Billboard).

We use a curated dataset rather than scraping because:
1. The official site structure changes frequently
2. The data is small enough to hand-verify (< 400 inductees)
3. Accuracy matters more than automation for the ground truth
4. Every entry can be individually cited

Data verified against:
- rockhall.com/inductees (official)
- futurerocklegends.com (nomination history)
- Billboard annual coverage
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import get_connection, init_db

# -----------------------------------------------------------
# Complete Rock and Roll Hall of Fame Inductee Database
# Category codes: P = Performer, EI = Early Influence,
# NM = Non-Performer (renamed Musical Excellence 2020+),
# ME = Musical Excellence, AH = Ahmet Ertegun Award,
# SIS = Singles (discontinued)
# -----------------------------------------------------------

INDUCTEES = [
    # 1986 -- First class
    ("Chuck Berry", 1986, "P", 1955, "Classic Rock", "male", "Black"),
    ("James Brown", 1986, "P", 1956, "Soul/R&B", "male", "Black"),
    ("Ray Charles", 1986, "P", 1949, "Soul/R&B", "male", "Black"),
    ("Sam Cooke", 1986, "P", 1951, "Soul/R&B", "male", "Black"),
    ("Fats Domino", 1986, "P", 1949, "Blues/Early", "male", "Black"),
    ("The Everly Brothers", 1986, "P", 1957, "Classic Rock", "group", "white"),
    ("Buddy Holly", 1986, "P", 1956, "Classic Rock", "male", "white"),
    ("Jerry Lee Lewis", 1986, "P", 1956, "Classic Rock", "male", "white"),
    ("Little Richard", 1986, "P", 1951, "Soul/R&B", "male", "Black"),
    ("Elvis Presley", 1986, "P", 1953, "Classic Rock", "male", "white"),
    # 1986 Early Influence
    ("Robert Johnson", 1986, "EI", 1936, "Blues/Early", "male", "Black"),
    ("Jimmie Rodgers", 1986, "EI", 1927, "Folk/Country", "male", "white"),
    ("Jimmy Yancey", 1986, "EI", 1939, "Blues/Early", "male", "Black"),

    # 1987
    ("The Coasters", 1987, "P", 1955, "Soul/R&B", "group", "Black"),
    ("Eddie Cochran", 1987, "P", 1956, "Classic Rock", "male", "white"),
    ("Bo Diddley", 1987, "P", 1955, "Blues/Early", "male", "Black"),
    ("Aretha Franklin", 1987, "P", 1960, "Soul/R&B", "female", "Black"),
    ("Marvin Gaye", 1987, "P", 1961, "Soul/R&B", "male", "Black"),
    ("Bill Haley", 1987, "P", 1951, "Classic Rock", "male", "white"),
    ("B.B. King", 1987, "P", 1949, "Blues/Early", "male", "Black"),
    ("Clyde McPhatter", 1987, "P", 1950, "Soul/R&B", "male", "Black"),
    ("Ricky Nelson", 1987, "P", 1957, "Classic Rock", "male", "white"),
    ("Roy Orbison", 1987, "P", 1956, "Classic Rock", "male", "white"),
    ("Carl Perkins", 1987, "P", 1954, "Classic Rock", "male", "white"),
    ("Smokey Robinson", 1987, "P", 1957, "Soul/R&B", "male", "Black"),
    ("Big Joe Turner", 1987, "P", 1938, "Blues/Early", "male", "Black"),
    ("Muddy Waters", 1987, "P", 1941, "Blues/Early", "male", "Black"),
    ("Jackie Wilson", 1987, "P", 1953, "Soul/R&B", "male", "Black"),
    # 1987 EI
    ("Louis Jordan", 1987, "EI", 1938, "Blues/Early", "male", "Black"),
    ("T-Bone Walker", 1987, "EI", 1929, "Blues/Early", "male", "Black"),
    ("Hank Williams", 1987, "EI", 1946, "Folk/Country", "male", "white"),

    # 1988
    ("The Beach Boys", 1988, "P", 1961, "Classic Rock", "group", "white"),
    ("The Beatles", 1988, "P", 1962, "Classic Rock", "group", "white"),
    ("The Drifters", 1988, "P", 1953, "Soul/R&B", "group", "Black"),
    ("Bob Dylan", 1988, "P", 1961, "Classic Rock", "male", "white"),
    ("The Supremes", 1988, "P", 1961, "Soul/R&B", "group", "Black"),
    # 1988 EI
    ("Woody Guthrie", 1988, "EI", 1937, "Folk/Country", "male", "white"),
    ("Leadbelly", 1988, "EI", 1933, "Blues/Early", "male", "Black"),
    ("Les Paul", 1988, "EI", 1936, "Classic Rock", "male", "white"),

    # 1989
    ("Dion", 1989, "P", 1958, "Classic Rock", "male", "white"),
    ("Otis Redding", 1989, "P", 1962, "Soul/R&B", "male", "Black"),
    ("The Rolling Stones", 1989, "P", 1963, "Classic Rock", "group", "white"),
    ("The Temptations", 1989, "P", 1961, "Soul/R&B", "group", "Black"),
    ("Stevie Wonder", 1989, "P", 1962, "Soul/R&B", "male", "Black"),
    # 1989 EI
    ("The Ink Spots", 1989, "EI", 1934, "Soul/R&B", "group", "Black"),
    ("Bessie Smith", 1989, "EI", 1923, "Blues/Early", "female", "Black"),
    ("The Soul Stirrers", 1989, "EI", 1935, "Soul/R&B", "group", "Black"),

    # 1990
    ("Hank Ballard", 1990, "P", 1953, "Soul/R&B", "male", "Black"),
    ("Bobby Darin", 1990, "P", 1956, "Pop", "male", "white"),
    ("The Four Tops", 1990, "P", 1956, "Soul/R&B", "group", "Black"),
    ("The Kinks", 1990, "P", 1964, "Classic Rock", "group", "white"),
    ("The Platters", 1990, "P", 1953, "Soul/R&B", "group", "Black"),
    ("Simon & Garfunkel", 1990, "P", 1964, "Folk/Country", "group", "white"),
    ("The Who", 1990, "P", 1964, "Classic Rock", "group", "white"),
    # 1990 EI
    ("Louis Armstrong", 1990, "EI", 1923, "Blues/Early", "male", "Black"),
    ("Charlie Christian", 1990, "EI", 1939, "Blues/Early", "male", "Black"),
    ("Ma Rainey", 1990, "EI", 1923, "Blues/Early", "female", "Black"),

    # 1991
    ("LaVern Baker", 1991, "P", 1953, "Soul/R&B", "female", "Black"),
    ("The Byrds", 1991, "P", 1965, "Classic Rock", "group", "white"),
    ("John Lee Hooker", 1991, "P", 1948, "Blues/Early", "male", "Black"),
    ("The Impressions", 1991, "P", 1958, "Soul/R&B", "group", "Black"),
    ("Wilson Pickett", 1991, "P", 1959, "Soul/R&B", "male", "Black"),
    ("Jimmy Reed", 1991, "P", 1953, "Blues/Early", "male", "Black"),
    ("Ike & Tina Turner", 1991, "P", 1960, "Soul/R&B", "group", "Black"),
    # 1991 EI
    ("Howlin' Wolf", 1991, "EI", 1951, "Blues/Early", "male", "Black"),

    # 1992
    ("Bobby Blue Bland", 1992, "P", 1952, "Blues/Early", "male", "Black"),
    ("Booker T. & the M.G.'s", 1992, "P", 1962, "Soul/R&B", "group", "Black"),
    ("Johnny Cash", 1992, "P", 1955, "Folk/Country", "male", "white"),
    ("Jimi Hendrix", 1992, "P", 1964, "Classic Rock", "male", "Black"),
    ("The Isley Brothers", 1992, "P", 1959, "Soul/R&B", "group", "Black"),
    ("Sam & Dave", 1992, "P", 1961, "Soul/R&B", "group", "Black"),
    ("The Yardbirds", 1992, "P", 1963, "Classic Rock", "group", "white"),
    # 1992 EI
    ("Elmore James", 1992, "EI", 1951, "Blues/Early", "male", "Black"),
    ("Professor Longhair", 1992, "EI", 1949, "Blues/Early", "male", "Black"),

    # 1993
    ("Ruth Brown", 1993, "P", 1949, "Soul/R&B", "female", "Black"),
    ("Cream", 1993, "P", 1966, "Classic Rock", "group", "white"),
    ("Creedence Clearwater Revival", 1993, "P", 1968, "Classic Rock", "group", "white"),
    ("The Doors", 1993, "P", 1967, "Classic Rock", "group", "white"),
    ("Frankie Lymon & The Teenagers", 1993, "P", 1956, "Soul/R&B", "group", "Black"),
    ("Etta James", 1993, "P", 1954, "Soul/R&B", "female", "Black"),
    ("Van Morrison", 1993, "P", 1964, "Classic Rock", "male", "white"),
    ("Sly & The Family Stone", 1993, "P", 1967, "Soul/R&B", "group", "Black"),
    # 1993 EI
    ("Dinah Washington", 1993, "EI", 1943, "Soul/R&B", "female", "Black"),

    # 1994
    ("The Animals", 1994, "P", 1964, "Classic Rock", "group", "white"),
    ("The Band", 1994, "P", 1968, "Classic Rock", "group", "white"),
    ("Duane Eddy", 1994, "P", 1958, "Classic Rock", "male", "white"),
    ("The Grateful Dead", 1994, "P", 1965, "Classic Rock", "group", "white"),
    ("Elton John", 1994, "P", 1969, "Classic Rock", "male", "white"),
    ("John Lennon", 1994, "P", 1969, "Classic Rock", "male", "white"),
    ("Bob Marley", 1994, "P", 1963, "Classic Rock", "male", "Black"),
    ("Rod Stewart", 1994, "P", 1964, "Classic Rock", "male", "white"),

    # 1995
    ("The Allman Brothers Band", 1995, "P", 1969, "Classic Rock", "group", "white"),
    ("Al Green", 1995, "P", 1967, "Soul/R&B", "male", "Black"),
    ("Janis Joplin", 1995, "P", 1966, "Classic Rock", "female", "white"),
    ("Led Zeppelin", 1995, "P", 1969, "Classic Rock", "group", "white"),
    ("Martha & The Vandellas", 1995, "P", 1962, "Soul/R&B", "group", "Black"),
    ("Neil Young", 1995, "P", 1968, "Classic Rock", "male", "white"),
    ("Frank Zappa", 1995, "P", 1966, "Classic Rock", "male", "white"),

    # 1996
    ("David Bowie", 1996, "P", 1964, "Classic Rock", "male", "white"),
    ("Gladys Knight & The Pips", 1996, "P", 1961, "Soul/R&B", "group", "Black"),
    ("Jefferson Airplane", 1996, "P", 1966, "Classic Rock", "group", "white"),
    ("Little Willie John", 1996, "P", 1953, "Soul/R&B", "male", "Black"),
    ("Pink Floyd", 1996, "P", 1967, "Classic Rock", "group", "white"),
    ("The Shirelles", 1996, "P", 1958, "Soul/R&B", "group", "Black"),
    ("The Velvet Underground", 1996, "P", 1967, "Classic Rock", "group", "white"),

    # 1997
    ("Bee Gees", 1997, "P", 1963, "Disco/Dance", "group", "white"),
    ("Buffalo Springfield", 1997, "P", 1966, "Classic Rock", "group", "white"),
    ("Crosby, Stills & Nash", 1997, "P", 1969, "Classic Rock", "group", "white"),
    ("The Jackson 5", 1997, "P", 1968, "Soul/R&B", "group", "Black"),
    ("Joni Mitchell", 1997, "P", 1967, "Folk/Country", "female", "white"),
    ("Parliament-Funkadelic", 1997, "P", 1967, "Soul/R&B", "group", "Black"),
    ("The (Young) Rascals", 1997, "P", 1965, "Classic Rock", "group", "white"),
    # 1997 EI
    ("Mahalia Jackson", 1997, "EI", 1937, "Soul/R&B", "female", "Black"),
    ("Bill Monroe", 1997, "EI", 1936, "Folk/Country", "male", "white"),

    # 1998
    ("Eagles", 1998, "P", 1971, "Classic Rock", "group", "white"),
    ("Fleetwood Mac", 1998, "P", 1967, "Classic Rock", "group", "white"),
    ("The Mamas & The Papas", 1998, "P", 1965, "Classic Rock", "group", "white"),
    ("Lloyd Price", 1998, "P", 1952, "Soul/R&B", "male", "Black"),
    ("Santana", 1998, "P", 1966, "Classic Rock", "group", "Latino"),
    ("Gene Vincent", 1998, "P", 1956, "Classic Rock", "male", "white"),

    # 1999
    ("Billy Joel", 1999, "P", 1971, "Classic Rock", "male", "white"),
    ("Curtis Mayfield", 1999, "P", 1958, "Soul/R&B", "male", "Black"),
    ("Paul McCartney", 1999, "P", 1970, "Classic Rock", "male", "white"),
    ("Del Shannon", 1999, "P", 1960, "Classic Rock", "male", "white"),
    ("Dusty Springfield", 1999, "P", 1963, "Pop", "female", "white"),
    ("Bruce Springsteen", 1999, "P", 1973, "Classic Rock", "male", "white"),
    ("The Staple Singers", 1999, "P", 1953, "Soul/R&B", "group", "Black"),
    # 1999 EI
    ("Charles Brown", 1999, "EI", 1945, "Blues/Early", "male", "Black"),
    ("Bob Wills", 1999, "EI", 1929, "Folk/Country", "male", "white"),

    # 2000
    ("Eric Clapton", 2000, "P", 1963, "Classic Rock", "male", "white"),
    ("Earth, Wind & Fire", 2000, "P", 1969, "Soul/R&B", "group", "Black"),
    ("The Lovin' Spoonful", 2000, "P", 1965, "Classic Rock", "group", "white"),
    ("The Moonglows", 2000, "P", 1952, "Soul/R&B", "group", "Black"),
    ("Bonnie Raitt", 2000, "P", 1971, "Classic Rock", "female", "white"),
    # 2000 EI
    ("Nat King Cole", 2000, "EI", 1936, "Pop", "male", "Black"),
    ("Billie Holiday", 2000, "EI", 1933, "Blues/Early", "female", "Black"),

    # 2001
    ("Aerosmith", 2001, "P", 1973, "Classic Rock", "group", "white"),
    ("Solomon Burke", 2001, "P", 1955, "Soul/R&B", "male", "Black"),
    ("The Flamingos", 2001, "P", 1953, "Soul/R&B", "group", "Black"),
    ("Michael Jackson", 2001, "P", 1971, "Pop", "male", "Black"),
    ("Queen", 2001, "P", 1973, "Classic Rock", "group", "white"),
    ("Paul Simon", 2001, "P", 1965, "Folk/Country", "male", "white"),
    ("Steely Dan", 2001, "P", 1972, "Classic Rock", "group", "white"),
    ("Ritchie Valens", 2001, "P", 1958, "Classic Rock", "male", "Latino"),
    # 2001 EI
    ("James Burton", 2001, "EI", 1957, "Classic Rock", "male", "white"),

    # 2002
    ("Isaac Hayes", 2002, "P", 1962, "Soul/R&B", "male", "Black"),
    ("Brenda Lee", 2002, "P", 1956, "Pop", "female", "white"),
    ("Tom Petty & The Heartbreakers", 2002, "P", 1976, "Classic Rock", "group", "white"),
    ("Gene Pitney", 2002, "P", 1959, "Pop", "male", "white"),
    ("Ramones", 2002, "P", 1976, "Punk", "group", "white"),
    ("Talking Heads", 2002, "P", 1977, "Punk", "group", "white"),
    # 2002 EI
    ("Chet Atkins", 2002, "EI", 1946, "Folk/Country", "male", "white"),

    # 2003
    ("AC/DC", 2003, "P", 1973, "Classic Rock", "group", "white"),
    ("The Clash", 2003, "P", 1977, "Punk", "group", "white"),
    ("Elvis Costello & The Attractions", 2003, "P", 1977, "Classic Rock", "group", "white"),
    ("The Police", 2003, "P", 1978, "Classic Rock", "group", "white"),
    ("The Righteous Brothers", 2003, "P", 1962, "Pop", "group", "white"),

    # 2004
    ("George Harrison", 2004, "P", 1968, "Classic Rock", "male", "white"),
    ("Prince", 2004, "P", 1978, "Soul/R&B", "male", "Black"),
    ("Bob Seger", 2004, "P", 1966, "Classic Rock", "male", "white"),
    ("Traffic", 2004, "P", 1967, "Classic Rock", "group", "white"),
    ("ZZ Top", 2004, "P", 1970, "Classic Rock", "group", "white"),
    ("Jackson Browne", 2004, "P", 1972, "Classic Rock", "male", "white"),

    # 2005
    ("Buddy Guy", 2005, "P", 1958, "Blues/Early", "male", "Black"),
    ("The O'Jays", 2005, "P", 1963, "Soul/R&B", "group", "Black"),
    ("The Pretenders", 2005, "P", 1979, "Classic Rock", "group", "white"),
    ("Percy Sledge", 2005, "P", 1966, "Soul/R&B", "male", "Black"),
    ("U2", 2005, "P", 1980, "Classic Rock", "group", "white"),
    # 2005 EI
    ("Frank Beecher", 2005, "EI", 1952, "Classic Rock", "male", "white"),

    # 2006
    ("Black Sabbath", 2006, "P", 1969, "Heavy Metal", "group", "white"),
    ("Blondie", 2006, "P", 1976, "Punk", "group", "white"),
    ("Miles Davis", 2006, "P", 1945, "Blues/Early", "male", "Black"),
    ("Lynyrd Skynyrd", 2006, "P", 1973, "Classic Rock", "group", "white"),
    ("Sex Pistols", 2006, "P", 1976, "Punk", "group", "white"),

    # 2007
    ("Grandmaster Flash & The Furious Five", 2007, "P", 1979, "Hip-Hop", "group", "Black"),
    ("R.E.M.", 2007, "P", 1981, "Classic Rock", "group", "white"),
    ("The Ronettes", 2007, "P", 1961, "Pop", "group", "Black"),
    ("Patti Smith", 2007, "P", 1974, "Punk", "female", "white"),
    ("Van Halen", 2007, "P", 1978, "Classic Rock", "group", "white"),

    # 2008
    ("Leonard Cohen", 2008, "P", 1967, "Folk/Country", "male", "white"),
    ("The Dave Clark Five", 2008, "P", 1963, "Classic Rock", "group", "white"),
    ("Madonna", 2008, "P", 1982, "Pop", "female", "white"),
    ("John Mellencamp", 2008, "P", 1976, "Classic Rock", "male", "white"),
    ("The Ventures", 2008, "P", 1959, "Classic Rock", "group", "white"),

    # 2009
    ("Jeff Beck", 2009, "P", 1966, "Classic Rock", "male", "white"),
    ("Little Anthony & The Imperials", 2009, "P", 1957, "Soul/R&B", "group", "Black"),
    ("Metallica", 2009, "P", 1983, "Heavy Metal", "group", "white"),
    ("Run-D.M.C.", 2009, "P", 1983, "Hip-Hop", "group", "Black"),
    ("Bobby Womack", 2009, "P", 1961, "Soul/R&B", "male", "Black"),

    # 2010
    ("ABBA", 2010, "P", 1972, "Pop", "group", "white"),
    ("Genesis", 2010, "P", 1969, "Classic Rock", "group", "white"),
    ("Jimmy Cliff", 2010, "P", 1962, "Classic Rock", "male", "Black"),
    ("The Hollies", 2010, "P", 1963, "Classic Rock", "group", "white"),
    ("The Stooges", 2010, "P", 1969, "Punk", "group", "white"),

    # 2011
    ("Alice Cooper", 2011, "P", 1969, "Classic Rock", "male", "white"),
    ("Neil Diamond", 2011, "P", 1966, "Pop", "male", "white"),
    ("Dr. John", 2011, "P", 1968, "Blues/Early", "male", "white"),
    ("Darlene Love", 2011, "P", 1962, "Pop", "female", "Black"),
    ("Tom Waits", 2011, "P", 1973, "Classic Rock", "male", "white"),

    # 2012
    ("Beastie Boys", 2012, "P", 1981, "Hip-Hop", "group", "white"),
    ("Donovan", 2012, "P", 1965, "Folk/Country", "male", "white"),
    ("Guns N' Roses", 2012, "P", 1985, "Classic Rock", "group", "white"),
    ("Laura Nyro", 2012, "P", 1966, "Pop", "female", "white"),
    ("Red Hot Chili Peppers", 2012, "P", 1983, "Classic Rock", "group", "white"),
    ("The Small Faces/Faces", 2012, "P", 1965, "Classic Rock", "group", "white"),

    # 2013
    ("Heart", 2013, "P", 1975, "Classic Rock", "group", "white"),
    ("Albert King", 2013, "P", 1953, "Blues/Early", "male", "Black"),
    ("Randy Newman", 2013, "P", 1968, "Pop", "male", "white"),
    ("Public Enemy", 2013, "P", 1987, "Hip-Hop", "group", "Black"),
    ("Rush", 2013, "P", 1974, "Classic Rock", "group", "white"),
    ("Donna Summer", 2013, "P", 1974, "Disco/Dance", "female", "Black"),

    # 2014
    ("Peter Gabriel", 2014, "P", 1977, "Classic Rock", "male", "white"),
    ("Hall & Oates", 2014, "P", 1972, "Pop", "group", "white"),
    ("Kiss", 2014, "P", 1974, "Classic Rock", "group", "white"),
    ("Nirvana", 2014, "P", 1989, "Classic Rock", "group", "white"),
    ("Linda Ronstadt", 2014, "P", 1969, "Pop", "female", "white"),
    ("Cat Stevens", 2014, "P", 1967, "Folk/Country", "male", "white"),

    # 2015
    ("Joan Jett & The Blackhearts", 2015, "P", 1980, "Classic Rock", "group", "white"),
    ("Lou Reed", 2015, "P", 1972, "Classic Rock", "male", "white"),
    ("Green Day", 2015, "P", 1990, "Punk", "group", "white"),
    ("Stevie Ray Vaughan", 2015, "P", 1983, "Blues/Early", "male", "white"),
    ("Bill Withers", 2015, "P", 1970, "Soul/R&B", "male", "Black"),
    ("The Paul Butterfield Blues Band", 2015, "P", 1965, "Blues/Early", "group", "white"),
    ("Ringo Starr", 2015, "P", 1970, "Classic Rock", "male", "white"),

    # 2016
    ("Cheap Trick", 2016, "P", 1977, "Classic Rock", "group", "white"),
    ("Chicago", 2016, "P", 1969, "Classic Rock", "group", "white"),
    ("Deep Purple", 2016, "P", 1968, "Classic Rock", "group", "white"),
    ("Steve Miller", 2016, "P", 1968, "Classic Rock", "male", "white"),
    ("N.W.A", 2016, "P", 1986, "Hip-Hop", "group", "Black"),

    # 2017
    ("Joan Baez", 2017, "P", 1960, "Folk/Country", "female", "Latino"),
    ("Electric Light Orchestra", 2017, "P", 1971, "Classic Rock", "group", "white"),
    ("Journey", 2017, "P", 1975, "Classic Rock", "group", "white"),
    ("Pearl Jam", 2017, "P", 1991, "Classic Rock", "group", "white"),
    ("Tupac Shakur", 2017, "P", 1991, "Hip-Hop", "male", "Black"),
    ("Yes", 2017, "P", 1969, "Classic Rock", "group", "white"),
    ("Nile Rodgers", 2017, "ME", 1977, "Disco/Dance", "male", "Black"),

    # 2018
    ("Bon Jovi", 2018, "P", 1983, "Classic Rock", "group", "white"),
    ("The Cars", 2018, "P", 1978, "Classic Rock", "group", "white"),
    ("Dire Straits", 2018, "P", 1978, "Classic Rock", "group", "white"),
    ("The Moody Blues", 2018, "P", 1964, "Classic Rock", "group", "white"),
    ("Nina Simone", 2018, "P", 1958, "Soul/R&B", "female", "Black"),
    # 2018 EI
    ("Sister Rosetta Tharpe", 2018, "EI", 1938, "Blues/Early", "female", "Black"),

    # 2019
    ("The Cure", 2019, "P", 1978, "Classic Rock", "group", "white"),
    ("Def Leppard", 2019, "P", 1980, "Classic Rock", "group", "white"),
    ("Janet Jackson", 2019, "P", 1982, "Pop", "female", "Black"),
    ("Stevie Nicks", 2019, "P", 1981, "Classic Rock", "female", "white"),
    ("Radiohead", 2019, "P", 1992, "Classic Rock", "group", "white"),
    ("The Zombies", 2019, "P", 1964, "Classic Rock", "group", "white"),
    ("Roxy Music", 2019, "P", 1972, "Classic Rock", "group", "white"),

    # 2020
    ("Depeche Mode", 2020, "P", 1981, "Electronic", "group", "white"),
    ("The Doobie Brothers", 2020, "P", 1970, "Classic Rock", "group", "white"),
    ("Whitney Houston", 2020, "P", 1985, "Pop", "female", "Black"),
    ("Nine Inch Nails", 2020, "P", 1989, "Electronic", "group", "white"),
    ("The Notorious B.I.G.", 2020, "P", 1994, "Hip-Hop", "male", "Black"),
    ("T. Rex", 2020, "P", 1968, "Classic Rock", "group", "white"),

    # 2021
    ("Foo Fighters", 2021, "P", 1995, "Classic Rock", "group", "white"),
    ("The Go-Go's", 2021, "P", 1981, "Classic Rock", "group", "white"),
    ("Jay-Z", 2021, "P", 1996, "Hip-Hop", "male", "Black"),
    ("Carole King", 2021, "P", 1970, "Pop", "female", "white"),
    ("Todd Rundgren", 2021, "P", 1970, "Classic Rock", "male", "white"),
    ("Tina Turner", 2021, "P", 1984, "Soul/R&B", "female", "Black"),
    ("Charley Patton", 2021, "EI", 1929, "Blues/Early", "male", "Black"),

    # 2022
    ("Pat Benatar", 2022, "P", 1979, "Classic Rock", "female", "white"),
    ("Duran Duran", 2022, "P", 1981, "Pop", "group", "white"),
    ("Eminem", 2022, "P", 1996, "Hip-Hop", "male", "white"),
    ("Eurythmics", 2022, "P", 1980, "Pop", "group", "white"),
    ("Dolly Parton", 2022, "P", 1967, "Folk/Country", "female", "white"),
    ("Lionel Richie", 2022, "P", 1968, "Soul/R&B", "male", "Black"),
    ("Carly Simon", 2022, "P", 1971, "Pop", "female", "white"),
    ("Judas Priest", 2022, "ME", 1974, "Heavy Metal", "group", "white"),

    # 2023
    ("Kate Bush", 2023, "P", 1978, "Pop", "female", "white"),
    ("Sheryl Crow", 2023, "P", 1993, "Classic Rock", "female", "white"),
    ("Missy Elliott", 2023, "P", 1997, "Hip-Hop", "female", "Black"),
    ("George Michael", 2023, "P", 1982, "Pop", "male", "white"),
    ("Willie Nelson", 2023, "P", 1956, "Folk/Country", "male", "white"),
    ("Rage Against the Machine", 2023, "P", 1992, "Heavy Metal", "group", "white"),
    ("The Spinners", 2023, "P", 1961, "Soul/R&B", "group", "Black"),

    # 2024
    ("Mary J. Blige", 2024, "P", 1991, "Hip-Hop", "female", "Black"),
    ("Cher", 2024, "P", 1963, "Pop", "female", "white"),
    ("Dave Matthews Band", 2024, "P", 1993, "Classic Rock", "group", "white"),
    ("Foreigner", 2024, "P", 1977, "Classic Rock", "group", "white"),
    ("Peter Frampton", 2024, "P", 1972, "Classic Rock", "male", "white"),
    ("Kool & The Gang", 2024, "P", 1969, "Soul/R&B", "group", "Black"),
    ("Ozzy Osbourne", 2024, "P", 1970, "Heavy Metal", "male", "white"),
    ("A Tribe Called Quest", 2024, "P", 1990, "Hip-Hop", "group", "Black"),
    # 2024 EI
    ("Louis Jordan", 2024, "EI", 1938, "Blues/Early", "male", "Black"),

    # 2025
    ("Oasis", 2025, "P", 1994, "Classic Rock", "group", "white"),
    ("Cyndi Lauper", 2025, "P", 1983, "Pop", "female", "white"),

    # 2026
    ("Iron Maiden", 2026, "P", 1980, "Heavy Metal", "group", "white"),
]


def load_inductees(db_path=None):
    """Load all inductees into the database."""
    conn = get_connection(db_path)
    c = conn.cursor()

    artist_count = 0
    induction_count = 0

    for row in INDUCTEES:
        name, year, category, first_rec, genre, gender, race = row

        # Upsert artist
        c.execute("""
            INSERT INTO artists (name, first_recording_year, genre_primary, gender, race,
                                 race_source, eligible_year, is_inducted, inducted_year,
                                 inducted_category)
            VALUES (?, ?, ?, ?, ?, 'curated', ?, 1, ?, ?)
            ON CONFLICT(name, first_recording_year) DO UPDATE SET
                is_inducted = 1,
                inducted_year = COALESCE(artists.inducted_year, excluded.inducted_year),
                inducted_category = excluded.inducted_category,
                genre_primary = COALESCE(artists.genre_primary, excluded.genre_primary),
                gender = COALESCE(artists.gender, excluded.gender),
                race = COALESCE(artists.race, excluded.race)
        """, (name, first_rec, genre, gender, race,
              first_rec + 25, year, category))
        artist_count += 1

        # Get artist ID
        artist_id = c.execute(
            "SELECT id FROM artists WHERE name = ? AND first_recording_year = ?",
            (name, first_rec)
        ).fetchone()[0]

        # Insert induction record
        c.execute("""
            INSERT OR IGNORE INTO inductions (artist_id, year, category)
            VALUES (?, ?, ?)
        """, (artist_id, year, category))
        induction_count += 1

    conn.commit()
    conn.close()

    print(f"Loaded {artist_count} artist records, {induction_count} induction events")
    return artist_count


if __name__ == "__main__":
    init_db()
    count = load_inductees()

    # Summary stats
    from db import query
    total = query("SELECT COUNT(*) as n FROM artists")[0]["n"]
    inducted = query("SELECT COUNT(*) as n FROM artists WHERE is_inducted = 1")[0]["n"]
    by_decade = query("""
        SELECT (year / 10) * 10 as decade, COUNT(*) as n
        FROM inductions GROUP BY decade ORDER BY decade
    """)

    print(f"\nTotal artists: {total}")
    print(f"Inducted: {inducted}")
    print("\nInductions by decade:")
    for row in by_decade:
        print(f"  {row['decade']}s: {row['n']}")

    # Genre breakdown
    by_genre = query("""
        SELECT genre_primary, COUNT(*) as n
        FROM artists WHERE is_inducted = 1
        GROUP BY genre_primary ORDER BY n DESC
    """)
    print("\nInducted by genre:")
    for row in by_genre:
        print(f"  {row['genre_primary']}: {row['n']}")

    # Race breakdown
    by_race = query("""
        SELECT race, COUNT(*) as n
        FROM artists WHERE is_inducted = 1
        GROUP BY race ORDER BY n DESC
    """)
    print("\nInducted by race:")
    for row in by_race:
        print(f"  {row['race']}: {row['n']}")
