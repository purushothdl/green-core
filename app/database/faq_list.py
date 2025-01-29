
from app.schemas.faqs import FAQ

faqs = [
    # Waste Classification
    FAQ(
        label="Waste Classification",
        question="How does the app classify waste?",
        answer="The app uses AI to analyze images of waste and classify them into categories like recyclable, biodegradable, or hazardous."
    ),
    FAQ(
        label="Waste Classification",
        question="What types of waste can the app classify?",
        answer="The app can classify common waste types such as plastic, paper, glass, organic waste, and electronic waste."
    ),

    # Waste Disposal
    FAQ(
        label="Waste Disposal",
        question="How do I dispose of recyclable waste?",
        answer="Recyclable waste should be placed in designated recycling bins. Check local guidelines for specific instructions."
    ),
    FAQ(
        label="Waste Disposal",
        question="What should I do with hazardous waste?",
        answer="Hazardous waste (e.g., batteries, chemicals) should be taken to a designated disposal facility. Do not dispose of it in regular bins."
    ),
    FAQ(
        label="Waste Disposal",
        question="Can I dispose of waste at any organization?",
        answer="No, you can only dispose of waste at an organization if you are within 50 meters of their location. The app will notify you if you are within range."
    ),

    # App Usage
    FAQ(
        label="App Usage",
        question="How do I upload an image for classification?",
        answer="Go to the 'Classify Waste' section, click 'Upload Image,' and select a photo of the waste. The app will analyze it and provide a classification."
    ),
    FAQ(
        label="App Usage",
        question="Can I ask the chatbot for disposal advice?",
        answer="Yes, you can ask the chatbot for advice on how to dispose of specific types of waste. Just type your question or upload an image."
    ),

    # Dashboard
    FAQ(
        label="Dashboard",
        question="What does the dashboard show?",
        answer="The dashboard displays your waste disposal history, nearby organizations, and a graph of your waste disposal trends over time."
    ),
    FAQ(
        label="Dashboard",
        question="How do I view my waste disposal history?",
        answer="Go to the 'Dashboard' section and click on 'Disposal History' to view all your past waste disposals, including dates and types of waste."
    ),

    # General
    FAQ(
        label="General",
        question="What should I do if the app misclassifies waste?",
        answer="If the app misclassifies waste, you can manually correct the classification and provide feedback to help improve the AI model."
    ),
    FAQ(
        label="General",
        question="How can I view my chat history?",
        answer="Go to the 'Chat History' section to view all your previous chats with the chatbot, including waste classifications and disposal advice."
    ),
    FAQ(
        label="General",
        question="What happens if I try to dispose of waste outside the 50-meter range?",
        answer="The app will notify you that you are not within range of any organization. You must move closer to a disposal point to proceed."
    ),
]