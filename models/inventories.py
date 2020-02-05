from main import db
from models.sales import  Sales


class Inventories(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String, nullable=False)
    # buying_price = db.Column(db.Integer, nullable=False)
    #
    #
    # sales = db.relationship('Sales', backref='inventory', lazy=True)

    __tablename__ = 'inventories'
    __table_args__ = {'extend_existing': True}
    # to add columns,use your sqlalchemy object to get the column class that'll help you define your columns
    id = db.Column(db.Integer, primary_key=True)  # research on additional objects you can pass in the column id
    inv_name = db.Column(db.String, nullable=False)
    inv_type = db.Column(db.String, nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    sales = db.relationship("Sales", backref="inventory", lazy=True)



    def add_records(self):
        db.session.add(self)
        db.session.commit()

    # Fetch all reords
    @classmethod
    def fetch_all_records(cls):
        return cls.query.all()

    #fetch one record
    @classmethod
    def fetch_one_record(cls,id):
        return cls.query.filter_by(id=id).first()