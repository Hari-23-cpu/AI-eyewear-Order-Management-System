import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from django.utils import timezone
from orders.models import Order

MODEL_PATH = os.path.join(os.path.dirname(__file__))

class EyeWearAIPredictor:
     """Uses a trained Scikit-Learn Gradient Boosting Regressor to predict real production TAT."""

     @classmethod
     def train_model_on_history(cls):
           """Scans completed historical orders to train/update the AI model."""
           historical_orders = Order.objects.filter(status = 'DELIVERED')

           if historical_orders.count()<5:
                 return False
           
           data = []
           for o in historical_orders:
                 elapsed_hours = 24.0
                 data.append({
                       'lens_type_num':1 if o.lens_type =='SINGLE_VISION'else (2 if o.lens_type =='BIFOCAL'else 3),
                       'lens_index':float(o.lens_index),
                       'is_outsourced':1 if o.inventory_source == 'OUTSOURCED' else 0,
                       'actual_tat':elapsed_hours
                    })
                 
                 df = pd.DataFrame(data)
                 X = df[['lens_type_num','lens_index','is_outsourced']]
                 Y = df[['actual_tat']]

                 model = GradientBoostingRegressor(n_estimators=100,random_state=42)
                 model.fit(X,Y)

                 with open (MODEL_PATH,'wb') as f:
                      pickle.dump(model,f)
                 return True
           
@classmethod
def predict_completion_hours(cls,order):
       """Scans completed historical orders to train/update the AI model."""
       if not os.path.exists(MODEL_PATH):
             return 12.0 if order.lens_type == 'SINGLE_VISION' else 36.0
       
       with open(MODEL_PATH,'rb') as f:
             model = pickle.load(f)

       lens_type_num = 1 if order.lens_type == 'SINGLE_VISION' else (2 if order.lens_type == 'BIFOCAL' else 3)

       is_outsourced = 1 if order.inventory_source == 'OUTSOURCED' else 0

        

       input_data = pd.DataFrame([{

            'lens_type_num': lens_type_num,

            'lens_index': float(order.lens_index),

            'is_outsourced': is_outsourced

        }])

        

       prediction = model.predict(input_data)
       return float(np.round(prediction[0], 1))

@classmethod
def assess_breach_risk(cls,order):
      if not order.predicted_tat_hours:
            return 'NORMAL'
      
      elapsed_hours = (timezone.now()-order.created_at).total_seconds()/3600

      estimated_total_time = elapsed_hours+order.predicted_tat_hours

      if estimated_total_time >= order.sla_hours:
            return 'BREACHED'
      elif(order.sla_hours-estimated_total_time)<6.0:
            return 'HIGH RISK'
      
      return 'NORMAL'
       
       

                     
           
          
