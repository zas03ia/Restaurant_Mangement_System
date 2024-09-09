import stripe


def create_payment(request, amount, payment_method_id):
    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount
            currency="bdt",  # Currency set to taka
            payment_method=payment_method_id,  # Payment method ID from front end
            confirm=True,  # Auto-confirm the payment
        )

        return intent

    except stripe.error.CardError as e:
        # Raise Stripe CardError
        raise e
    except Exception as e:
        # Raise any other exceptions
        raise e
