# myapp/signals.py

from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from .Models import Payment

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        try:
            # Look for the corresponding payment by transaction ID
            payment = Payment.objects.get(transaction_id=ipn_obj.txn_id)
            payment.complete_payment(ipn_obj.txn_id)  # Mark payment as complete
        except Payment.DoesNotExist:
            # Handle case where payment doesn't exist
            pass
