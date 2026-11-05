from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON
)

from sqlalchemy.sql import func

from database import Base


class Invoice(Base):

    __tablename__ = "invoices"

    # Primary key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Unique job identifier
    job_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    # Original uploaded filename
    filename = Column(
        String,
        nullable=True
    )

    # Job processing status
    status = Column(
        String,
        default="pending",
        nullable=False
    )

    # Extracted invoice information
    result = Column(
        JSON,
        nullable=True
    )

    # Error message
    error = Column(
        String,
        nullable=True
    )

    # Creation timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Last updated timestamp
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )