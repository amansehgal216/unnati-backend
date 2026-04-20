from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from models import (
    BlogPost, BlogPostCreate, BlogPostUpdate,
    Testimonial, TestimonialCreate, TestimonialUpdate,
    News, NewsCreate, NewsUpdate,
    AMCPartner, AMCPartnerCreate,
    RecommendedFund, RecommendedFundCreate, RecommendedFundUpdate,
    AdminLogin, AdminCreate
)
from settings_models import WebsiteSettings, WebsiteSettingsUpdate
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import os
from bson import ObjectId

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# Get database from request
async def get_db(request: Request):
    return request.state.db

# Authentication Routes
@router.post("/admin/login")
async def admin_login(credentials: AdminLogin, request: Request):
    db = request.state.db
    user = await db.admin_users.find_one({"email": credentials.email})
    if not user or not pwd_context.verify(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user["email"],
            "name": user["name"],
            "role": user.get("role", "admin")
        }
    }

@router.post("/admin/create")
async def create_admin(admin: AdminCreate, request: Request):
    db = request.state.db
    # Check if admin already exists
    existing = await db.admin_users.find_one({"email": admin.email})
    if existing:
        raise HTTPException(status_code=400, detail="Admin user already exists")
    
    # Create admin user
    admin_dict = {
        "email": admin.email,
        "password_hash": pwd_context.hash(admin.password),
        "name": admin.name,
        "role": "admin",
        "created_at": datetime.utcnow()
    }
    
    result = await db.admin_users.insert_one(admin_dict)
    return {"message": "Admin created successfully", "id": str(result.inserted_id)}

# Blog Routes
@router.get("/blogs", response_model=List[BlogPost])
async def get_blogs(request: Request, published_only: bool = True):
    db = request.state.db
    query = {"published": True} if published_only else {}
    blogs = await db.blogs.find(query).sort("date", -1).to_list(100)
    return [serialize_doc(blog) for blog in blogs]

@router.get("/blogs/{blog_id}", response_model=BlogPost)
async def get_blog(blog_id: str, request: Request):
    db = request.state.db
    blog = await db.blogs.find_one({"_id": ObjectId(blog_id)})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return serialize_doc(blog)

@router.post("/blogs", response_model=BlogPost)
async def create_blog(blog: BlogPostCreate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    blog_dict = blog.dict()
    blog_dict["author"] = "Aman Sehgal"
    blog_dict["date"] = datetime.utcnow()
    
    result = await db.blogs.insert_one(blog_dict)
    blog_dict["id"] = str(result.inserted_id)
    return blog_dict

@router.put("/blogs/{blog_id}", response_model=BlogPost)
async def update_blog(blog_id: str, blog: BlogPostUpdate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    update_data = {k: v for k, v in blog.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.blogs.find_one_and_update(
        {"_id": ObjectId(blog_id)},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return serialize_doc(result)

@router.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: str, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    result = await db.blogs.delete_one({"_id": ObjectId(blog_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}

# Testimonial Routes
@router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials(request: Request, published_only: bool = True):
    db = request.state.db
    query = {"published": True} if published_only else {}
    testimonials = await db.testimonials.find(query).sort("date", -1).to_list(100)
    return [serialize_doc(t) for t in testimonials]

@router.post("/testimonials", response_model=Testimonial)
async def create_testimonial(testimonial: TestimonialCreate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    testimonial_dict = testimonial.dict()
    testimonial_dict["date"] = datetime.utcnow()
    
    result = await db.testimonials.insert_one(testimonial_dict)
    testimonial_dict["id"] = str(result.inserted_id)
    return testimonial_dict

@router.put("/testimonials/{testimonial_id}", response_model=Testimonial)
async def update_testimonial(testimonial_id: str, testimonial: TestimonialUpdate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    update_data = {k: v for k, v in testimonial.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.testimonials.find_one_and_update(
        {"_id": ObjectId(testimonial_id)},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    return serialize_doc(result)

@router.delete("/testimonials/{testimonial_id}")
async def delete_testimonial(testimonial_id: str, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    result = await db.testimonials.delete_one({"_id": ObjectId(testimonial_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return {"message": "Testimonial deleted successfully"}

# News Routes
@router.get("/news", response_model=List[News])
async def get_news(request: Request, published_only: bool = True):
    db = request.state.db
    query = {"published": True} if published_only else {}
    news_items = await db.news.find(query).sort("date", -1).to_list(100)
    return [serialize_doc(n) for n in news_items]

@router.post("/news", response_model=News)
async def create_news(news: NewsCreate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    news_dict = news.dict()
    news_dict["date"] = datetime.utcnow()
    
    result = await db.news.insert_one(news_dict)
    news_dict["id"] = str(result.inserted_id)
    return news_dict

@router.put("/news/{news_id}", response_model=News)
async def update_news(news_id: str, news: NewsUpdate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    update_data = {k: v for k, v in news.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.news.find_one_and_update(
        {"_id": ObjectId(news_id)},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    
    return serialize_doc(result)

@router.delete("/news/{news_id}")
async def delete_news(news_id: str, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    result = await db.news.delete_one({"_id": ObjectId(news_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="News not found")
    return {"message": "News deleted successfully"}

# AMC Partner Routes
@router.get("/amc-partners", response_model=List[AMCPartner])
async def get_amc_partners(request: Request):
    db = request.state.db
    partners = await db.amc_partners.find().sort("order", 1).to_list(100)
    return [serialize_doc(p) for p in partners]

@router.post("/amc-partners", response_model=AMCPartner)
async def create_amc_partner(partner: AMCPartnerCreate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    partner_dict = partner.dict()
    result = await db.amc_partners.insert_one(partner_dict)
    partner_dict["id"] = str(result.inserted_id)
    return partner_dict

@router.delete("/amc-partners/{partner_id}")
async def delete_amc_partner(partner_id: str, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    result = await db.amc_partners.delete_one({"_id": ObjectId(partner_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="AMC Partner not found")
    return {"message": "AMC Partner deleted successfully"}

# Recommended Funds Routes
@router.get("/recommended-funds", response_model=List[RecommendedFund])
async def get_recommended_funds(request: Request, published_only: bool = True):
    db = request.state.db
    query = {"published": True} if published_only else {}
    funds = await db.recommended_funds.find(query).sort("order", 1).to_list(100)
    return [serialize_doc(f) for f in funds]

@router.get("/recommended-funds/{fund_id}", response_model=RecommendedFund)
async def get_recommended_fund(fund_id: str, request: Request):
    db = request.state.db
    fund = await db.recommended_funds.find_one({"_id": ObjectId(fund_id)})
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return serialize_doc(fund)

@router.post("/recommended-funds", response_model=RecommendedFund)
async def create_recommended_fund(fund: RecommendedFundCreate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    fund_dict = fund.dict()
    fund_dict["date"] = datetime.utcnow()
    
    result = await db.recommended_funds.insert_one(fund_dict)
    fund_dict["id"] = str(result.inserted_id)
    return fund_dict

@router.put("/recommended-funds/{fund_id}", response_model=RecommendedFund)
async def update_recommended_fund(fund_id: str, fund: RecommendedFundUpdate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    update_data = {k: v for k, v in fund.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.recommended_funds.find_one_and_update(
        {"_id": ObjectId(fund_id)},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    return serialize_doc(result)

@router.delete("/recommended-funds/{fund_id}")
async def delete_recommended_fund(fund_id: str, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    result = await db.recommended_funds.delete_one({"_id": ObjectId(fund_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Fund not found")
    return {"message": "Fund deleted successfully"}

# Website Settings Routes
@router.get("/settings", response_model=WebsiteSettings)
async def get_settings(request: Request):
    db = request.state.db
    settings = await db.website_settings.find_one()
    if not settings:
        # Create default settings if none exist
        default_settings = WebsiteSettings().dict()
        await db.website_settings.insert_one(default_settings)
        settings = await db.website_settings.find_one()
    return serialize_doc(settings)

@router.put("/settings", response_model=WebsiteSettings)
async def update_settings(settings: WebsiteSettingsUpdate, request: Request, email: str = Depends(verify_token)):
    db = request.state.db
    update_data = {k: v for k, v in settings.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Get existing settings or create new
    existing = await db.website_settings.find_one()
    if not existing:
        default_settings = WebsiteSettings().dict()
        await db.website_settings.insert_one(default_settings)
        existing = await db.website_settings.find_one()
    
    result = await db.website_settings.find_one_and_update(
        {"_id": existing["_id"]},
        {"$set": update_data},
        return_document=True
    )
    
    return serialize_doc(result)
