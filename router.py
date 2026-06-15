from .models import LensStock

def assign_inventory_source(order):
    """
    Scans physical database rows to verify lens component match options.
    Deducts stock on success or redirects parameters to vendor processing paths.
    """
    try:
        right_lens = LensStock.objects.get(
            sphere = order.od_sphere,
            cylinder = order.os_cylinder,
            lens_type = order.lens_type
        )

        left_lens = LensStock.objects.get(
            sphere = order.od_sphere,
            cylinder = order.od_cylinder,
            lens_type = order.lens_type
        )

        if right_lens.quantity > 0 and left_lens.quantity > 0:
            order.inventory_source = 'IN_HOUSE'

            right_lens.quantity -= 1
            left_lens.quantity -= 1
            right_lens.save()
            left_lens.save()

        else:
            order.inventory_source = 'OUTSOURCED'

    except LensStock.DoesNotExist:
        order.inventory_source = 'OUTSOURCED'

    order.save()