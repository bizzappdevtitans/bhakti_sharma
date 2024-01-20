from odoo import models, fields


class ClassDetails(models.Model):
    _name = "class.details"
    _description = "Class Information"
    _rec_name = "class_name"

    class_name = fields.Char(
        "Class name", help="Enter class name like -[10th-B]", default="10th-A"
    )
    class_teacher = fields.Many2one("teacher.details", "Class teacher")
    capacity = fields.Integer("Capacity", help="Howmuch capacity in classroom")
    room_number = fields.Integer("Room number", help="Enter room number")
    facilities = fields.Many2many(
        "facility.details", help="Facilities list that class have"
    )
    students = fields.One2many("student.details", "student_class", "Students")
    subject = fields.One2many("subject.details", "subject_name", "Subjects")
