# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/product_pricelist/'], type="json", auth="public", website=True)
    def product_pricelist(self, product=None, combination=None, **post):
        if int(product) != 0:
            product = request.env['product.product'].browse(int(product))

            pricelist_id = request.website.get_current_pricelist()
            pricelist = request.env['product.pricelist'].browse(int(pricelist_id or 0))
            #base_pricelist = request.env['product.pricelist'].search([('base_pricelist_id.id', '=', pricelist_id)])
            
            pricelist_item_ids = variant_id = request.env['product.pricelist.item'].search(
                [('product_id', '=', product.id),
                 ('pricelist_id', '=', pricelist.id)],order="min_quantity")
            if not variant_id:
                pricelist_item_ids = request.env['product.pricelist.item'].search(
                    [('product_tmpl_id', '=', product.product_tmpl_id.id),
                     ('pricelist_id', '=', pricelist.id)],order="min_quantity")

            currency = request.website.currency_id
            items = []
            if pricelist_item_ids:
                for pricelist_item in pricelist_item_ids:
                    if currency.id == pricelist_item.currency_id.id:
                        if pricelist_item.date_start:
                            date_start = datetime.strptime(
                                pricelist_item.date_start, '%Y-%m-%d').date()
                        if pricelist_item.date_end:
                            date_end = datetime.strptime(
                                pricelist_item.date_end, '%Y-%m-%d').date()
                        current_date = date.today()

                        if pricelist_item.date_start and not pricelist_item.date_end:
                            if current_date >= date_start:
                                if pricelist_item.compute_price == 'fixed':
                                    if pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'before':
                                        items.append(
                                            {'quantity': pricelist_item.min_quantity, 'price': pricelist_item.currency_id.symbol + str(round(pricelist_item.fixed_price or 0, 2))})
                                    elif pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'after':
                                        items.append({'quantity': pricelist_item.min_quantity, 'price': str(
                                            round(pricelist_item.fixed_price or 0, 2)) + pricelist_item.currency_id.symbol})

                                elif pricelist_item.compute_price == 'formula' or pricelist_item.compute_price == 'percentage':
                                    products = request.env['product.product'].with_context(
                                        {'quantity': pricelist_item.min_quantity}).browse(product.id)
                                    data = product.product_tmpl_id._get_first_possible_combination()
                                    main_v = product.product_tmpl_id._get_combination_info(
                                        data, add_qty=pricelist_item.min_quantity or 1, pricelist=pricelist)
                                    if pricelist_item.min_quantity > 0:
                                        price_dict = {
                                            'product_price': main_v.get('price')}
                                        if pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': pricelist_item.min_quantity, 'price': pricelist_item.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                        elif pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'after':
                                            items.append({'quantity': pricelist_item.min_quantity, 'price': str(
                                                round(price_dict.get('product_price') or 0, 2)) + pricelist_item.currency_id.symbol})

                        elif not pricelist_item.date_start and pricelist_item.date_end:
                            if current_date <= date_end:
                                if pricelist_item.compute_price == 'fixed':
                                    if pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'before':
                                        items.append(
                                            {'quantity': pricelist_item.min_quantity, 'price': pricelist_item.currency_id.symbol + str(round(pricelist_item.fixed_price or 0, 2))})
                                    elif pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'after':
                                        items.append({'quantity': pricelist_item.min_quantity, 'price': str(
                                            round(pricelist_item.fixed_price or 0, 2)) + pricelist_item.currency_id.symbol})

                                elif pricelist_item.compute_price == 'formula' or pricelist_item.compute_price == 'percentage':
                                    products = request.env['product.product'].with_context(
                                        {'quantity': pricelist_item.min_quantity}).browse(product.id)
                                    ProductTemplate = request.env['product.template']
                                    combination_p = request.env['product.template.attribute.value'].browse(
                                        combination)
                                    main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                        combination_p, int(product or 0), int(pricelist_item.min_quantity or 1), pricelist)
                                    if pricelist_item.min_quantity > 0:
                                        price_dict = {
                                            'product_price': main_v.get('price')}
                                        if pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': pricelist_item.min_quantity, 'price': pricelist_item.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                        elif pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'after':
                                            items.append({'quantity': pricelist_item.min_quantity, 'price': str(
                                                round(price_dict.get('product_price') or 0, 2)) + pricelist_item.currency_id.symbol})

                        elif pricelist_item.date_start and pricelist_item.date_end:
                            if current_date >= date_start and current_date <= date_end:
                                if pricelist_item.compute_price == 'fixed':
                                    if pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'before':
                                        items.append(
                                            {'quantity': pricelist_item.min_quantity, 'price': pricelist_item.currency_id.symbol + str(round(pricelist_item.fixed_price or 0, 2))})
                                    elif pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'after':
                                        items.append({'quantity': pricelist_item.min_quantity, 'price': str(
                                            round(pricelist_item.fixed_price or 0, 2)) + pricelist_item.currency_id.symbol})

                                elif pricelist_item.compute_price == 'formula' or pricelist_item.compute_price == 'percentage':
                                    products = request.env['product.product'].with_context(
                                        {'quantity': pricelist_item.min_quantity}).browse(product.id)
                                    ProductTemplate = request.env['product.template']
                                    combination_p = request.env['product.template.attribute.value'].browse(
                                        combination)
                                    main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                        combination_p, int(product or 0), int(pricelist_item.min_quantity or 1), pricelist)
                                    if pricelist_item.min_quantity > 0:
                                        price_dict = {
                                            'product_price': main_v.get('price')}
                                        if pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': pricelist_item.min_quantity, 'price': pricelist_item.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                        elif pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'after':
                                            items.append({'quantity': pricelist_item.min_quantity, 'price': str(
                                                round(price_dict.get('product_price') or 0, 2)) + pricelist_item.currency_id.symbol})
                        else:
                            if pricelist_item.compute_price == 'fixed':
                                if pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'before':
                                    items.append(
                                        {'quantity': pricelist_item.min_quantity, 'price': pricelist_item.currency_id.symbol + str(round(pricelist_item.fixed_price or 0, 2))})
                                elif pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'after':
                                    items.append({'quantity': pricelist_item.min_quantity, 'price': str(
                                        round(pricelist_item.fixed_price or 0, 2)) + pricelist_item.currency_id.symbol})

                            elif pricelist_item.compute_price == 'formula' or pricelist_item.compute_price == 'percentage':
                                products = request.env['product.product'].with_context(
                                    {'quantity': pricelist_item.min_quantity}).browse(product.id)
                                # data = product.product_tmpl_id._get_first_possible_combination()

                                # main_v = product.product_tmpl_id._get_combination_info(
                                #     data, add_qty=pricelist_item.min_quantity or 1, pricelist=pricelist)
                                ProductTemplate = request.env['product.template']
                                combination_p = request.env['product.template.attribute.value'].browse(
                                    combination)
                                main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                    combination_p, int(product or 0), int(pricelist_item.min_quantity or 1), pricelist)
                                # print('\n\n\n\n\n==my===========', my)

                                if pricelist_item.min_quantity > 0:
                                    price_dict = {
                                        'product_price': main_v.get('price')}
                                    if pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'before':
                                        items.append(
                                            {'quantity': pricelist_item.min_quantity, 'price': pricelist_item.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                    elif pricelist_item.currency_id and pricelist_item.currency_id.position and pricelist_item.currency_id.position == 'after':
                                        items.append({'quantity': pricelist_item.min_quantity, 'price': str(
                                            round(price_dict.get('product_price') or 0, 2)) + pricelist_item.currency_id.symbol})

                pricelist_items = {'pricelist_items': items}
                res = request.env['ir.ui.view'].render_template(
                    'product_tiered_pricing.web_pricelist', pricelist_items)
                return res
            elif pricelist and not pricelist_item_ids and pricelist.item_ids:
                flag = 0
                for data in pricelist.item_ids:
                    if data.applied_on == '2_product_category':

                        product_id = request.env['product.product'].sudo(
                        ).search([('id', '=', int(product.id)), ('categ_id', '=', int(data.categ_id.id))])

                        if currency.id == data.currency_id.id and product_id:
                            if data.date_start:
                                date_start = datetime.strptime(
                                    data.date_start, '%Y-%m-%d').date()
                            if data.date_end:
                                date_end = datetime.strptime(
                                    data.date_end, '%Y-%m-%d').date()
                            current_date = date.today()

                            if data.date_start and not data.date_end:
                                if current_date >= date_start:
                                    if data.compute_price == 'fixed':
                                        if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(data.fixed_price or 0, 2))})
                                        elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                            items.append({'quantity': data.min_quantity, 'price': str(
                                                round(data.fixed_price or 0, 2)) + data.currency_id.symbol})

                                    elif data.compute_price == 'formula' or data.compute_price == 'percentage':
                                        products = request.env['product.product'].with_context(
                                            {'quantity': data.min_quantity}).browse(product.id)
                                        # row = product.product_tmpl_id._get_first_possible_combination()
                                        # main_v = product.product_tmpl_id._get_combination_info(
                                        #     row, add_qty=data.min_quantity or 1, pricelist=pricelist)

                                        ProductTemplate = request.env['product.template']
                                        combination_p = request.env['product.template.attribute.value'].browse(
                                            combination)
                                        main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                            combination_p, int(product or 0), int(data.min_quantity or 1), pricelist)
                                        if data.min_quantity > 0:
                                            price_dict = {
                                                'product_price': main_v.get('price')}
                                            if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                                items.append(
                                                    {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                            elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                                items.append({'quantity': data.min_quantity, 'price': str(
                                                    round(price_dict.get('product_price') or 0, 2)) + data.currency_id.symbol})

                            elif not data.date_start and data.date_end:
                                if current_date <= date_end:
                                    if data.compute_price == 'fixed':
                                        if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(data.fixed_price or 0, 2))})
                                        elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                            items.append({'quantity': data.min_quantity, 'price': str(
                                                round(data.fixed_price or 0, 2)) + data.currency_id.symbol})

                                    elif data.compute_price == 'formula' or data.compute_price == 'percentage':
                                        products = request.env['product.product'].with_context(
                                            {'quantity': data.min_quantity}).browse(product.id)
                                        ProductTemplate = request.env['product.template']
                                        combination_p = request.env['product.template.attribute.value'].browse(
                                            combination)
                                        main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                            combination_p, int(product or 0), int(data.min_quantity or 1), pricelist)
                                        if data.min_quantity > 0:
                                            price_dict = {
                                                'product_price': main_v.get('price')}
                                            if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                                items.append(
                                                    {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                            elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                                items.append({'quantity': data.min_quantity, 'price': str(
                                                    round(price_dict.get('product_price') or 0, 2)) + data.currency_id.symbol})

                            elif data.date_start and data.date_end:
                                if current_date >= date_start and current_date <= date_end:
                                    if data.compute_price == 'fixed':
                                        if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(data.fixed_price or 0, 2))})
                                        elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                            items.append({'quantity': data.min_quantity, 'price': str(
                                                round(data.fixed_price or 0, 2)) + data.currency_id.symbol})

                                    elif data.compute_price == 'formula' or data.compute_price == 'percentage':
                                        products = request.env['product.product'].with_context(
                                            {'quantity': data.min_quantity}).browse(product.id)
                                        ProductTemplate = request.env['product.template']
                                        combination_p = request.env['product.template.attribute.value'].browse(
                                            combination)
                                        main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                            combination_p, int(product or 0), int(data.min_quantity or 1), pricelist)
                                        if data.min_quantity > 0:
                                            price_dict = {
                                                'product_price': main_v.get('price')}
                                            if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                                items.append(
                                                    {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                            elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                                items.append({'quantity': data.min_quantity, 'price': str(
                                                    round(price_dict.get('product_price') or 0, 2)) + data.currency_id.symbol})

                            else:
                                if data.compute_price == 'fixed':
                                    if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                        items.append(
                                            {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(data.fixed_price or 0, 2))})
                                    elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                        items.append({'quantity': data.min_quantity, 'price': str(
                                            round(data.fixed_price or 0, 2)) + data.currency_id.symbol})

                                elif data.compute_price == 'formula' or data.compute_price == 'percentage':
                                    products = request.env['product.product'].with_context(
                                        {'quantity': data.min_quantity}).browse(product.id)
                                    ProductTemplate = request.env['product.template']
                                    combination_p = request.env['product.template.attribute.value'].browse(
                                        combination)
                                    main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                        combination_p, int(product or 0), int(data.min_quantity or 1), pricelist)
                                    if data.min_quantity > 0:
                                        price_dict = {
                                            'product_price': main_v.get('price')}
                                        if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                        elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                            items.append({'quantity': data.min_quantity, 'price': str(
                                                round(price_dict.get('product_price') or 0, 2)) + data.currency_id.symbol})
                        if items:
                            flag = 1

                    elif data.applied_on == '3_global' and flag == 0:
                        if currency.id == data.currency_id.id:
                            if data.date_start:
                                date_start = datetime.strptime(
                                    data.date_start, '%Y-%m-%d').date()
                            if data.date_end:
                                date_end = datetime.strptime(
                                    data.date_end, '%Y-%m-%d').date()
                            current_date = date.today()

                            if data.date_start and not data.date_end:
                                if current_date >= date_start:
                                    if data.compute_price == 'fixed':
                                        if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(data.fixed_price or 0, 2))})
                                        elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                            items.append({'quantity': data.min_quantity, 'price': str(
                                                round(data.fixed_price or 0, 2)) + data.currency_id.symbol})

                                    elif data.compute_price == 'formula' or data.compute_price == 'percentage':
                                        products = request.env['product.product'].with_context(
                                            {'quantity': data.min_quantity}).browse(product.id)
                                        # row = product.product_tmpl_id._get_first_possible_combination()
                                        # main_v = product.product_tmpl_id._get_combination_info(
                                        #     row, add_qty=row.min_quantity or 1, pricelist=pricelist)

                                        ProductTemplate = request.env['product.template']
                                        combination_p = request.env['product.template.attribute.value'].browse(
                                            combination)
                                        main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                            combination_p, int(product or 0), int(data.min_quantity or 1), pricelist)
                                        if data.min_quantity > 0:
                                            price_dict = {
                                                'product_price': main_v.get('price')}
                                            if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                                items.append(
                                                    {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                            elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                                items.append({'quantity': data.min_quantity, 'price': str(
                                                    round(price_dict.get('product_price') or 0, 2)) + data.currency_id.symbol})

                            elif not data.date_start and data.date_end:
                                if current_date <= date_end:
                                    if data.compute_price == 'fixed':
                                        if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(data.fixed_price or 0, 2))})
                                        elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                            items.append({'quantity': data.min_quantity, 'price': str(
                                                round(data.fixed_price or 0, 2)) + data.currency_id.symbol})

                                    elif data.compute_price == 'formula' or data.compute_price == 'percentage':
                                        products = request.env['product.product'].with_context(
                                            {'quantity': data.min_quantity}).browse(product.id)
                                        ProductTemplate = request.env['product.template']
                                        combination_p = request.env['product.template.attribute.value'].browse(
                                            combination)
                                        main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                            combination_p, int(product or 0), int(data.min_quantity or 1), pricelist)
                                        if data.min_quantity > 0:
                                            price_dict = {
                                                'product_price': main_v.get('price')}
                                            if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                                items.append(
                                                    {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                            elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                                items.append({'quantity': data.min_quantity, 'price': str(
                                                    round(price_dict.get('product_price') or 0, 2)) + data.currency_id.symbol})

                            elif data.date_start and data.date_end:
                                if current_date >= date_start and current_date <= date_end:
                                    if data.compute_price == 'fixed':
                                        if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(data.fixed_price or 0, 2))})
                                        elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                            items.append({'quantity': data.min_quantity, 'price': str(
                                                round(data.fixed_price or 0, 2)) + data.currency_id.symbol})

                                    elif data.compute_price == 'formula' or data.compute_price == 'percentage':
                                        products = request.env['product.product'].with_context(
                                            {'quantity': data.min_quantity}).browse(product.id)
                                        ProductTemplate = request.env['product.template']
                                        combination_p = request.env['product.template.attribute.value'].browse(
                                            combination)
                                        main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                            combination_p, int(product or 0), int(data.min_quantity or 1), pricelist)
                                        if data.min_quantity > 0:
                                            price_dict = {
                                                'product_price': main_v.get('price')}
                                            if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                                items.append(
                                                    {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                            elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                                items.append({'quantity': data.min_quantity, 'price': str(
                                                    round(price_dict.get('product_price') or 0, 2)) + data.currency_id.symbol})
                            else:
                                if data.compute_price == 'fixed':
                                    if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                        items.append(
                                            {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(data.fixed_price or 0, 2))})
                                    elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                        items.append({'quantity': data.min_quantity, 'price': str(
                                            round(data.fixed_price or 0, 2)) + data.currency_id.symbol})

                                elif data.compute_price == 'formula' or data.compute_price == 'percentage':
                                    products = request.env['product.product'].with_context(
                                        {'quantity': data.min_quantity}).browse(product.id)
                                    ProductTemplate = request.env['product.template']
                                    combination_p = request.env['product.template.attribute.value'].browse(
                                        combination)
                                    main_v = ProductTemplate.browse(int(product.product_tmpl_id.id))._get_combination_info(
                                        combination_p, int(product or 0), int(data.min_quantity or 1), pricelist)
                                    if data.min_quantity > 0:
                                        price_dict = {
                                            'product_price': main_v.get('price')}
                                        if data.currency_id and data.currency_id.position and data.currency_id.position == 'before':
                                            items.append(
                                                {'quantity': data.min_quantity, 'price': data.currency_id.symbol + str(round(price_dict.get('product_price') or 0, 2))})
                                        elif data.currency_id and data.currency_id.position and data.currency_id.position == 'after':
                                            items.append({'quantity': data.min_quantity, 'price': str(
                                                round(price_dict.get('product_price') or 0, 2)) + data.currency_id.symbol})
                pricelist_items = {'pricelist_items': items}
                res = request.env['ir.ui.view'].render_template(
                    'product_tiered_pricing.web_pricelist', pricelist_items)
                return res
            else:
                return None

        else:
            return None
