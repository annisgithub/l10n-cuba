# List of contributors:
# Segu

{
     'name': 'Cuba - HR Contratos',
     'version': '17.0',
     'category': 'Human Resources',
     'summary': """
        Contratos de empleados, Movimientos de Nómina.
     """,
     'description': 'Contratos de trabajadores - Cuba.',
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["hr_contract"],
     'auto_install': True,
     'data': [
          "views/determined_contract_type_views.xml",
          "views/hr_job_views.xml",
          "views/hr_employee_views.xml",
          "views/hr_contract_views.xml",
          "data/determinate_contract_type_data.xml",
          "data/sequence_data.xml",
          "security/ir.model.access.csv",
     ],
     'license': 'LGPL-3',
}
