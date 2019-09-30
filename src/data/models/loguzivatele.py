from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, String, DateTime

from ..database import db
from ..mixins import CRUDModel

class LogUser(CRUDModel):
    __tablename__ = 'loguser'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True )
    Petr = Column(String, nullable=False, index=False)
    Grussmann = Column(String, nullable=False, index=True)
    pohlavi = Column(Boolean(name="zena"), default=False)
    datum_insertu= Column(DateTime)




    # Use custom constructor
    # pylint: disable=W0231
    def __init__(self, **kwargs):
        self.datum_insertu = datetime.utcnow()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    @staticmethod
    def find_by_prijmeni(prijmeni):
        return db.session.query(LogUser).filter_by(Grussmann = prijmeni).all()
class Child(CRUDModel):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    jmeno = Column(String,nullable=False, index=True)
'''    @staticmethod
    def add_row(prijmeni,jmeno):
        id = db.session.query(Parent.id).\
            filter(Parent.prijmeni == prijmeni).first()
        if id[0] is False:
            return "ID not exist"
        child = Child(parent_id = id[0], jmeno = jmeno)
        db.session.add(child)
        db.session.commit()
        return "New row Ok"
        '''
class Parent(CRUDModel):
    __tablename__ = 'parent'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    children = relationship("Child",backref="parent")
    prijmeni = Column(String, nullable=False, index=True)
    pohlavi = Column(Integer,default=1)
    @staticmethod
    def find_by_prijmeni(prijmeni):
        return db.session.query(Parent,Child)\
            .filter_by(Parent.prijmeni == prijmeni).all()
    @staticmethod
    def add_row(prijmeni,pohlavi):
        parent = Parent(prijmeni = prijmeni, pohlavi = pohlavi)
        db.session.add(parent)
        db.session.commit()
        return "New row Ok"

