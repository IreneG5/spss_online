import arrow
import models


def subscription_created(sender, **kwargs):
    ipn_obj = sender
    product_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]
    product_bought = models.Product.objects.get(id=product_id)
    if product_bought.license_type[0]==1:
        license_end = arrow.now().replace(years=+1).datetime
    else:
        license_end = arrow.now().replace(years=+2).datetime

    models.Purchase.objects.create(product_id=product_id, user_id=user_id,
                            license_end=license_end)


def subscription_was_cancelled(sender, **kwargs):
    ipn_obj = sender
    product_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]
    purchase = models.Purchase.objects.get(user_id=user_id, product_id=product_id)
    purchase.license_end = arrow.now().datetime
    purchase.save()
