from django.db import models

class Order(models.Model):
    STATUS_CHOICES =[
        ('PLACED','Order placed'),
        ('LAB_ROUTING','Lab Routing'),
        ('PROCESSING','Lens processing'),
        ('QC','Quality Check'),
        ('READY','Ready to Dispatch'),
        ('DELIVERED','Delivered'),
    ]

    LENS_TYPES = [
        ('SINGLE_VISION','single vision'),
        ('BIFOCAL','Bifocal'),
        ('PROGRESSIVE','progressive'),
    ]

    Order_number = models.CharField(max_length=50,unique=True)
    Customer_name = models.CharField(max_length=100)
    Store_location = models.CharField(max_length=100,db_index=True)

    od_sphere = models.DecimalField(max_digits=4, decimal_places=2)  # Right Eye
    od_cylinder = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    os_sphere = models.DecimalField(max_digits=4, decimal_places=2)  # Left Eye
    os_cylinder = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    lens_type = models.CharField(max_length=100,choices=LENS_TYPES,db_index=True)
    lens_index = models.DecimalField(max_digits=3, decimal_places=2)
    coating = models.CharField(max_length=100)
    frame_model = models.CharField(max_length=100)

    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default= 'PLACED',db_index=True)
    inventory_source = models.CharField(max_length=20, choices=[('IN_HOUSE', 'In House'), ('OUTSOURCED', 'Outsourced')], null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    sla_hours = models.IntegerField(default=48)  # Promised Delivery Contract Windows
    predicted_tat_hours = models.FloatField(null=True, blank=True)
    ai_breach_risk = models.CharField(max_length=20, choices=[('NORMAL', 'Normal'), ('HIGH_RISK', 'High Risk'), ('BREACHED', 'Breached')], default='NORMAL')

    def __str__ (self):
        return f"Order{self.Order_number}-{self.Customer_name}"