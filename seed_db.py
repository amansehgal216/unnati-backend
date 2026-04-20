import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_database():
    print("🌱 Starting database seeding...")
    
    # 1. Create admin user
    print("\n📝 Creating admin user...")
    existing_admin = await db.admin_users.find_one({"email": "admin@unnatiinvestments.in"})
    if not existing_admin:
        admin_user = {
            "email": "admin@unnatiinvestments.in",
            "password_hash": pwd_context.hash("admin123"),  # Change this password!
            "name": "Admin User",
            "role": "admin",
            "created_at": datetime.utcnow()
        }
        await db.admin_users.insert_one(admin_user)
        print("✅ Admin user created: admin@unnatiinvestments.in / admin123")
    else:
        print("⚠️  Admin user already exists")
    
    # 2. Seed blog posts
    print("\n📰 Seeding blog posts...")
    existing_blogs = await db.blogs.count_documents({})
    if existing_blogs == 0:
        blog_posts = [
            {
                "title": "Understanding SIP: A Beginner's Guide to Systematic Investment Plans",
                "excerpt": "Learn how SIP can help you build wealth systematically through disciplined investing in mutual funds.",
                "content": """
                    <p>Systematic Investment Plan (SIP) is one of the most popular ways to invest in mutual funds. It allows investors to invest a fixed amount regularly in their chosen mutual fund scheme.</p>
                    
                    <h3>Benefits of SIP:</h3>
                    <ul>
                        <li>Rupee Cost Averaging</li>
                        <li>Power of Compounding</li>
                        <li>Disciplined Investing</li>
                        <li>Flexibility</li>
                        <li>Convenience</li>
                    </ul>
                    
                    <p>Starting early with SIP can help you achieve your long-term financial goals effectively.</p>
                """,
                "author": "Aman Sehgal",
                "date": datetime.utcnow(),
                "category": "Investment Basics",
                "image": "https://images.unsplash.com/photo-1633158829875-e5316a358c6f",
                "readTime": "5 min read",
                "published": True
            },
            {
                "title": "PMS vs Mutual Funds: Which Investment Option is Right for You?",
                "excerpt": "Explore the key differences between Portfolio Management Services and Mutual Funds to make informed investment decisions.",
                "content": """
                    <p>Portfolio Management Service (PMS) and Mutual Funds are both popular investment options, but they cater to different investor segments.</p>
                    
                    <h3>Key Differences:</h3>
                    <ul>
                        <li>Minimum Investment: PMS requires higher minimum investment (₹50 lakhs) vs Mutual Funds (₹500)</li>
                        <li>Customization: PMS offers personalized portfolio vs standardized mutual fund schemes</li>
                        <li>Transparency: PMS provides direct ownership of securities</li>
                        <li>Costs: PMS has different fee structures compared to mutual funds</li>
                    </ul>
                """,
                "author": "Aman Sehgal",
                "date": datetime.utcnow(),
                "category": "Portfolio Management",
                "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
                "readTime": "7 min read",
                "published": True
            },
            {
                "title": "Alternative Investment Funds (AIF): Opportunities for HNI Investors",
                "excerpt": "Discover how AIFs can diversify your portfolio and provide access to alternative asset classes.",
                "content": """
                    <p>Alternative Investment Funds (AIFs) are privately pooled investment vehicles that invest in alternative asset classes.</p>
                    
                    <h3>Categories of AIFs:</h3>
                    <ul>
                        <li>Category I: Venture Capital, Angel Funds, Infrastructure Funds</li>
                        <li>Category II: Private Equity, Debt Funds</li>
                        <li>Category III: Hedge Funds, PIPE Funds</li>
                    </ul>
                    
                    <p>AIFs are suitable for sophisticated investors looking for diversification beyond traditional assets.</p>
                """,
                "author": "Aman Sehgal",
                "date": datetime.utcnow(),
                "category": "Alternative Investments",
                "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40",
                "readTime": "6 min read",
                "published": True
            }
        ]
        await db.blogs.insert_many(blog_posts)
        print(f"✅ Seeded {len(blog_posts)} blog posts")
    else:
        print(f"⚠️  {existing_blogs} blog posts already exist")
    
    # 3. Seed testimonials
    print("\n⭐ Seeding testimonials...")
    existing_testimonials = await db.testimonials.count_documents({})
    if existing_testimonials == 0:
        testimonials = [
            {
                "name": "Rajesh Kumar",
                "designation": "Business Owner",
                "content": "Working with Aman Sehgal and Unnati Investments has been a transformative experience. Their expertise in portfolio management helped me achieve my financial goals faster than I expected. Highly recommended for anyone serious about wealth creation.",
                "image": "https://via.placeholder.com/100/0A1F44/FFFFFF?text=RK",
                "rating": 5,
                "location": "Mumbai",
                "date": datetime.utcnow(),
                "published": True
            },
            {
                "name": "Priya Sharma",
                "designation": "IT Professional",
                "content": "As a first-time investor, I was nervous about mutual funds. Aman's personalized guidance and the team's patient approach made everything clear. My SIP investments are now growing steadily, and I feel confident about my financial future.",
                "image": "https://via.placeholder.com/100/0A1F44/FFFFFF?text=PS",
                "rating": 5,
                "location": "Bangalore",
                "date": datetime.utcnow(),
                "published": True
            },
            {
                "name": "Vikram Patel",
                "designation": "Entrepreneur",
                "content": "The professional approach and deep market knowledge of Unnati Investments is impressive. They helped me diversify my portfolio with PMS and AIF options that aligned perfectly with my risk appetite and goals.",
                "image": "https://via.placeholder.com/100/0A1F44/FFFFFF?text=VP",
                "rating": 5,
                "location": "Delhi",
                "date": datetime.utcnow(),
                "published": True
            },
            {
                "name": "Anjali Mehta",
                "designation": "Doctor",
                "content": "Planning for my children's education seemed daunting until I connected with Unnati Investments. Their goal-based planning approach and regular follow-ups give me peace of mind. Excellent service!",
                "image": "https://via.placeholder.com/100/0A1F44/FFFFFF?text=AM",
                "rating": 5,
                "location": "Pune",
                "date": datetime.utcnow(),
                "published": True
            }
        ]
        await db.testimonials.insert_many(testimonials)
        print(f"✅ Seeded {len(testimonials)} testimonials")
    else:
        print(f"⚠️  {existing_testimonials} testimonials already exist")
    
    # 4. Seed news items
    print("\n📢 Seeding news...")
    existing_news = await db.news.count_documents({})
    if existing_news == 0:
        news_items = [
            {
                "title": "SEBI Updates Mutual Fund Investment Guidelines",
                "description": "New regulations aim to enhance investor protection and transparency in mutual fund investments",
                "date": datetime.utcnow(),
                "category": "Regulatory",
                "published": True
            },
            {
                "title": "Top Performing Equity Funds in Q4 2024",
                "description": "Analysis of mutual funds that delivered exceptional returns in the last quarter",
                "date": datetime.utcnow(),
                "category": "Market Update",
                "published": True
            },
            {
                "title": "Tax Saving Investment Options for FY 2024-25",
                "description": "Complete guide to maximize tax savings through ELSS and other investment vehicles",
                "date": datetime.utcnow(),
                "category": "Tax Planning",
                "published": True
            }
        ]
        await db.news.insert_many(news_items)
        print(f"✅ Seeded {len(news_items)} news items")
    else:
        print(f"⚠️  {existing_news} news items already exist")
    
    # 5. Seed AMC partners
    print("\n🤝 Seeding AMC partners...")
    existing_partners = await db.amc_partners.count_documents({})
    if existing_partners == 0:
        amc_partners = [
            {"name": "HDFC Mutual Fund", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=HDFC+MF", "order": 1},
            {"name": "ICICI Prudential", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=ICICI+MF", "order": 2},
            {"name": "SBI Mutual Fund", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=SBI+MF", "order": 3},
            {"name": "Axis Mutual Fund", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=Axis+MF", "order": 4},
            {"name": "Kotak Mahindra", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=Kotak+MF", "order": 5},
            {"name": "Aditya Birla", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=ABSL+MF", "order": 6},
            {"name": "UTI Mutual Fund", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=UTI+MF", "order": 7},
            {"name": "DSP Mutual Fund", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=DSP+MF", "order": 8},
            {"name": "Franklin Templeton", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=Franklin", "order": 9},
            {"name": "Nippon India", "logo": "https://via.placeholder.com/120x60/0A1F44/D4AF37?text=Nippon", "order": 10}
        ]
        await db.amc_partners.insert_many(amc_partners)
        print(f"✅ Seeded {len(amc_partners)} AMC partners")
    else:
        print(f"⚠️  {existing_partners} AMC partners already exist")
    
    print("\n✅ Database seeding completed!")
    print("\n📋 Admin Credentials:")
    print("   Email: admin@unnatiinvestments.in")
    print("   Password: admin123")
    print("   ⚠️  PLEASE CHANGE THIS PASSWORD AFTER FIRST LOGIN!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
