class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # ✅ Add this to prevent redeclaration errors

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.user)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    cumulative_sales = Column(Numeric(12, 2), default=0.00)

    # Relationships
    fee_transactions = relationship("FeeTransaction", back_populates="user")
    fraud_alerts = relationship("FraudAlert", back_populates="user")