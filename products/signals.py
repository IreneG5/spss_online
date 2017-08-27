import arrow
import models


def subscription_created(sender, **kwargs):
    ipn_obj = sender
    product_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]

    # if Product.license_type == "1 year":
    #    license_time = 12
    # elif Product.license_type == "2 years":
    #    license_time = 24
    # else:
    #    license_time = 999999

    models.Purchase.object.create(product_id=product_id, user_id=user_id,
                            license_end=arrow.now().replace(months=+12).datetime)


def subscription_was_cancelled(sender, **kwargs):

    ipn_obj = sender
    product_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]
    purchase = models.Purchase.object.get(user_id=user_id, product_id=product_id)
    purchase.license_end = arrow.now().datetime
    purchase.save()
