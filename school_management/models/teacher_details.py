from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class TeacherDetails(models.Model):
    _name = "teacher.details"
    _description = "Information about teacher"
    _rec_name = "teacher_name"

    teacher_name = fields.Char("Teacher name")
    phone_number = fields.Text("Phone number", help="Enter phone number")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    dateOfBirth = fields.Date("Date Of Birth", help="date of birth")
    age = fields.Integer("Age", help="Enter age", compute="_compute_age")
    email = fields.Text(string="Email", help="enter email")
    address = fields.Html(string="Address", help="Enter address")
    assign_class = fields.One2many("class.details", "class_teacher", "Class Assign")

    @api.depends("dateOfBirth")
    def _compute_age(self):
        for record in self:
            today = date.today()
            if record.dateOfBirth:
                record.age = today.year - record.dateOfBirth.year
            else:
                record.age = 0

    @api.constrains("dateOfBirth")
    def _validate_date(self):
        for record in self:
            today = date.today()
            if record.dateOfBirth and record.dateOfBirth.year >= today.year:
                raise ValidationError(
                    "Entered date is not valid ..please enter date of birth again"
                )

    @api.constrains("phone_number")
    def _validate_phoneNumber(self):
        for record in self:
            if len(record.phone_number) != 10:
                raise ValidationError("Please add proper 10 digit phone number")
