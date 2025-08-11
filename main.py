# main.py

from modules.property_scraper import PropertyScraper
# from modules.legal_analyzer import LegalAnalyzer
# from modules.community_insights import CommunityInsights
# from modules.market_comparator import MarketComparator
# from modules.recommendation_engine import RecommendationEngine
# from modules.financial_assessor import FinancialAssessor
# from modules.chat_agent import ChatAgent
import json
import asyncio


def main():
    print("🚀 Starting Real Estate AI Consultant Pipeline...\n")

    # Step 1: Get input (property address, user profile, optional documents)
    # address = input("🏠 Enter property address: ")
    # website_url = input("🌐 Enter property listing website (optional): ")
    # user_profile = {
    #     "income": float(input("💰 Enter your annual income (USD): ")),
    #     "budget": float(input("💵 Enter your budget for purchase (USD): ")),
    #     "bedrooms": int(input("🛏️ Desired number of bedrooms: "))
    # }

    url = "https://www.redfin.com/CA/Sunnyvale/822-Julian-Ter-94085/unit-4/home/172929985"

    # Step 2: Scrape property data
    scraper = PropertyScraper()
    property_data = asyncio.run(scraper.fetch_property_info(url))

    print("✅ Property data fetched successfully.")
    print(json.dumps(property_data, indent=2, ensure_ascii=False))    
  

    # # Step 3: Analyze legal documents (optional upload)
    # legal_analyzer = LegalAnalyzer()
    # disclosure_summary = legal_analyzer.analyze_disclosures(address)

    # # Step 4: Community and location insights
    # insights = CommunityInsights()
    # neighborhood_report = insights.get_neighborhood_info(address)

    # # Step 5: Market comparison and price trend
    # comparator = MarketComparator()
    # market_comparison = comparator.compare_nearby_properties(address)

    # # Step 6: Financial assessment
    # assessor = FinancialAssessor()
    # affordability_report = assessor.evaluate_affordability(user_profile)

    # # Step 7: Generate personalized recommendation
    # recommender = RecommendationEngine()
    # recommendation = recommender.generate(
    #     property_data, neighborhood_report, market_comparison, user_profile
    # )

    # # Step 8: LLM-based conversational Q&A agent
    # chat = ChatAgent()
    # chat.start_conversation(
    #     context={
    #         "property": property_data,
    #         "legal": disclosure_summary,
    #         "community": neighborhood_report,
    #         "market": market_comparison,
    #         "financial": affordability_report,
    #         "recommendation": recommendation
    #     }
    # )

    # print("\n✅ Real Estate AI Consultation Complete.")


if __name__ == "__main__":
    main()
