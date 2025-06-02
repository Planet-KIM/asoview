from . import db

class TaskRun(db.Model):
    __tablename__ = "task_run"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(50), index=True, unique=True)
    user_name = db.Column(db.String(100), index=True, nullable=False)
    status = db.Column(db.String(20))  # PENDING / STARTED / SUCCESS / FAILURE
    args_json = db.Column(db.Text)
    args_hash = db.Column(db.String(64), index=True, nullable=False)
    result_json = db.Column(db.Text)
    started_at = db.Column(db.DateTime(timezone=True))
    finished_at = db.Column(db.DateTime(timezone=True))
    elapsed_sec = db.Column(db.Float)
    asodesign_link = db.Column(db.String(256), index=True)

    __table_args__ = (
        db.UniqueConstraint("args_hash", name="uq_taskrun_args"),
    )

'''
class TaskRun(db.Model):
    __tablename__ = "task_run"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(50), index=True, unique=True)
    status = db.Column(db.String(20))  # PENDING / STARTED / SUCCESS / FAILURE
    args_json = db.Column(db.Text)
    result_json = db.Column(db.Text)
    started_at = db.Column(db.DateTime(timezone=True))
    finished_at = db.Column(db.DateTime(timezone=True))
    elapsed_sec = db.Column(db.Float)
'''