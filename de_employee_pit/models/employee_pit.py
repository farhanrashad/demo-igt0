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
    marital_stat = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ], string='Marital Status', readonly=True, copy=False, index=True, default='single')
    no_of_dependant = fields.Integer(string="No. of Dependants")
    no_of_children = fields.Integer(string="No. of Children", compute='employee_count')
    father = fields.Boolean(string="Father", readonly=True)
    mother = fields.Boolean(string="Mother", readonly=True)
    child = fields.Boolean(string="Child", readonly=True)
    annual_wage = fields.Float(string="Annual Wage", compute='employee_count')
    tax_income = fields.Float(string="Tax Income", compute='employee_count')
    monthly_tax = fields.Float('Monthly tax amount')
    ss_amount = fields.Float('Social Security Amount')
    
    employee_income_tax_ids = fields.One2many('employee.income.tax.line', 'employee_income_tax_id')
            
        
    @api.onchange('ss_amount','employee_id')
    def employee_count(self):
        count = 0
        parent_count = 0
        tax_per = 0
        tax_total = 0
        wife_count = 0
        child_count =  0
        for rec in self:
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
                
            if rec.employee_id.employee_family_ids:
                for dependant in rec.employee_id.employee_family_ids:
                    if dependant.relation_ship == "father":
                        rec.father = True
                        parent_count = parent_count + 1
                    if dependant.relation_ship == "mother":
                        rec.mother = True
                        parent_count = parent_count + 1
                    if dependant.relation_ship == "child":
                        rec.child = True
                        child_count = rec.no_of_children + 1
                        rec.update({
                            'no_of_children' : child_count,
                        })
                    if dependant.relation_ship == "wife":
                        wife_count = wife_count + 1
                        rec.update({
                            'marital_stat' : 'married',
                        })
                    count = count + 1
            rec.no_of_dependant = count
            rec.no_of_children = child_count
            
            if (rec.annual_wage*0.20) > 10000000:
                rec.tax_income = (rec.annual_wage-10000000) - ((rec.no_of_children * 500000) + (parent_count * 1000000) + (rec.ss_amount*12) + (wife_count * 1000000))
#             if (rec.annual_wage*20) < 10000000:
            else:
                rec.tax_income = (rec.annual_wage*0.80) - ((rec.no_of_children * 500000) + (parent_count * 1000000) + (rec.ss_amount*12) + (wife_count * 1000000))
            
            if rec.tax_income > 1 and rec.tax_income <= 2000000:
                tax_per = 0
            if rec.tax_income > 2000001 and rec.tax_income <= 5000000:
                tax_total = ((rec.tax_income - 2000000)*0.05)
                tax_per = 5
            if rec.tax_income > 5000001 and rec.tax_income <= 10000000:
                tax_total = (((rec.tax_income - 5000000)*0.10)+150000)
                tax_per = 10
            if rec.tax_income > 10000001 and rec.tax_income <= 20000000:
                tax_total = (((rec.tax_income - 10000000)*0.15)+650000)
                tax_per = 15
            if rec.tax_income > 20000001 and rec.tax_income <= 30000000:
                tax_total = (((rec.tax_income - 20000000)*0.20)+2150000)
                tax_per = 20
            if rec.tax_income > 30000001:
                tax_total = (((rec.tax_income - 30000000)*0.25)+4150000)
                tax_per = 25
                
            
            total_annual_tax = tax_total
            rec.monthly_tax = total_annual_tax / 12
            
    @api.onchange("employee_id")
    def compute_wage(self):
        if self.employee_id:
            list_months=['jan','feb','march','april','may','june','jul','aug','sep','oct','nov','dec']
            if self.employee_income_tax_ids:
                for line in self.employee_income_tax_ids:
                    line.unlink()
            for i in range(len(list_months)):
                vals = {
                    'months': list_months[i],
                    'employee_income_tax_id': self.id
                    }
                self.employee_income_tax_ids.create(vals)
                
            

            
class EmployeeIncomeTaxLine(models.Model):
    _name = 'employee.income.tax.line'

    employee_income_tax_id = fields.Many2one('employee.income.tax')
    months = fields.Char('Months')
    month_salary = fields.Float(string="Month Salary")
    month_tax = fields.Float(string="Monthly Tax", compute='compute_monthly_tax')
    
    
    def compute_monthly_tax(self):
        for rec in self:
            rec.month_tax = rec.employee_income_tax_id.monthly_tax
            rec.month_salary = rec.employee_income_tax_id.wage
            
