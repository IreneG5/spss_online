import arrow
import models


def subscription_created(sender, **kwargs):
    ipn_obj = sender
    product_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]

    # Get the last purchase and calculate the purchase date
    last_purchase = models.Purchase.objects.last()
    year = last_purchase.license_end.year - int(last_purchase.product.license_type[0])
    last_purchase_date=last_purchase.license_end.replace(year=year)
    # print "STATUS: %s" % ipn_obj.payment_status
    # print ipn_obj.pending_reason
    # print "User: %s" % last_purchase.user_id
    # print "User: %s" % user_id
    # print "Product: %s" % last_purchase.product_id
    # print "Product: %s" % product_id

    if ipn_obj.payment_status == "Completed":
        # print "COMPLETED"
        # Check if the receiver's email and the purchase amount are correct
        if ipn_obj.receiver_email != 'irene.g5555-easySPSS1@gmail.com':
            # print "Receiver's emails don't match"
            return

        if ipn_obj.mc_gross != last_purchase.product.price or ipn_obj.mc_currency != 'GBP':
            # # print "Amounts don't match"
            return

        # Check if the purchase was already saved in the database (duplicate signal), and if not, save it
        if int(last_purchase.user_id) == int(user_id) and int(last_purchase.product_id) == int(product_id):
            # # print "last: %s" % last_purchase_date
            # # print "arrow: %s" % arrow.utcnow().replace(seconds=-60).datetime
            if last_purchase_date > arrow.utcnow().replace(seconds=-60).datetime:
                # # print "already created"
                return

        print "saving purchase"
        license_duration = int(models.Product.objects.get(pk=product_id).license_type[0])
        models.Purchase.objects.create(product_id=product_id, user_id=user_id, license_end=arrow.now().
                                       replace(years=+license_duration,tzinfo='Europe/London').datetime)


# # This function is not being called, signal from Paypal has changed
# # def subscription_was_cancelled(sender, **kwargs):
# #    ipn_obj = sender
# #    product_id = ipn_obj.custom.split('-')[0]
# #    user_id = ipn_obj.custom.split('-')[1]
# #    purchase = models.Purchase.objects.get(user_id=user_id, product_id=product_id)
# #    purchase.license_end = arrow.now().datetime
# #    purchase.save()
