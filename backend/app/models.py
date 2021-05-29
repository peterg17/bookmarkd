from app import db


class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    url = db.Column(db.String(300))
    chrome_id = db.Column(db.Integer)
    date_added = db.Column(db.BigInteger)

    def __repr__(self):
        return "<Bookmark %r>" % self.url


