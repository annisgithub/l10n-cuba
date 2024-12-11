# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class Profession(models.Model):
    _name = 'profession'
    _description = 'Profession'

    name = fields.Char(string="Name", groups="hr.group_hr_user", required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)


    @api.ondelete(at_uninstall=False)
    def _unlink_except_referenced_by_employee(self):
        employees = self.env['hr.employee'].search([('profession_id', 'in', self.ids)])
        if employees:
            raise ValidationError(
                    _("No puedes eliminar una profesión que está siendo utilizado por empleados."))


    @api.constrains('name')
    def _check_name(self):
        '''
        Valida que el name y code sean únicos
        '''
        if len(self.search([('name', '=', self.name),
                            ('company_id', '=', self.company_id.id),
                            ('id', 'not in', self.ids)])):
            raise ValidationError(u'El nombre de la profesión debe'
                                  u'ser único.')