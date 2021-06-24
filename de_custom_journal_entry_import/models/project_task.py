# -*- coding: utf-8 -*-

import time
from datetime import datetime
import tempfile
import binascii
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, _
from dateutil import parser

import logging
_logger = logging.getLogger(__name__)
import io
try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class ProjectProject(models.Model):
    _inherit = 'project.project'


class ProjectTask(models.Model):
    _inherit = 'project.task'


    entry_attachment_id = fields.Many2many('ir.attachment', relation="files_rel_project_task_entry",
                                            column1="doc_id",
                                            column2="attachment_id",
                                            string="Entry Attachment")


    is_entry_attachment = fields.Boolean(string='Is Entry Attachment')
    is_entry_processed = fields.Boolean(string='Entry Processed')
    un_processed_entry = fields.Boolean(string='Un-Processed Entry')

    @api.constrains('entry_attachment_id')
    def _check_attachment(self):
        if self.entry_attachment_id:
            self.is_entry_attachment = True
            self.un_processed_entry = True

	
    def action_journal_entry_import(self):
        keys = []
        line_keys = []
        ir_model_fields_obj = self.env['ir.model.fields']
        custom_entry_obj = self.env['account.custom.entry']
        custom_entry_obj_line = self.env['account.custom.entry.line']

        for custom in self:
            if custom.is_entry_processed == False:
                counter = 1
                try:
                    file = str(base64.decodebytes(custom.entry_attachment_id.datas).decode('utf-8'))
                    file_reader = csv.reader(file.splitlines())
                    skip_header = True

                except:
                    raise  UserError('Invalid File Format!')
                count = 0
                for row in file_reader:
                    for row_val in  row:
                        search_field = ir_model_fields_obj.sudo().search([
                            ("model", "=", "account.custom.entry"),
                            ("name", "=", row_val),
                        ], limit=1)
                        # if search_field:
                        keys.append(search_field.name)

                        search_line_field = ir_model_fields_obj.sudo().search([
                            ("model", "=", "account.custom.entry.line"),
                            ("name", "=", row_val),
                        ], limit=1)
                        # if search_line_field:
                        line_keys.append(search_line_field.name)
                    break
                rowvals = []
                vals = {}
                line_vals = {}
                for data_row in file_reader:
                    index = 0
                    i = 0
                    for data_column in data_row:
                        rowvals.append(data_row)
                        search_field = ir_model_fields_obj.sudo().search([
                            ("model", "=", "account.custom.entry"),
                            ("name", "=", keys[i]),
                        ], limit=1)
                        if search_field.ttype == 'many2one':

                            many2one_vals = self.env[str(search_field.relation)].search([('name','=',data_column)], limit=1)

                            vals.update({
                                keys[i]: many2one_vals.id
                            })
                            index = index + 1
                            i = i + 1
                        elif search_field.ttype == 'date':
                            date_parse = parser.parse(data_column)
                            date_vals = date_parse.strftime("%Y-%m-%d")
                            vals.update({
                                keys[i]: date_vals
                            })
                            index = index + 1
                            i = i + 1
                        elif search_field.ttype == 'datetime':
                            datetime_parse = parser.parse(data_column)
                            datetime_vals = datetime_parse.strftime("%Y-%m-%d %H:%M:%S")
                            vals.update({
                                keys[i]: datetime_vals
                            })
                            index = index + 1
                            i = i + 1

                        else:
                            if keys[i] != False:
                                vals.update({
                                        keys[i] : data_column
                                    })
                            index = index + 1
                            i = i + 1

                        search_field_line = ir_model_fields_obj.sudo().search([
                            ("model", "=", "account.custom.entry.line"),
                            ("name", "=", line_keys[i]),
                        ], limit=1)
                #         if search_field_line:
                #             if search_field_line.ttype == 'many2one':
                #
                #                 many2one_vals = self.env[str(search_field_line.relation)].search([('name', '=', data_column)],
                #                                                                             limit=1)
                #                 # raise UserError(str(search_field_line.name)+ ' '+str(many2one_vals.id)+' '+str(data_column))
                #
                #                 line_vals.update({
                #                     line_keys[i]: many2one_vals.id
                #                 })
                #                 index = index + 1
                #                 i = i + 1
                #
                #             else:
                #                 if line_keys[i] != False:
                #                     line_vals.update({
                #                         line_keys[i]: data_column
                #                     })
                #                 index = index + 1
                #                 i = i + 1
                # raise UserError(str(vals) +' '+str(line_keys))
                custom_entry_obj.create(vals)
                custom_entry_obj_line.create(line_vals)


                custom.is_entry_processed = True
                custom.un_processed_entry = False
    
