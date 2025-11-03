from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import pandas as pd
from rapidfuzz import process, fuzz
import os

class ActionPDEUFAQ(Action):
    def name(self) -> Text:
        return "action_pdeu_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load CSV data with fallback
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "../data/questions_db.csv")
        
        # Fallback FAQ data if CSV not available
        fallback_faq = {
            "admission": "You can apply online through https://pdeu.ac.in/admissions. Complete the application form and upload required documents.",
            "fees": "B.Tech tuition fee is ₹2,25,000 per semester. Total annual fee including hostel is approximately ₹5,50,000.",
            "hostel": "PDEU provides excellent hostel facilities with AC/Non-AC rooms, WiFi, mess, laundry, and 24x7 security.",
            "placement": "PDEU has 85%+ placement rate with average package ₹6-8 LPA. Top recruiters include TCS, Infosys, Reliance, Microsoft.",
            "eligibility": "Minimum 50% in 12th with PCM and valid JEE Main score or PDET score required for B.Tech admission.",
            "scholarship": "Merit-based scholarships up to 100% fee waiver, need-based scholarships, and sports scholarships available."
        }

        user_msg = tracker.latest_message.get('text', '').lower().strip()
        
        try:
            faq_df = pd.read_csv(csv_path)
            if 'question' in faq_df.columns and 'answer' in faq_df.columns:
                faq_questions = faq_df['question'].astype(str).tolist()
                faq_answers = faq_df['answer'].astype(str).tolist()
                
                matches = process.extract(user_msg, faq_questions, scorer=fuzz.token_sort_ratio, limit=3)
                best_match = matches[0] if matches else None
                
                if best_match and best_match[1] >= 60:
                    response = faq_answers[best_match[2]]
                    dispatcher.utter_message(text=response)
                    return [FollowupAction("action_followup_suggestions")]
        except:
            pass
        
        # Fallback to keyword matching
        for keyword, answer in fallback_faq.items():
            if keyword in user_msg:
                dispatcher.utter_message(text=answer)
                return [FollowupAction("action_followup_suggestions")]
        
        # Default response
        dispatcher.utter_message(text="I'd be happy to help! Here are some popular topics:")
        dispatcher.utter_message(text="Choose a topic:", buttons=[
            {"title": "📘 Admission Process", "payload": "/admission_process"},
            {"title": "💰 Fees & Scholarships", "payload": "/fees"},
            {"title": "🏠 Hostel Facilities", "payload": "/hostel"},
            {"title": "💼 Placements", "payload": "/placement"},
            {"title": "🎓 Eligibility", "payload": "/eligibility"},
            {"title": "📞 Contact Info", "payload": "/contact"}
        ])
        
        return []

class ActionContextualResponse(Action):
    def name(self) -> Text:
        return "action_contextual_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        last_intent = tracker.get_slot("last_intent")
        user_interest = tracker.get_slot("user_interest")
        
        # Provide contextual follow-up based on previous interaction
        if last_intent == "fees":
            dispatcher.utter_message(text="Would you also like to know about scholarships or payment options?")
        elif last_intent == "admission_process":
            dispatcher.utter_message(text="Do you need information about eligibility criteria or required documents?")
        elif last_intent == "hostel":
            dispatcher.utter_message(text="Would you like to know about hostel fees or room allocation process?")
        
        return []

class ActionFollowupSuggestions(Action):
    def name(self) -> Text:
        return "action_followup_suggestions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        latest_intent = tracker.latest_message['intent']['name']
        
        suggestions = {
            "admission_process": [
                {"title": "🎓 Eligibility Criteria", "payload": "/eligibility"},
                {"title": "💰 Fee Structure", "payload": "/fees"},
                {"title": "📞 Contact Admissions", "payload": "/contact"}
            ],
            "fees": [
                {"title": "🎓 Scholarships", "payload": "/scholarship"},
                {"title": "🏠 Hostel Fees", "payload": "/hostel"},
                {"title": "📘 Admission Process", "payload": "/admission_process"}
            ],
            "hostel": [
                {"title": "💰 Hostel Fees", "payload": "/fees"},
                {"title": "🛡️ Safety Measures", "payload": "/safety"},
                {"title": "🍽️ Mess Facilities", "payload": "/facilities"}
            ],
            "placement": [
                {"title": "📚 Courses Offered", "payload": "/courses"},
                {"title": "🎓 Eligibility", "payload": "/eligibility"},
                {"title": "💼 Internships", "payload": "/academic"}
            ]
        }
        
        if latest_intent in suggestions:
            dispatcher.utter_message(text="💡 You might also want to know:", 
                                   buttons=suggestions[latest_intent])
        
        return [SlotSet("last_intent", latest_intent)]

class ValidateAdmissionForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_admission_form"

    def validate_course_type(self, slot_value: Any, dispatcher: CollectingDispatcher,
                           tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        valid_courses = ["b.tech", "btech", "engineering", "mba", "mca", "m.tech", "mtech"]
        if slot_value.lower() in valid_courses:
            return {"course_type": slot_value}
        else:
            dispatcher.utter_message(text="Please select from: B.Tech, MBA, MCA, M.Tech")
            return {"course_type": None}

class ValidateFeeInquiryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_fee_inquiry_form"

    def validate_fee_type(self, slot_value: Any, dispatcher: CollectingDispatcher,
                         tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        valid_types = ["tuition", "hostel", "total", "semester", "annual"]
        if slot_value.lower() in valid_types:
            return {"fee_type": slot_value}
        else:
            dispatcher.utter_message(text="Please specify: tuition, hostel, or total fees")
            return {"fee_type": None}
