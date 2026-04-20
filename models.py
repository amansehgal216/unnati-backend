from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Blog Models
class BlogPost(BaseModel):
    id: Optional[str] = None
    title: str
    excerpt: str
    content: str
    author: str = "Aman Sehgal"
    category: str
    image: str
    readTime: str
    date: datetime = Field(default_factory=datetime.utcnow)
    published: bool = True

class BlogPostCreate(BaseModel):
    title: str
    excerpt: str
    content: str
    category: str
    image: str
    readTime: str
    published: bool = True

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    readTime: Optional[str] = None
    published: Optional[bool] = None

# Testimonial Models
class Testimonial(BaseModel):
    id: Optional[str] = None
    name: str
    designation: str
    content: str
    image: str
    rating: int = 5
    location: str
    date: datetime = Field(default_factory=datetime.utcnow)
    published: bool = True

class TestimonialCreate(BaseModel):
    name: str
    designation: str
    content: str
    image: str
    rating: int = 5
    location: str
    published: bool = True

class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[int] = None
    location: Optional[str] = None
    published: Optional[bool] = None

# News Models
class News(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    category: str
    date: datetime = Field(default_factory=datetime.utcnow)
    published: bool = True

class NewsCreate(BaseModel):
    title: str
    description: str
    category: str
    published: bool = True

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    published: Optional[bool] = None

# AMC Partner Models
class AMCPartner(BaseModel):
    id: Optional[str] = None
    name: str
    logo: str
    order: int = 0

class AMCPartnerCreate(BaseModel):
    name: str
    logo: str
    order: int = 0

# Recommended Mutual Fund Models
class RecommendedFund(BaseModel):
    id: Optional[str] = None
    fundName: str
    amc: str
    category: str
    returns1Y: float
    returns3Y: float
    returns5Y: float
    minInvestment: int
    riskLevel: str  # Low, Medium, High
    rating: int  # 1-5
    description: str
    navValue: float
    expenseRatio: float
    fundSize: str  # e.g., "₹1000 Cr"
    schemeCode: Optional[int] = None  # MFApi scheme code for live data
    published: bool = True
    order: int = 0
    date: datetime = Field(default_factory=datetime.utcnow)

class RecommendedFundCreate(BaseModel):
    fundName: str
    amc: str
    category: str
    returns1Y: float
    returns3Y: float
    returns5Y: float
    minInvestment: int
    riskLevel: str
    rating: int
    description: str
    navValue: float
    expenseRatio: float
    fundSize: str
    schemeCode: Optional[int] = None
    published: bool = True
    order: int = 0

class RecommendedFundUpdate(BaseModel):
    fundName: Optional[str] = None
    amc: Optional[str] = None
    category: Optional[str] = None
    returns1Y: Optional[float] = None
    returns3Y: Optional[float] = None
    returns5Y: Optional[float] = None
    minInvestment: Optional[int] = None
    riskLevel: Optional[str] = None
    rating: Optional[int] = None
    description: Optional[str] = None
    navValue: Optional[float] = None
    expenseRatio: Optional[float] = None
    fundSize: Optional[str] = None
    schemeCode: Optional[int] = None
    published: Optional[bool] = None
    order: Optional[int] = None

# Admin User Model
class AdminUser(BaseModel):
    id: Optional[str] = None
    email: str
    password_hash: str
    name: str
    role: str = "admin"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminLogin(BaseModel):
    email: str
    password: str

class AdminCreate(BaseModel):
    email: str
    password: str
    name: str
