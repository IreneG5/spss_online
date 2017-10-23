import arrow
import models


def subscription_created(sender, **kwargs):
    """
    Create new purchase instance.
    Check if PayPal purchase was successful (ipn_obj),
    if the amounts and the emails match and is not a duplicate
    and save the details in a new purchase instance
    """
    ipn_obj = sender
    product_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]

    # Get the last purchase and calculate the purchase date
    last_purchase = models.Purchase.objects.last()
    year = last_purchase.license_end.year - int(last_purchase.product.license_type[0])
    last_purchase_date = last_purchase.license_end.replace(year=year)

    if ipn_obj.payment_status == "Completed":
        # Check if the receiver's email and the purchase amount are correct
        if ipn_obj.receiver_email != 'irene.g5555-easySPSS1@gmail.com':
            return

        # Check if amount's don't match
        if ipn_obj.mc_gross != last_purchase.product.price or ipn_obj.mc_currency != 'GBP':
            return

        # Check if the purchase was already saved in the database (duplicate signal), and if not, save it
        if int(last_purchase.user_id) == int(user_id) and int(last_purchase.product_id) == int(product_id):
            if last_purchase_date > arrow.utcnow().replace(seconds=-60).datetime:
                return

        license_duration = int(models.Product.objects.get(pk=product_id).license_type[0])
        models.Purchase.objects.create(product_id=product_id, user_id=user_id, license_end=arrow.now().
                                       replace(years=+license_duration, tzinfo='Europe/London').datetime)
