from flask import jsonify, request, g, url_for, current_app
from . import API
from .. import db, models
import logging
import json


# set up logging
logging.basicConfig(format="[%(filename)s:%(lineno)d]\t %(message)s")
log = logging.getLogger(__name__)
log.setLevel("INFO")


@API.route("/bookmarks", methods=["POST"])
def upload_bookmarks():
    log.info("\n\n-----------------------------------------")
    log.info("Uploading Bookmarks\n")
    # formKeys = request.form.keys()
    # file_name = request.form["filename"]
    json_data = request.json
    # bookmarks_lst = json.loads(json_data)
    # log.info("request json is: " + str(json_data))
    log.info("bookmarks array has %d bookmarks" % len(json_data))
    for i in range(10):
        log.info(json_data[i])

    for i in range(len(json_data)):
        bookmark = json_data[i]
        bookmark_json = {}
        if "url" not in bookmark:
            continue
        url = bookmark["url"]
        id = int(bookmark["id"])
        title = bookmark["title"]
        bookmark_row = models.Bookmark(title=title, url=url, chrome_id=id)
        db.session.add(bookmark_row)
    db.session.commit()

    # log.info("file name is: " + json_data["filename"])
    # file_type = request.form["filetype"]
    # file_text = request.form["filedata"]
    return jsonify(success=True)