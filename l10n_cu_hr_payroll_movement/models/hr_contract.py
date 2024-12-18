# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from datetime import timedelta
from odoo.exceptions import ValidationError
class HrContract(models.Model):
    _inherit = 'hr.contract'

    central_office = fields.Char(default=lambda self: self.get_default_central_office(), store=True)
    central_office_abbreviation = fields.Char(store=True)
    business_group = fields.Char(store=True)
    abbreviation_group = fields.Char(store=True)
    ministry = fields.Char(store=True)
    ministry_abbreviation = fields.Char(store=True)
    legal_address = fields.Char(store=True)
    director = fields.Char(store=True)
    position_id = fields.Char(store=True)
    resolution = fields.Char(store=True)
    phone = fields.Char(store=True)
    email = fields.Char(store=True)
    employer = fields.Char(store=True)

    @api.model
    def get_default_central_office(self):
        config = self.env['res.config.settings'].search([], limit=1)
        return config.central_office if config else False


    def create(self, vals):
        contract = super(HrContract, self).create(vals)
        contract._create_payroll_movement()
        return contract

    def _create_payroll_movement(self):
        for contract in self:
            self.env['payroll.movement'].create({
                'employee_id': contract.employee_id.id,
                'contract_id': contract.id,
                'actual_wage': contract.wage,
                'actual_situation_id': contract.job_id.id,
                'actual_occupational_category_id': contract.occupational_category_id.id,
                'actual_department_id':contract.department_id.id,
                'actual_resource_calendar_id': contract.resource_calendar_id.id,
            })
    def print_contract_proforma(self):
        return self.env.ref('l10n_cu_hr_payroll_movement.action_report_contract').report_action(self)





