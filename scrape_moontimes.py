"""
A small script to scrape the moon phase times (GMT) for a given number of years
between 2001 and 2025.

If you need other years, check out the site at the URL below and checkout the
links. The data is nearly the same, but there is a delta column that will need
to be parsed/handled in parse_text() for this script to work. 98% of the work is
there, but it is no use to me...
"""
__author__ = "Lyle Scott, III <lyle@digitalfoo.net>"


from lxml import html
from datetime import datetime


# The years to get moon phase times for.
# MIN: 2001, # MAX: 2025
YEARS = range(2013, 2025+1)

# The date format used in the HTML document.
DATEFMT = '%Y %b %d %H:%M'

# The xpath path used to find the year moon phases.
DATEXPATH = '//span[@class="prehead"]/following-sibling::text()[contains(., "%s")]'

# The URL containing the moon phase data.
URL = 'http://eclipse.gsfc.nasa.gov/phase/phase2001gmt.html'

# A mapping to make the phase human readable.
PHASE_MAP = {
    0: 'NEW',
    1: 'FSQ',
    2: 'FUL',
    3: 'LSQ',
}

CLEAN_THINGS = ('T', 'A', 'H', 'P', 't', 'p', 'n')

def chunk_at_n(split_text, chunk_size):
    """Chunk together items of a sequence by chunk_size."""
    for i in xrange(0, len(split_text), chunk_size):
        yield split_text[i:i + chunk_size]


def cleanup(node, year):
    """Clean up some notes in the file depicting eclipse types."""
    text = node[0].replace(str(year), '').strip()
    for thing in CLEAN_THINGS:
        text = text.replace(' %s ' % thing, '   ')
    if text[-1] in CLEAN_THINGS:
        text = text[:-1]
    return text


def parse_text(text, year):
    """Parse the text into date objects and moon phases."""
    for row in text.split('\n'):
        chunks = list(chunk_at_n(row.split(), 3))
        chunks_len = len(chunks)
        for i, chunk in enumerate(chunks):
            datestr = '%s %s' % (year, ' '.join(chunk))
            dateobj = datetime.strptime(datestr, DATEFMT)
            i = (4 - chunks_len) + i
            yield (dateobj, PHASE_MAP[i])


def process(dates_with_phases):
    """Do something with the data. Insert your funkiness here..."""
    for phase, date_ in dates_with_phases:
        print phase, date_


def run():
    """Do work."""
    doc = html.parse(URL)
    for year in YEARS:
        node = doc.xpath(DATEXPATH % year)
        text = cleanup(node, year)
        dates_with_phases = parse_text(text, year)
        process(dates_with_phases)


if __name__ == '__main__':
    run()
