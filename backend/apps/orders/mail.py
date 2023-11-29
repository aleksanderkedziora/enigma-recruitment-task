from abc import ABC, abstractmethod

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class AbstractEmail(ABC):
    def __init__(self, to_email: str, from_email: str = settings.DEFAULT_FROM_EMAIL):
        self.subject = None
        self.to_email = to_email
        self.from_email = from_email
        self.text_content = None
        self.html_content = None

    @abstractmethod
    def set_subject(self):
        pass

    @abstractmethod
    def set_text_content(self):
        pass

    def build(self):
        self.set_subject()
        self.set_text_content()

        email = EmailMultiAlternatives(
            self.subject,
            self.text_content,
            self.from_email,
            [self.to_email],
        )

        return email

    def send(self):
        email = self.build()
        email.send()


class OrderConfirmationEmail(AbstractEmail):
    def __init__(self, *, order_number, to_email):
        super().__init__(to_email)
        self.order_number = order_number

    def set_subject(self):
        self.subject = f"Order Confirmation #{self.order_number}"

    def set_text_content(self):
        self.text_content = f"Thank you for your order #{self.order_number}."


class PaymentRemindEmail(AbstractEmail):
    def __init__(self, *, order_number, to_email):
        super().__init__(to_email)
        self.order_number = order_number

    def set_subject(self):
        self.subject = f"Payment Reminder - Order #{self.order_number}"

    def set_text_content(self):
        self.text_content = f"One day left to pay for #{self.order_number} order."
