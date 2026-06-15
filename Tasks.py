from orders.models import Order
from .predictor import EyeWearAIPredictor

def run_order_analytics_pipeline(order_id):
    """
    Executes the analytical data processing sequence.
    Updates the target order with estimated completion times and risk analysis profiles.
    """
    try:
        order = Order.objects.get(id=order_id)
        
        # Step 1: Run inference using the Scikit-Learn Machine Learning model
        order.predicted_tat_hours = EyeWearAIPredictor.predict_completion_hours(order)
        
        # Step 2: Compare predicted execution speeds against promised SLA windows
        order.ai_breach_risk = EyeWearAIPredictor.assess_breach_risk(order)
        order.save()
        
        # Step 3: Trigger external notification routing hooks if a bottleneck is flagged
        if order.ai_breach_risk in ['HIGH_RISK', 'BREACHED']:
            trigger_breach_alert_payload(order)
            
    except Order.DoesNotExist:
        pass

def trigger_breach_alert_payload(order):
    """
    Simulates sending an emergency operational alert to communication channels 
    (Twilio WhatsApp webhook brokers or SendGrid mailing layouts).
    """
    print(f"\n⚡ --- SYSTEM BREACH ALERT TRIGGERED --- ⚡")
    print(f"CRITICAL WARNING: Order {order.order_number} for {order.customer_name} is running dangerously late!")
    print(f"Current State: {order.status} | Promised SLA: {order.sla_hours} hours")
    print(f"AI Calculated Remaining Duration: {order.predicted_tat_hours} hours")
    print(f"Dispatched WhatsApp notification to lab supervisor for immediate line escalation.\n")