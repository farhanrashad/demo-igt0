# # -*- coding: utf-8 -*-

from . import config
from . import update
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError
from collections import OrderedDict
from operator import itemgetter
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR

def docs_page_content(flag = 0):
    docs = request.env['documents.document'].search([])

    return {
        'docs': docs,
        'success_flag' : flag,
    }

def paging(data, flag1 = 0, flag2 = 0):        
    if flag1 == 1:
        return config.list12
    elif flag2 == 1:
        config.list12.clear()
    else:
        k = []
        for rec in data:
            for ids in rec:
                config.list12.append(ids.id)  
 
###---------------------------------------#####
        
class DocumentsOrder(http.Controller):
    @http.route('/documents/create/',type="http", website=True, auth='user')
    def payslips_create_template(self, **kw):
        return request.render("de_portal_payslips.create_payslip",docs_page_content())
    
    @http.route('/my/documents/save', type="http", auth="public", website=True)
    def create_payslips(self, **kw):
        payslip_val = {
            'name': kw.get('payslip_name'),
            'number': kw.get('payslip_number'),
            'employee_id': int(kw.get('payslip_emp_id')),
            'struct_id': int(kw.get('payslip_structure_id')),
            'date_from':kw.get('date_start'),
            'date_to': kw.get('date_end'),
        }
        record = request.env['hr.payslip'].sudo().create(payslip_val)

        success_flag = 1
        return request.render("de_portal_material_requisition.create_payslip", docs_page_content(success_flag))

###---------------------------------------####

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'docs_count' in counters:
            values['docs_count'] = request.env['documents.document'].search_count([])
        return values
  
    def _docs_get_page_view_values(self,docs, next_id = 0,pre_id= 0, docs_user_flag = 0, access_token = None, **kwargs):
        values = {
            'page_name' : 'docs',
            'docs' : docs,
            'docs_user_flag': docs_user_flag,
            'next_id' : next_id,
            'pre_id' : pre_id,
        }
        return self._get_page_view_values(docs, access_token, values, 'my_docs_history', False, **kwargs)

    @http.route(['/docs/orders', '/docs/orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_docs(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                         search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'id': {'label': _('Default'), 'order': 'id asc'},
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name desc' },
            'update': {'label': _('Last Update'), 'order': 'write_date desc'},
        }
                                                
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('state', 'in', ['draft', 'ongoing','in_progress','done','cancel'])]},
            'draft': {'label': _('Draft'), 'domain': [('state', '=', 'draft')]},
            'ongoing': {'label': _('Ongoing'), 'domain': [('state', '=', 'ongoing')]},
            'in_progress': {'label': _('Confirmed'), 'domain': [('state', '=', 'in_progress')]},
            'done': {'label': _('Done'), 'domain': [('state', '=', 'done')]},
            'cancel': {'label': _('Rejected'), 'domain': [('state', '=', 'cancel')]},
        }
           
        searchbar_inputs = {
            'id': {'input': 'id', 'label': _('Search in No#')},
            'origin': {'input': 'origin', 'label': _('Source Document')},
            'name': {'input': 'name', 'label': _('Search in Reference')},

        }
        
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }

        project_groups = request.env['documents.document'].search([])

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
#         domain = []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]       

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('id', 'all'):
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            domain += search_domain
 
        docs_count = request.env['documents.document'].search_count(domain)

        pager = portal_pager(
            url="/docs/orders",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'search_in': search_in, 'search': search},
            total=docs_count,
            page=page,
            step=self._items_per_page
        )

        _docs = request.env['documents.document'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_docs_history'] = _docs.ids[:100]

        grouped_docs = [_docs]
                
        paging(0,0,1)
        paging(grouped_docs)
        
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_docs': grouped_docs,
            'page_name': 'docs',
            'default_url': '/docs/orders',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
        })
        return request.render("de_portal_document_upload.portal_my_purchase_docs", values)

   
    @http.route(['/docs/order/<int:move_id>'], type='http', auth="user", website=True)
    def portal_my_docs(self, move_id, access_token=None, **kw):
        values = []

        id = move_id
        try:
            docs_sudo = self._document_check_access('documents.document', move_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        next_id = 0
        pre_id = 0
        docs_user_flag = 0

                
        move_id_list = paging(0,1,0)
        next_next_id = 0
        move_id_list.sort()
        length_list = len(move_id_list)
        length_list = length_list - 1
        if length_list != 0:
            if move_id in move_id_list:
                move_id_loc = move_id_list.index(move_id)
                if move_id_loc == 0:
                    next_id = 1
                    pre_id = 0
                elif move_id_loc == length_list:
                    next_id = 0
                    pre_id = 1
                else:
                    next_id = 1
                    pre_id = 1
        else:
            next_id = 0
            pre_id = 0

        values = self._docs_get_page_view_values(docs_sudo,next_id, pre_id, docs_user_flag,access_token, **kw)
        return request.render("de_portal_document_upload.portal_my_docs", values)

    @http.route(['/docs/order/next/<int:move_id>'], type='http', auth="user", website=True)
    def portal_my_next_docs(self, move_id, access_token=None, **kw):
        
        move_id_list = paging(0,1,0)
        next_next_id = 0
        move_id_list.sort()
        
        length_list = len(move_id_list)
        if length_list == 0:
            return request.redirect('/my')
        length_list = length_list - 1
        
        if move_id in move_id_list:
            move_id_loc = move_id_list.index(move_id)
            next_next_id = move_id_list[move_id_loc + 1] 
            next_next_id_loc = move_id_list.index(next_next_id)
            if next_next_id_loc == length_list:
                next_id = 0
                pre_id = 1
            else:
                next_id = 1
                pre_id = 1      
        else:
            buffer_larger = 0
            buffer_smaller = 0
            buffer = 0
            for ids in move_id_list:
                if ids < move_id:
                    buffer_smaller = ids
                if ids > move_id:
                    buffer_smaller = ids
                if buffer_larger and buffer_smaller:
                    break
            if buffer_larger:
                next_next_id = buffer_smaller
            elif buffer_smaller:
                next_next_id = buffer_larger
                
            next_next_id_loc = move_id_list.index(next_next_id)
            length_list = len(move_id_list)
            length_list = length_list + 1
            if next_next_id_loc == length_list:
                next_id = 0
                pre_id = 1
            elif next_next_id_loc == 0:
                next_id = 1
                pre_id = 0
            else:
                next_id = 1
                pre_id = 1
         
        values = []

        id = move_id
        try:
            docs_sudo = self._document_check_access('documents.document', next_next_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        

        docs_user_flag = 0


        values = self._docs_get_page_view_values(docs_sudo,next_id, pre_id, access_token, **kw)
        return request.render("de_portal_document_upload.portal_my_docs", values)

  
    @http.route(['/docs/order/pre/<int:move_id>'], type='http', auth="user", website=True)
    def portal_my_pre_docs(self, move_id, access_token=None, **kw):
        
        move_id_list = paging(0,1,0)
        pre_pre_id = 0
        move_id_list.sort()
        length_list = len(move_id_list)
    
        if length_list == 0:
            return request.redirect('/my')
        
        length_list = length_list - 1
        if move_id in move_id_list:
            move_id_loc = move_id_list.index(move_id)
            pre_pre_id = move_id_list[move_id_loc - 1] 
            pre_pre_id_loc = move_id_list.index(move_id)

            if move_id_loc == 1:
                next_id = 1
                pre_id = 0
            else:
                next_id = 1
                pre_id = 1      
        else:
            buffer_larger = 0
            buffer_smaller = 0
            buffer = 0
            for ids in move_id_list:
                if ids < move_id:
                    buffer_smaller = ids
                if ids > move_id:
                    buffer_smaller = ids
                if buffer_larger and buffer_smaller:
                    break
            if buffer_smaller:
                pre_pre_id = buffer_smaller
            elif buffer_larger:
                pre_pre_id = buffer_larger
                
            pre_pre_id_loc = move_id_list.index(pre_pre_id)
            length_list = len(move_id_list)
            length_list = length_list -1
            if pre_pre_id_loc == 0:
                next_id = 1
                pre_id = 0
            elif pre_pre_id_loc == length_list:
                next_id = 0
                pre_id = 1
            else:
                next_id = 1
                pre_id = 1
   
        values = []

        id = pre_pre_id
        try:
            docs_sudo = self._document_check_access('documents.document', pre_pre_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        

        docs_user_flag = 0


        values = self._docs_get_page_view_values(docs_sudo, next_id,pre_id, access_token, **kw)
        return request.render("de_portal_document_upload.portal_my_docs", values)

    