# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class ServerActions(models.Model):
    """ Add email option in server actions. """
    _inherit = 'ir.actions.server'

    @api.model
    def run_action_email(self, action, eval_context=None):
        # TDE CLEANME: when going to new api with server action, remove action
        if not action.template_id or not self._context.get('active_id'):
            return False
        # Clean context from default_type to avoid making attachment
        # with wrong values in subsequent operations
        cleaned_ctx = dict(self.env.context)
        cleaned_ctx.pop('default_type', None)

        # Custom Code starts here
        action.template_id.with_context(cleaned_ctx).send_mail(self._context.get('active_id'), force_send=True, raise_exception=False)
        # custom Code ends here

        return False
