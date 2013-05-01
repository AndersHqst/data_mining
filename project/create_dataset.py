from os import listdir
from os.path import isfile, join
from database_writer import DatabaseWriter, TestDatabaseWriter
from website import Website
from website_analyzer import analyze
from scanners import *

# Settings
website_dir = 'top_sites'
db_connection_string = """host='web331.webfaction.com' dbname='datamining' user='datamining_admin' password='P@ssword'"""
db_table = 'dataset'

scanners = [
    url_scanner,
    image_count_scanner,
    external_links_scanner,
    internal_links_scanner,
    title_scanner,
    cms_scanner,
    description_scanner,
    keyword_scanner
]

# Get all websites
files_names = [join(website_dir,fn) for fn in listdir(website_dir) if isfile(join(website_dir,fn))]
websites = []
for fn in files_names[:4]:
    print fn
    with open(fn) as f:
        website = Website(f)
        websites.append(website)

# Scan attributes
attribute_rows = []
for website in websites:
    attributes = analyze(website, scanners)
    attribute_rows.append(attributes)
    print 'Analyzed: %s' % website.url

# Write to database
writer = TestDatabaseWriter(db_connection_string, db_table)
writer.connect()

for attributes in attribute_rows:
    writer.write_row(attributes)

writer.commit()
writer.disconnect()

