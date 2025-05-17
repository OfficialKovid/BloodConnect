from django.db import models
import random
import string
from django.utils import timezone
from datetime import date

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('FULFILLED', 'Fulfilled'),
        ('EXPIRED', 'Expired'),
    ]
    reference_number = models.CharField(max_length=8, unique=True)
    patient_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=3)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    required_date = models.DateField()
    additional_notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    is_fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_reference_number(self):
        chars = string.ascii_uppercase + string.digits
        while True:
            reference = ''.join(random.choices(chars, k=8))
            if not BloodRequest.objects.filter(reference_number=reference).exists():
                return reference

    @property
    def is_expired(self):
        return self.required_date < date.today()

    @property
    def current_status(self):
        """
        Returns the current status based on fulfillment and expiration,
        updates the database if status has changed
        """
        if self.is_fulfilled:
            if self.status != 'FULFILLED':
                self.status = 'FULFILLED'
                self.save(update_fields=['status'])
            return 'FULFILLED'
        
        if self.required_date < date.today():
            if self.status != 'EXPIRED':
                self.status = 'EXPIRED'
                self.save(update_fields=['status'])
            return 'EXPIRED'
        
        return 'PENDING'

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
        if not kwargs.get('update_fields'):  # Only update status if not doing a partial update
            self.status = self.current_status
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Request {self.reference_number} - {self.patient_name} ({self.current_status})"
