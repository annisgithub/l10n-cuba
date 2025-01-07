# List of contributors:
# Segu

{
     'name': 'Cuba - RRHH',
     'version': '17.0',
     'category': 'Human Resources',
     'summary': """
        Empleados, tarjetas de asistencias.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["hr","l10n_cu_address"],
     'auto_install': True,     
     'data': [
          "data/hr_data.xml",
          "data/resource_data.xml",
          "data/schooling_level_data.xml",
          "data/occupational_category_data.xml",
          "views/res_users_views.xml",
          "views/assistance_cards_template.xml",
          "views/schooling_level_views.xml",
          "views/profession_views.xml",
          "views/occupational_category_views.xml",
          "views/hr_employee_views.xml",
          "reports/report_assistance_cards.xml",
          "wizards/assistance_cards_wizard.xml",
          "security/ir.model.access.csv"
     ],
     'license': 'LGPL-3',
}
