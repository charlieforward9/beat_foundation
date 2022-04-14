"""This is a huge mess of a file. Dont try to fix it... Use the original file, link below."""

"""  SOURCES
applehealthdata.py: Extract data from Apple Health App's export.xml.
Copyright (c) 2016 Nicholas J. Radcliffe
Licence: MIT

https://medium.com/@bobbie.wxy/how-to-convert-calendar-ics-to-csv-excel-using-python-3-steps-ca3903530aa3
http://www.markwk.com/data-analysis-for-apple-health.html
"""
from operator import truediv
import os
import re
import sys
import random
from time import time
from xml.etree import ElementTree
from collections import Counter, OrderedDict
from datetime import date, datetime, timedelta
from pytz import UTC, timezone   # timezone
from csv_ical import Convert
from dateutil.rrule import rrule, rrulestr

FREQNAMES = ['YEARLY', 'MONTHLY', 'WEEKLY',
             'DAILY', 'HOURLY', 'MINUTELY', 'SECONDLY']

(YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY) = list(range(7))
(MO, TU, WE, TH, FR, SA, SU) = list(range(7))


__version__ = '420'

#User ID values, used to populate csv with proper IDs
CHARBOID = str(0.8302870117189518)
CAMID    = str(0.26777655249889387)

#Commented out irrelevant attr
RECORD_FIELDS = OrderedDict((
    #('sourceName', 's'),
    #('sourceVersion', 's'),
    ('device', 's'),
    #('type', 's'),
    #('unit', 's'),
    #('creationDate', 'd'),
    ('startDate', 'd'),
    #('endDate', 'd'),
    ('value', 'n'),
))

ACTIVITY_SUMMARY_FIELDS = OrderedDict((
    ('dateComponents', 'd'),
    ('activeEnergyBurned', 'n'),
    ('activeEnergyBurnedGoal', 'n'),
    ('activeEnergyBurnedUnit', 's'),
    ('appleExerciseTime', 's'),
    ('appleExerciseTimeGoal', 's'),
    ('appleStandHours', 'n'),
    ('appleStandHoursGoal', 'n'),
))

WORKOUT_FIELDS = OrderedDict((
    ('sourceName', 's'),
    ('sourceVersion', 's'),
    ('device', 's'),
    ('creationDate', 'd'),
    ('startDate', 'd'),
    ('endDate', 'd'),
    ('workoutActivityType', 's'),
    ('duration', 'n'),
    ('durationUnit', 's'),
    ('totalDistance', 'n'),
    ('totalDistanceUnit', 's'),
    ('totalEnergyBurned', 'n'),
    ('totalEnergyBurnedUnit', 's'),
))

FIELDS = {
    'Record': RECORD_FIELDS,
    'ActivitySummary': ACTIVITY_SUMMARY_FIELDS,
    'Workout': WORKOUT_FIELDS,
}

CATS = [
    "fitness",
    "rest",
    "work",
    "social",
    "eating",
    "other"]

DAYS = ['MO','TU','WE','TH','FR','SA','SU']

PREFIX_RE = re.compile('^HK.*TypeIdentifier(.+)$')
ABBREVIATE = True
VERBOSE = False

#User ID values, used to populate csv with proper IDs
RAND = str(random.random()) # Randomly generate a float for deviceID
CHARBOID = str(0.8302870117189518)
CAMID    = str(0.26777655249889387)


def format_freqs(counter):
    """
    Format a counter object for display.
    """
    return '\n'.join('%s: %d' % (tag, counter[tag])
                     for tag in sorted(counter.keys()))


def format_value(value, datatype):
    """
    Format a value for a CSV file, escaping double quotes and backslashes.
    None maps to randomly generated float in interval [0,1], converted to a string.
    datatype should be
        's' for string (escaped)
        'n' for number
        'd' for datetime
    """
    if value is None or datatype == 's':  # DeviceID should be a randomized float (use RAND if new user)
        return CAMID
    # elif datatype == 's':  # string
    #    return '"%s"' % value.replace('\\', '\\\\').replace('"', '\\"')
    elif datatype == 'n':
        # number (round to nearest int and convert back to string)
        return str(round(float(value)))
    elif datatype == 'd':  # date
        return value[0:19]
    else:
        raise KeyError('Unexpected format value: %s' % datatype)


def abbreviate(s, enabled=ABBREVIATE):
    """
    Abbreviate particularly verbose strings based on a regular expression
    """
    m = re.match(PREFIX_RE, s)
    return m.group(1) if enabled and m else s


class HealthDataExtractor(object):
    """
    Extract health data from Apple Health App's XML export, export.xml.
    Inputs:
        path:      Relative or absolute path to export.xml
        verbose:   Set to False for less verbose output
    Outputs:
        Writes a CSV file for each record type found, in the same
        directory as the input export.xml. Reports each file written
        unless verbose has been set to False.
    """

    def __init__(self, path, verbose=VERBOSE):
        self.in_path = path
        self.verbose = verbose
        self.directory = os.path.abspath(os.path.split(path)[0])
        with open(path) as f:
            self.report('Reading data from %s . . . ' % path, end='')
            self.data = ElementTree.parse(f)
            self.report('done')
        self.root = self.data._root
        self.nodes = list(self.root)
        self.n_nodes = len(self.nodes)
        self.abbreviate_types()
        self.collect_stats()

    def report(self, msg, end='\n'):
        if self.verbose:
            print(msg, end=end)
            sys.stdout.flush()

    def count_tags_and_fields(self):
        self.tags = Counter()
        self.fields = Counter()
        for record in self.nodes:
            self.tags[record.tag] += 1
            for k in record.keys():
                self.fields[k] += 1

    def count_record_types(self):
        """
        Counts occurrences of each type of (conceptual) "record" in the data.
        In the case of nodes of type 'Record', this counts the number of
        occurrences of each 'type' or record in self.record_types.
        In the case of nodes of type 'ActivitySummary' and 'Workout',
        it just counts those in self.other_types.
        The slightly different handling reflects the fact that 'Record'
        nodes come in a variety of different subtypes that we want to write
        to different data files, whereas (for now) we are going to write
        all Workout entries to a single file, and all ActivitySummary
        entries to another single file.
        """
        self.record_types = Counter()
        self.other_types = Counter()
        for record in self.nodes:
            if record.tag == 'Record':
                self.record_types[record.attrib['type']] += 1
            elif record.tag in ('ActivitySummary', 'Workout'):
                self.other_types[record.tag] += 1
            elif record.tag in ('Export', 'Me'):
                pass
            else:
                self.report('Unexpected node of type %s.' % record.tag)

    def collect_stats(self):
        self.count_record_types()
        self.count_tags_and_fields()

    def open_for_writing(self, user):
        self.handles = {}
        self.paths = []
        for kind in (list(self.record_types) + list(self.other_types)):
            # Only open what I need: Heart Rate
            if kind == "HeartRate":
                path = os.path.join(self.directory, user + '%s.csv' %
                                    abbreviate(kind))
                f = open(path, 'w')
                headerType = (kind if kind in ('Workout', 'ActivitySummary')
                              else 'Record')
                f.write(','.join(FIELDS[headerType].keys()) + '\n')
                self.handles[kind] = f
                self.report('Opening %s for writing' % path)

    def abbreviate_types(self):
        """
        Shorten types by removing common boilerplate text.
        """
        for node in self.nodes:
            if node.tag == 'Record':
                if 'type' in node.attrib:
                    node.attrib['type'] = abbreviate(node.attrib['type'])

    def write_records(self, user):
        kinds = FIELDS.keys()
        for node in self.nodes:
            if node.tag in kinds:
                attributes = node.attrib
                kind = attributes['type'] if node.tag == 'Record' else node.tag
                # Only write what I need: Heart Rate
                if kind == "HeartRate":
                    values = [format_value(attributes.get(field), datatype)
                              for (field, datatype) in FIELDS[node.tag].items()]
                    # Insert user name at beginning of line
                    line = ','.join(values) + '\n'
                    self.handles[kind].write(line)

    def close_files(self):
        for (kind, f) in self.handles.items():
            f.close()
            self.report('Written %s data.' % abbreviate(kind))

    def extract(self, user):
        self.open_for_writing(user)
        self.write_records(user)
        self.close_files()

    def report_stats(self):
        print('\nTags:\n%s\n' % format_freqs(self.tags))
        print('Fields:\n%s\n' % format_freqs(self.fields))
        print('Record types:\n%s\n' % format_freqs(self.record_types))


def parseHealthData(users):
    for user in users:
        f = user + ".xml"
        data = HealthDataExtractor(f)
        # data.report_stats()
        print("Extracting data from " + user + "'s file")
        data.extract(user)


def make_csv(self) -> None:

    """ Make CSV """
    ncount = 0
    tcount = 0
    for event in self.cal.subcomponents:
        tcount = tcount  + 1
        rdates = []
        byweekday = []
        duration = timedelta(hours=1)
        

        #print(event.get('SUMMARY'))
        if event.name != 'VEVENT':
            continue


        dtstart = ''
        if event.get('DTSTART'):
            dtstart = event.get('DTSTART').dt
            if isinstance(dtstart, date) and not isinstance(dtstart, datetime):
                #If missing a timestamp, make it midnight
                dtstart = str(datetime.combine(event.get('DTSTART').dt, datetime.min.time()))[0:19]
            else:
                dtstart = str(dtstart)[0:19]

           
        
        dtend = ''
        if event.get('DTEND'):
            dtend = event.get('DTEND').dt
            if isinstance(dtend, date) and not isinstance(dtend, datetime):
                #If missing a timestamp, make it midnight
                dtend = str(datetime.combine(event.get('DTEND').dt, datetime.min.time()))[0:19]
            else:
                dtend = str(dtend)[0:19]
        else:
            #No end date
            continue

        #Event duration for recurring events
        if dtstart != dtstart[0:10] and dtend != dtend[0:10]:
            start = datetime.strptime(dtstart,"%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(dtend,"%Y-%m-%d %H:%M:%S")
            duration = end - start
        
        if event.get('RRULE'):
            #Get all of the recurring dates, up to today
            rr = event.get('RRULE')

            if rr.get('FREQ'):
                f = rr.get('FREQ')[0]
                if f == "YEARLY":
                    f = YEARLY
                elif f == "MONTHLY":
                    f = MONTHLY
                elif f == "WEEKLY":
                    f = WEEKLY
                elif f == "DAILY":
                    f = DAILY
                elif f == "HOURLY":
                    f = HOURLY
                elif f == "MINUTELY":
                    f = MINUTELY
                elif f == "SECONDLY":
                    f = SECONDLY
                else:
                    print("ERROR")

            interval = rr.get('INTERVAL')[0] if rr.get('INTERVAL') else 1
            wkst = rr.get('WKST')[0] if rr.get('WKST') else None
            if wkst != 1:
                if wkst == DAYS[0]:
                    wkst = MO
                if wkst == DAYS[1]:
                    wkst = TU
                if wkst == DAYS[2]:
                    wkst = WE
                if wkst == DAYS[3]:
                    wkst = TH
                if wkst == DAYS[4]:
                    wkst = FR
                if wkst == DAYS[5]:
                    wkst = SA
                if wkst == DAYS[6]:
                    wkst = SU
            count = rr.get('COUNT')[0] if rr.get('COUNT') else None
            until = rr.get('UNTIL')[0] if rr.get('UNTIL') else datetime.today()
            if count is None and until is not None:
                #Until attribute sometimes has no time, it is added for consistency
                if isinstance(until, date):
                    until = datetime.combine(until, datetime.max.time())

            if rr.get('BYDAY'):
                for day in rr.get('BYDAY'):
                    if (day in DAYS):
                        if day == DAYS[0]:
                            day = MO
                        if day == DAYS[1]:
                            day = TU
                        if day == DAYS[2]:
                            day = WE
                        if day == DAYS[3]:
                            day = TH
                        if day == DAYS[4]:
                            day = FR
                        if day == DAYS[5]:
                            day = SA
                        if day == DAYS[6]:
                            day = SU
                        byweekday.append(day)
            recs = list(rrule(dtstart=start, freq=f, interval=interval, wkst=wkst, count=count, until=until, byweekday=byweekday))
            
        

            
            for r in recs:
                if r.date() < datetime.today().date():
                    #print(r)
                    rdates.append(r)
             
        #Find the categories in the calendar event
        #function getCategory()
        for cat in CATS:
            if cat in str(event.get('SUMMARY')).lower():
                if rdates is not None and len(rdates) > 0:
                    #All recurring events
                    for start in rdates:
                        end = start + duration
                        row = [
                            CHARBOID,
                            cat,
                            start, 
                            end
                        ]
                        row = [str(x) for x in row]
                        self.csv_data.append(row)
                        ncount = ncount + 1
                        
                else:
                    #All single time events
                    row = [
                            CHARBOID,
                            cat,
                            dtstart, 
                            dtend,
                        ]
                    row = [str(x) for x in row]
                    for data in self.csv_data: 
                        if str(data) == row:
                            continue
                    self.csv_data.append(row)
                    ncount = ncount + 1

    #Tentative total is 2360
    #New total 4037
    print(ncount)

def parseCalenderData(users):
    
    for user in users:
        convert = Convert()
        convert.CSV_FILE_LOCATION = user + 'Cal.csv'
        convert.SAVE_LOCATION = user + '.ics'
        convert.read_ical(convert.SAVE_LOCATION)
        make_csv(convert)
        convert.save_csv(convert.CSV_FILE_LOCATION)

    # https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python


#A temporary function to fix the issues encountered with the recurrring rule and primary key voilations
def removeDupes():
    with open('CamHeartRate.csv','r') as in_file, open('CamHR.csv','w') as out_file:
    
        seen = set() # set for fast O(1) amortized lookup
        
        for line in in_file:
            if line in seen: 
                continue # skip duplicate

            seen.add(line)
            out_file.write(line)

if __name__ == '__main__':
    #Put file names to parse in the user array
    users = ["CAM"]
    
    parseHealthData(users)
    #parseCalenderData(users)

    removeDupes()

    print("Data extracted")
