from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
from datetime import datetime, timezone, timedelta
import uuid
from typing import Optional, List

# Define the SQLite database connection
engine = create_engine('sqlite:///auth_database.db', echo=True)
Base = declarative_base()

# 1. Users Table (for authentication)
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = Column(String, nullable=False)  # Store hashed passwords
    email: Mapped[Optional[str]] = Column(String, unique=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now(timezone.utc))
    
    # Bi-directional relationship to AuthorizationCode and Token
    auth_codes: Mapped[List["AuthorizationCode"]] = relationship("AuthorizationCode", back_populates="user")
    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="user")

# 2. Clients Table (for OAuth clients)
class Client(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = Column(Integer, primary_key=True)
    client_id: Mapped[str] = Column(String, unique=True, nullable=False)
    client_secret: Mapped[str] = Column(String, nullable=False)  # Store hashed secret
    redirect_uri: Mapped[str] = Column(String, nullable=False)
    scopes: Mapped[Optional[str]] = Column(String)  # Comma-separated scope names
    client_name: Mapped[Optional[str]] = Column(String)
    client_type: Mapped[Optional[str]] = Column(String)  # "public" or "confidential"
    
    # Bi-directional relationship to AuthorizationCode and Token
    auth_codes: Mapped[List["AuthorizationCode"]] = relationship("AuthorizationCode", back_populates="client")
    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="client")

# 3. Authorization Codes Table (for storing authorization codes)
class AuthorizationCode(Base):
    __tablename__ = 'authorization_codes'
    id: Mapped[int] = Column(Integer, primary_key=True)
    code: Mapped[str] = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'))
    client_id: Mapped[int] = Column(Integer, ForeignKey('clients.id'))
    scopes: Mapped[Optional[str]] = Column(String)
    expires_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=10))
    is_used: Mapped[bool] = Column(Boolean, default=False)
    
    # Define relationships back to User and Client
    user: Mapped["User"] = relationship("User", back_populates="auth_codes")
    client: Mapped["Client"] = relationship("Client", back_populates="auth_codes")

# 4. Tokens Table (for access and refresh tokens)
class Token(Base):
    __tablename__ = 'tokens'
    id: Mapped[int] = Column(Integer, primary_key=True)
    access_token: Mapped[str] = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    refresh_token: Mapped[str] = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'))
    client_id: Mapped[int] = Column(Integer, ForeignKey('clients.id'))
    scopes: Mapped[Optional[str]] = Column(String)
    issued_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(hours=1))
    revoked: Mapped[bool] = Column(Boolean, default=False)
    
    # Define relationships back to User and Client
    user: Mapped["User"] = relationship("User", back_populates="tokens")
    client: Mapped["Client"] = relationship("Client", back_populates="tokens")

# 5. Scopes Table (optional, stores scope descriptions)
class Scope(Base):
    __tablename__ = 'scopes'
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    description: Mapped[Optional[str]] = Column(String)  # Description of what the scope allows
