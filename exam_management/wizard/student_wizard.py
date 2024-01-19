from odoo import api, models, fields


class CreateStudentWizard(models.TransientModel):
    _name = "create.student.wizard"
    _description = "Create Student Wizard"

    student_name=fields.Char(string="Student name",required="True")
    parent_field_id = fields.Many2one("parent.details", string="Parent Id")

    def action_create(self):
        print("Create button clicked!!")
        return
