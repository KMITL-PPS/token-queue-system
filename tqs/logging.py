import logging
import traceback

from tqs import app, db
from tqs.models import Log


class SQLAlchemyHandler(logging.StreamHandler):
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            message=record.__dict__['msg'],)
        db.session.add(log)
        db.session.commit()


if app.debug:
    app.logger.handlers[0].setLevel(logging.DEBUG)
else:
    app.logger.handlers[0].setLevel(logging.WARNING)

db_handler = SQLAlchemyHandler()
db_handler.setLevel(logging.INFO)

app.logger.addHandler(db_handler)
