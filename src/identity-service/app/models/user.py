from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Association Table for Many-to-Many
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('identity.users.id', ondelete="CASCADE"), primary_key=True),
    Column('role_id', Integer, ForeignKey('identity.roles.id', ondelete="CASCADE"), primary_key=True),
    schema='identity'
)

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "identity"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to Roles
    roles = relationship("Role", secondary=user_roles, backref="users")
    