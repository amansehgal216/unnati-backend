from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Website Settings Model
class WebsiteSettings(BaseModel):
    id: Optional[str] = None
    # Hero Section
    heroTitle: str = "Investing In Your Future"
    heroSubtitle: str = "Expert wealth management solutions with over 10 years of experience in Mutual Funds, PMS, and AIF investments."
    
    # Stats
    yearsExperience: int = 10
    happyClients: int = 1000
    aum: str = "₹500Cr+"
    
    # Milestones
    totalInvestors: int = 400
    happyFamilies: int = 150
    assetsUnderManagement: str = "₹500Cr+"
    
    # About Section
    aboutTitle: str = "Expert Financial Guidance You Can Trust"
    aboutDescription: str = "With over 10 years of proven expertise in the financial services industry, Aman Sehgal brings unparalleled knowledge and experience to Unnati Investments."
    founderQuote: str = "At Unnati Investments, we believe in building long-term wealth through disciplined investing, personalized strategies, and unwavering commitment to our clients' financial success."
    
    # Trust Indicators
    trustTitle: str = "Why Choose Unnati Investments?"
    trustSubtitle: str = "Trust us, your savings are in safe hands"
    trustFeature1Title: str = "Personalized Financial Roadmaps"
    trustFeature1Desc: str = "Tailored strategies designed to meet your unique financial goals"
    trustFeature2Title: str = "Unbiased & Research-Driven Advice"
    trustFeature2Desc: str = "Transparent recommendations backed by thorough market analysis"
    trustFeature3Title: str = "End-to-End Wealth Management"
    trustFeature3Desc: str = "Comprehensive solutions covering all aspects of your financial journey"
    trustFeature4Title: str = "Consistent Monitoring & Proactive Updates"
    trustFeature4Desc: str = "Regular portfolio reviews and timely insights to keep you informed"
    
    # Images
    heroBackgroundImage: str = "https://images.unsplash.com/photo-1542744173-05336fcc7ad4"
    aboutFounderImage: str = "https://images.unsplash.com/photo-1551836022-d5d88e9218df"
    serviceMutualFundsImage: str = "https://images.unsplash.com/photo-1633158829875-e5316a358c6f"
    servicePMSImage: str = "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
    serviceAIFImage: str = "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40"
    serviceInsuranceImage: str = "https://images.unsplash.com/photo-1450101499163-c8848c66ca85"
    servicePrivateEquityImage: str = "https://images.unsplash.com/photo-1559526324-4b87b5e36e44"
    
    # Mobile App
    mobileAppTitle: str = "Do More With Unnati Investments"
    mobileAppDescription: str = "The financial world is moving at a fast pace with technological advancements that have brought financial services to your fingertips. We present to you the Unnati Investments app to stay ahead of the curve by unleashing the power of investments."
    playStoreUrl: str = "https://play.google.com/store/apps/details?id=in.mymfbox"
    appStoreUrl: str = "https://apps.apple.com/in/app/themfbox/id1594370380"
    
    # Contact Info
    email: str = "info@unnatiinvestments.in"
    phone: str = "+91 XXX XXX XXXX"
    address: str = "Mumbai, India"
    
    # Social Media
    facebookUrl: Optional[str] = "#"
    twitterUrl: Optional[str] = "#"
    linkedinUrl: Optional[str] = "#"
    instagramUrl: Optional[str] = "#"
    
    # Footer
    footerDescription: str = "Investing in your future with expertise and trust. Over 10 years of financial planning excellence."
    footerDisclaimer: str = "Mutual fund investments are subject to market risks. Please read all scheme related documents carefully before investing."
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WebsiteSettingsUpdate(BaseModel):
    heroTitle: Optional[str] = None
    heroSubtitle: Optional[str] = None
    yearsExperience: Optional[int] = None
    happyClients: Optional[int] = None
    aum: Optional[str] = None
    totalInvestors: Optional[int] = None
    happyFamilies: Optional[int] = None
    assetsUnderManagement: Optional[str] = None
    aboutTitle: Optional[str] = None
    aboutDescription: Optional[str] = None
    founderQuote: Optional[str] = None
    trustTitle: Optional[str] = None
    trustSubtitle: Optional[str] = None
    trustFeature1Title: Optional[str] = None
    trustFeature1Desc: Optional[str] = None
    trustFeature2Title: Optional[str] = None
    trustFeature2Desc: Optional[str] = None
    trustFeature3Title: Optional[str] = None
    trustFeature3Desc: Optional[str] = None
    trustFeature4Title: Optional[str] = None
    trustFeature4Desc: Optional[str] = None
    heroBackgroundImage: Optional[str] = None
    aboutFounderImage: Optional[str] = None
    serviceMutualFundsImage: Optional[str] = None
    servicePMSImage: Optional[str] = None
    serviceAIFImage: Optional[str] = None
    serviceInsuranceImage: Optional[str] = None
    servicePrivateEquityImage: Optional[str] = None
    mobileAppTitle: Optional[str] = None
    mobileAppDescription: Optional[str] = None
    playStoreUrl: Optional[str] = None
    appStoreUrl: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    facebookUrl: Optional[str] = None
    twitterUrl: Optional[str] = None
    linkedinUrl: Optional[str] = None
    instagramUrl: Optional[str] = None
    footerDescription: Optional[str] = None
    footerDisclaimer: Optional[str] = None
