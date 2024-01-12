from odoo import models, fields


class ParentDetails(models.Model):
    _name = "parent.details"
    _description = "Parent Information"
    _rec_name = "mother_name"

    mother_name = fields.Char(string="Mother name")
    father_name = fields.Char(string="Father name")
    student_field_id = fields.One2many(
        "student.details", "parent_field_id", string="Student Id"
    )
    image = fields.Binary("Image")
    sequence = fields.Integer(
        default=10, help="Gives the sequence order when displaying records in List"
    )
