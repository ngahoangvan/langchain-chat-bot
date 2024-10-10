from sqlalchemy import (
    Boolean, Column, Float, ForeignKey, Integer, String,
    Table
)
from sqlalchemy.orm import relationship

from core.databases.db import Base
from core.enumerate import DatabaseSchema

# Association table for many-to-many relationship between Restaurant and PromotionGroup
restaurant_promotion_association = Table(
    'restaurant_promotion_association',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.restaurants.id')),
    Column('promotion_group_id', Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.promotion_groups.id')),
    schema=DatabaseSchema.SHOPEE.value
)

# Association table for Restaurant and ShippingMethod (many-to-many)
restaurant_shipping_association = Table(
    'restaurant_shipping_association',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.restaurants.id')),
    Column('shipping_method_id', Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.shipping_methods.id')),
    schema=DatabaseSchema.SHOPEE.value
)

class Rating(Base):
    __tablename__ = 'ratings'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    total_review = Column(Integer)
    avg = Column(Float)
    display_total_review = Column(String)
    app_link = Column(String)

    restaurant_id = Column(Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.restaurants.id'))


class Operating(Base):
    __tablename__ = 'operating_statuses'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    color = Column(String)
    close_time = Column(String)
    open_time = Column(String)
    resource_name = Column(String)

    restaurant_id = Column(Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.restaurants.id'))


class LabelPhoto(Base):
    __tablename__ = 'label_photos'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    width = Column(Integer)
    value = Column(String)
    height = Column(Integer)
    label_id = Column(Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.labels.id'))


class Label(Base):
    __tablename__ = 'labels'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    mms_img_id = Column(String)
    label_position = Column(Integer)
    
    photos = relationship('LabelPhoto', backref='label')
    restaurant_id = Column(Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.restaurants.id'))


class PromotionGroup(Base):
    __tablename__ = 'promotion_groups'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    group = Column(Integer)
    text = Column(String)
    browsing_icon = Column(String)
    mms_img_id = Column(String)
    discount_type = Column(Integer)


class Photo(Base):
    __tablename__ = 'photos'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    width = Column(Integer)
    value = Column(String)
    height = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.restaurants.id'))
    brand_id = Column(Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.brands.id'))


class Brand(Base):
    __tablename__ = 'brands'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer)
    name = Column(String)
    restaurant_count = Column(Integer)
    url_rewrite_name = Column(String)
    
    restaurant_id = Column(Integer, ForeignKey(f'{DatabaseSchema.SHOPEE.value}.restaurants.id'))
    photos = relationship('Photo', backref='brand')


class ShippingMethod(Base):
    __tablename__ = 'shipping_methods'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    method_id = Column(Integer)


class Restaurant(Base):
    __tablename__ = 'restaurants'
    __table_args__ = {'schema': DatabaseSchema.SHOPEE.value}

    id = Column(Integer, primary_key=True)
    total_order = Column(Integer)
    city_id = Column(Integer)
    restaurant_id = Column(Integer)
    district_id = Column(Integer)
    logo_mms_img_id = Column(String)
    brand_id = Column(Integer)
    is_open = Column(Boolean)
    contract_type = Column(Integer)
    location_url = Column(String)
    has_contract = Column(Boolean)
    is_quality_merchant = Column(Boolean)
    merchant_time = Column(Integer)
    service_type = Column(Integer)
    is_foody_delivery = Column(Boolean)
    limit_distance = Column(Integer)
    image_name = Column(String)
    restaurant_status = Column(Integer)
    address = Column(String)
    name = Column(String)
    foody_service_id = Column(Integer)
    url = Column(String)
    display_order = Column(Integer)
    delivery_id = Column(Integer)
    restaurant_url = Column(String)
    is_pickup = Column(Boolean)
    banner_mms_img_id = Column(String)
    url_rewrite_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    is_verified = Column(Boolean)

    # Relationships
    rating = relationship('Rating', uselist=False, backref='restaurant', lazy="selectin")
    operating = relationship('Operating', uselist=False, backref='restaurant', lazy="selectin")
    label = relationship('Label', uselist=False, backref='restaurant', lazy="selectin")
    brand = relationship('Brand', uselist=False, backref='restaurant', lazy="selectin")
    promotions = relationship('PromotionGroup', secondary=restaurant_promotion_association, backref='restaurants', lazy="selectin")
    photos = relationship('Photo', backref='restaurant', lazy="selectin")
    shipping_methods = relationship('ShippingMethod', secondary=restaurant_shipping_association, backref='restaurants', lazy="selectin")
