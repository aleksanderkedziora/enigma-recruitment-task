import datetime

from celery import shared_task

from apps.orders.mail import OrderConfirmationEmail, PaymentRemindEmail


@shared_task(serializer='json', name="send_confirmation_email")
def send_confirmation_email(*, order_number, to_email):
    OrderConfirmationEmail(order_number=order_number, to_email=to_email).send()


@shared_task(serializer='json', name="send_payment_remind_email")
def send_payment_remind_email():
    from apps.orders.models import Order

    one_day_from_now = datetime.date.today() + datetime.timedelta(days=5)

    for order in Order.objects.filter(payment_date=one_day_from_now):
        PaymentRemindEmail(order_number=order.id, to_email=order.client.email).send()

    return 'Remind mails sent'
