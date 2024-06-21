from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Tạo ra một engine kết nối đến cơ sở dữ liệu
engine = create_engine('sqlite:///patients.db')

# Tạo ra một session để thao tác với cơ sở dữ liệu
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Tạo ra một Base class để tạo ra các model class
Base = declarative_base()

# Gắn session vào Base class để có thể truy cập từ model class
Base.query = db_session.query_property()

# khởi tạo cơ sở dữ liệu
def init_db():
    Base.metadata.create_all(bind=engine)
