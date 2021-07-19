from odoo.osv import osv
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
from odoo import api, fields, models, _, tools


class ProductCarouselData(osv.osv):
    _name = 'product.carousel.data'
    _description = 'Product Carousel Data'
    _carousel_data = True

    def get_product_carousel_filter_product_data(self, filter_id, context=None):
        res = {
            'domain': [],
            'model': self._name,
            'order': False
        }
        if context is None:
            context = {}

        if filter_id:
            filter_product_data = request.env['website.product.filter'].sudo().browse(filter_id)
            res['domain'] = safe_eval(filter_product_data.filter_id.domain, {'uid': request.uid})
            res['model'] = filter_product_data.filter_id.model_id
            res['name'] = filter_product_data.name
        else:
            res['model'] = 'product.template'
        return res

    def get_product_carousel_slider(self, filter_id, limit, context=None):
        filter_product_data = self.get_product_carousel_filter_product_data(filter_id, context)
        if filter_product_data:
            product_ids = request.env[filter_product_data['model']].sudo().search(filter_product_data['domain'],limit=limit,
                                                                                  order=filter_product_data['order'], )
            return {'all_products': product_ids,
                    'name': 'name' in filter_product_data and filter_product_data['name'] or _("All")}
