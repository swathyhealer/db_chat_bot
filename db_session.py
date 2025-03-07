
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base
# Create SQLite database
engine = create_engine('sqlite:///invoices5623.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()