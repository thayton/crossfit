#!/bin/sh

sqlite3 scraper/db.sqlite3 <<EOF
select * from crossfit_scraper_crossfitgym where email != '';
EOF

