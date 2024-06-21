from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class BenhNhan(Base):
    __tablename__ = 'benh_nhan'
    ma_benh_nhan = Column(Integer, primary_key=True)
    ho_ten = Column(String)
    gioi_tinh = Column(String)
    nam_sinh = Column(Integer)
    dia_chi = Column(String)
    dien_thoai = Column(String)
    kham_benh = relationship("KhamBenh", back_populates="benh_nhan")

class KhamBenh(Base):
    __tablename__ = 'kham_benh'
    so_kham = Column(Integer, primary_key=True)
    ma_benh_nhan = Column(Integer, ForeignKey('benh_nhan.ma_benh_nhan'))
    ngay_kham = Column(Date)
    tong_tien = Column(Integer)
    benh_nhan = relationship("BenhNhan", back_populates="kham_benh")
