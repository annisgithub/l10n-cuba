# List of contributors:
# Segu

{
     'name': 'Cuba - HR Movimientos',
     'version': '17.0',
     'category': 'Human Resources',
     'summary': """
        Empleados, Movimientos de Nómina.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["hr","l10n_cu_hr_employee_contract","l10n_cu_address","l10n_cu_hr"],
     'auto_install': True,     
     'data': [
          "views/hr_contract_views.xml",
          "views/payroll_movement_views.xml",
          "views/res_config_settings_views.xml",
          "data/paperformat_global.xml",
          "reports/report_payroll_movement.xml",
          "reports/report_contract_proforma.xml",
          "security/ir.model.access.csv"
     ],
     'license': 'LGPL-3',

}
