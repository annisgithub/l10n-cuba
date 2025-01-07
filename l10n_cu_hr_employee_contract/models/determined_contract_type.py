# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class DeterminedContractType(models.Model):
    _name = 'determined.contract.type'
    _description = 'Determined Contract Type'

    name = fields.Char(string="Name", groups="hr.group_hr_user", required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)


    @api.ondelete(at_uninstall=False)
    def _unlink_except_referenced_by_contract(self):
        employees = self.env['hr.contract'].search([('determined_contract_type_id', 'in', self.ids)])
        if employees:
            raise ValidationError(
                    _("No puedes eliminar una tipo de contrato determinado que está siendo utilizado por Contratos del empleado."))


    @api.constrains('name')
    def _check_name(self):
        '''
        Valida que el name y code sean únicos
        '''
        if len(self.search([('name', '=ilike', self.name),
                            ('company_id', '=', self.company_id.id),
                            ('id', 'not in', self.ids)])):
            raise ValidationError(u'El nombre del tipo de contrato debe '
                                  u'ser único.')