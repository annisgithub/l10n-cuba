from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PayrollMovement(models.Model):
    _name = "payroll.movement"
    _description = 'Payroll Movement'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,check_company=True)
    contract_id = fields.Many2one('hr.contract', 'Contract Reference', required=True,
                                         domain="[('employee_id', '=', employee_id)]")
    state = fields.Selection([('draft', _('New')), ('open', 'Open')], 'State', required=True, default='draft',
                             store=True)
    effective_date = fields.Date('Effective Date', required=True)

    # Actual situation
    actual_wage = fields.Float(string='Basic Salary', required=True, store=True)
    actual_situation_id = fields.Many2one('hr.job', string='Job Name', required=True,check_company=True)
    actual_occupational_category_id = fields.Many2one('occupational.category',
                                                   string='Occupational Category',
                                                   store=True, required=True)
    actual_department_id = fields.Many2one('hr.department', 'Work Area',
                                           related='actual_situation_id.department_id',
                                           store=True)
    actual_resource_calendar_id = fields.Many2one('resource.calendar',string="Working Hours",
                                                  default=lambda self: self.env.company.resource_calendar_id.id,
                                                  check_company=True)

    # New situation
    new_wage = fields.Float(string='New Salary', store=True)
    new_situation_id = fields.Many2one('hr.job', 'New Job',check_company=True)
    new_occupational_category_id = fields.Many2one('occupational.category',
                                                   string='New Occupational Category', store=True)
    new_department_id = fields.Many2one('hr.department', 'New Work Area',
                                        related='new_situation_id.department_id',
                                        store=True)

    new_resource_calendar_id = fields.Many2one('resource.calendar',string="New Working Hours",
                                               default=lambda self: self.env.company.resource_calendar_id.id,
                                               check_company=True)
    def name_get(self):
        """
        Retrieves the name of the record in the format "MOV - [contract_reference.name]".
        """
        result = []
        for record in self:
            """
            Retrieves the name of the record.
            """
            name = 'MOV' + '-' + record.contract_id.name
            result.append((record.id, name))
        return result


    @api.ondelete(at_uninstall=False)
    def _check_type_usage(self):
        for record in self:
            if record.state == 'open':
                raise ValidationError(_('The payroll movement has already been approved, it cannot be deleted.'))



