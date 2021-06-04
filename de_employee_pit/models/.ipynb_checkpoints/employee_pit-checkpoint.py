from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime


class EmployeeIncomeTax(models.Model):
    _name = 'employee.income.tax'
    _description = 'Employee PIT model'

    def unlink(self):
        for r in self:
            if r.state == 'confirmed' or r.state == 'cancelled' or r.state == 'closed':
                raise UserError(
                    "Employee PIT records which are set to Confirmed/Cancelled/Closed can't be deleted!")
        return super(EmployeeIncomeTax, self).unlink()

    @api.model
    def create(self, values):
        if values.get('employee_pit', _('New')) == _('New'):
            values['employee_pit'] = self.env['ir.sequence'].next_by_code('employee.income.tax.employee_pit') or _(
                'New')
        return super(EmployeeIncomeTax, self).create(values)

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
    wage = fields.Float(string="Contract Wage", compute='employee_count')
    marital_stat = fields.Selection(string="Marital Status", related='employee_id.marital')
    no_of_dependant = fields.Integer(string="No. of Dependants", compute='employee_count')
    no_of_children = fields.Integer(string="No. of Children", related='employee_id.children', compute='employee_count')
    father = fields.Boolean(string="Father")
    mother = fields.Boolean(string="Mother")
    annual_wage = fields.Float(string="Annual Wage", compute='employee_count')
    tax_income = fields.Float(string="Tax Income")

    employee_income_tax_ids = fields.One2many('employee.income.tax.line', 'employee_income_tax_id')

    @api.onchange("employee_id")
    def compute_wage(self):
        list_months=['jan','feb']
        for i in range(len(list_months)):
            vals = {
                'months': list_months[i],
                'employee_income_tax_id': self.id
                }
            self.employee_income_tax_ids.create(vals)
            
        
        
                
                
    def employee_count(self):
        for rec in self:
            count = 0
            if rec.employee_id:
                if rec.employee_id.contract_id:
                    for contract in rec.employee_id.contract_id:
                        if contract.state == 'open':
                            rec.wage = contract.wage 
                            rec.annual_wage = contract.wage * 12 
                        else:
                            rec.wage = 0
                            rec.annual_wage = 0
                else:
                    rec.wage = 0
                    rec.annual_wage = 0
        
        
                if rec.employee_income_tax_ids:
                    for line in rec.employee_income_tax_ids:
            line.unlink()
                
                if rec.employee_id.employee_family_ids:
                    for dependant in rec.employee_id.employee_family_ids:
                        if dependant.relation_ship == "father":
                            rec.father = True
#                         if dependant.relation_ship == "mother":
#                             rec.mother = True
                        if dependant.relation_ship == "child":
                            rec.child = True
                        count = count + 1
                    rec.no_of_dependant = count
            

class EmployeeIncomeTaxLine(models.Model):
    _name = 'employee.income.tax.line'

    employee_income_tax_id = fields.Many2one('employee.income.tax')
    months = fields.Char('Months')
    month_salary = fields.Float(string="Month Salary")
    month_tax = fields.Float(string="Monthly Tax")
