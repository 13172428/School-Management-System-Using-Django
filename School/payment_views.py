# School/payment_views.py
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        student = request.user.student
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            client_reference_id = student.id,
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': 1500000,   # ₹15,000
                    'product_data': {'name': f'Fee for {student.user.get_full_name()}'},
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url = request.build_absolute_uri(reverse('fee_success')),
            cancel_url  = request.build_absolute_uri(reverse('student_dashboard')),
        )
        return redirect(session.url)
