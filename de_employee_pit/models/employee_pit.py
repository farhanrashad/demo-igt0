from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime


class EmployeePIT(models.Model):
    _name = 'employee.pit'
    _description = 'Employee Pit model'

    def unlink(self):
        for r in self:
            if r.state == 'confirmed' or r.state == 'cancelled' or r.state == 'closed':
                raise UserError(
                    "Employee PIT records which are set to Confirmed/Cancelled/Closed can't be deleted!")
        return super(EmployeePIT, self).unlink()

    @api.model
    def create(self, values):
        if values.get('employee_pit', _('New')) == _('New'):
            values['employee_pit'] = self.env['ir.sequence'].next_by_code('employee.pit.employee_pit') or _('New')
        return super(EmployeePIT, self).create(values)

    crnt_year = fields.Integer(string="Current Year", default=datetime.now().year)
    employee_pit = fields.Char('Name', required=True, copy=False, readonly=True, index=True,
                               default=lambda self: _('New'))
    name = fields.Char('Name')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='State', index=True, copy=False, default='draft', track_visibility='onchange')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_close(self):
        self.state = 'closed'

    def action_cancel(self):
        self.state = 'cancelled'

    current_date = date.today()
    end_date = current_date + timedelta(days=30)

    employee_id = fields.Many2one('hr.employee', string="Employee")
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id')
    #     wage = fields.Many2one('hr.contract', string="Contract Wage", related='employee_id.contract_id.wage')
    marital_stat = fields.Selection(string="Marital Status", related='employee_id.marital')
    no_of_dependant = fields.Integer(string="No. of Dependants", compute='_compute_dependant_count')
    no_of_children = fields.Integer(string="No. of Children", related='employee_id.children')
    #     dependant_id = fields.Many2one('hr.employee.family', related='employee_family_ids.relation_ship')
    father = fields.Boolean(string="Father")
    mother = fields.Boolean(string="Mother")

    employee_pit_ids = fields.One2many


#     record = self.env['hr.employee.family'].search([('employee_id', '=' , 'id' )])
#     for rec in record:

#         @api.depends('employee_family_ids')
#         def _compute_dependant_count(self):
#             count = 0
#             for rec in self:
#                 if rec.employee_family_ids:
#                     for line in rec.employee_family_ids:
#                         count = count + 1
#                     rec.no_of_dependant = count
#                 else:
#                     rec.no_of_dependant = count

class EmployeePIT(models.Model):
    _name = 'employee.pit.line'

    months = fields.Date('Months')
#     datetime.strftime(datetime.strptime(months, "%Y-%m-%d"), %m)