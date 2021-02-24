"""
TODO:
- Properly configure app for deployment
- Fix any security shit with file paths
- Periodically remove files from uploads and downloads (without annoying users)

- Allow numerous uploads in html
- CSS shit

- Could maybe encrypt PDF's ?

- maybe write a test/build script that includes something like this:
    find -name "*.pdf" -exec rm {} \;
    BUT with a directory specified so you don't accidentally delete all your PDF's on your computer

Lot's of help from here:
https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
"""

from app import app
