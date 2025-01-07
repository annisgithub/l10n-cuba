from odoo import models, fields,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    central_office = fields.Char('Central office')
    central_office_abbreviation = fields.Char('Central office abbreviation')
    business_group = fields.Char('Business group')
    abbreviation_group = fields.Char('Group abbreviation')
    ministry = fields.Char('Ministry')
    ministry_abbreviation = fields.Char('Ministry abbreviation')
    legal_address = fields.Char('Legal address')
    director = fields.Char('Director')
    job_id = fields.Char('Position')
    resolution = fields.Char('Resolution')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    employer = fields.Char('Footer page')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.central_office',
                                                  self.central_office)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.central_office_abbreviation',
                                                  self.central_office_abbreviation)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.business_group',
                                                  self.business_group)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.abbreviation_group',
                                                  self.abbreviation_group)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.ministry',
                                                  self.ministry)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.ministry_abbreviation',
                                                  self.ministry_abbreviation)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.legal_address',
                                                  self.legal_address)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.director',
                                                  self.director)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.job_id',
                                                  self.job_id)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.resolution',
                                                  self.resolution)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.phone',
                                                  self.phone)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.email',
                                                  self.email)
        self.env['ir.config_parameter'].set_param('l10n_cu_hr_employee_contract.employer',
                                                  self.employer)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            central_office=self.env['ir.config_parameter'].sudo().get_param('l10n_cu_hr_employee_contract.central_office'),
            central_office_abbreviation=self.env['ir.config_parameter'].sudo().get_param('l10n_cu_hr_employee_contract.central_office_abbreviation'),
            business_group=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.business_group'),
            abbreviation_group=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.abbreviation_group'),
            ministry=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.ministry'),
            ministry_abbreviation=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.ministry_abbreviation'),
            legal_address=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.legal_address'),
            director=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.director'),
            job_id=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.job_id'),
            resolution=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.resolution'),
            phone=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.phone'),
            email=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.email'),
            employer=self.env['ir.config_parameter'].sudo().get_param(
                'l10n_cu_hr_employee_contract.employer'),
        )
        return res
