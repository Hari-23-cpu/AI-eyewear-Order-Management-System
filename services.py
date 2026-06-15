import os
from django.conf import settings
from openai import OpenAI
import json

class EyewearAIConversationalAgent:

    @classmethod
    def analyze_qc_failure(cls, technician_notes, customer_name):
        """
        Intercepts unstructured QC failure notes, runs an analytical OpenAI evaluation,
        and returns a structured root cause and a custom customer notification.
        """
        try:
            api_key = settings.env('OPENAI_API_KEY')
        except Exception:
            api_key = None

        if not api_key:
            return {
                "root_cause": "QC Mechanical Failure",
                "whatsapp_message": f"Hi {customer_name}, we are adjusting your eyewear lenses to guarantee perfect precision. Thanks for your patience!"
            }
        
        client = OpenAI(api_key=api_key)

        system_instruction = (
            "You are an expert Optical Laboratory QA Supervisor. Your job is to analyze a technician's "
            "raw, messy notes regarding a lens quality check failure, extract the technical root cause "
            "in 3-5 words, and draft a polite, reassuring update for the customer. "
            "CRITICAL: Do not mention internal lab terms like 'QC failure', 'scratched machine', or 'mistake' "
            "to the customer. Instead, phrase it as a dedication to custom engineering and extreme precision calibration."
        )

        user_input = f"Customer Name: {customer_name}\nTechnician Notes: {technician_notes}"

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={ "type": "json_object" }, 
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3 
            )

            raw_json_output = response.choices[0].message.content
            parsed_data = json.loads(raw_json_output)

            return {
                "root_cause": parsed_data.get("root_cause", "Precision Calibration Variance"),
                "whatsapp_message": parsed_data.get("whatsapp_message", f"Hi {customer_name}, we are fine-tuning your custom lenses.")
            }

        except Exception as e:
            print(f"OpenAI API Error Intercepted: {e}")
            return {
                "root_cause": "Operational Loop Interception",
                "whatsapp_message": f"Hi {customer_name}, we are performing an extra optimization scan on your lenses to guarantee perfect clarity."
            }