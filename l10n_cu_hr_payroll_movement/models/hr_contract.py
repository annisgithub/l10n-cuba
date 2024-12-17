# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from datetime import timedelta
from odoo.exceptions import ValidationError
class HrContract(models.Model):
    _inherit = 'hr.contract'


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






