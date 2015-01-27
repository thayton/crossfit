#!/bin/sh

sqlite3 scraper/db.sqlite3 <<EOF
.mode csv
select name,link,addr,phone,email from crossfit_scraper_crossfitgym where email != '';
EOF

