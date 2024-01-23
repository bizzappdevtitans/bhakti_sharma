from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Students Details"
    _rec_name = "rollNumber"

    student_name = fields.Char(string="Student name", help="Enter student name")
    father_name = fields.Char(string="Father name", help="Enter father name")
    mother_name = fields.Char(string="Mother name", help="Enter mother name")
    rollNumber = fields.Char(string="Roll number", help="Enter roll number")
    address = fields.Html(string="Address", help="Enter address")
    dateOfBirth = fields.Date("Date Of Birth", help="date of birth")
    age = fields.Integer("Age", help="Enter age", compute="_compute_age")
    email = fields.Text(string="Email", help="enter email")
    phone_number = fields.Text("Phone Number", help="Enter phone number")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], "Gender", help="Select gender"
    )
    student_class = fields.Many2one(
        "class.details",
        string="Class name",
        help="Enter class name in format like - [10th-A]",
    )
    attendance = fields.Many2many("attendance.details")
    attendance_count = fields.Integer(compute="_compute_attendance_count")

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

    def _compute_attendance_count(self):
        for record in self:
            record.attendance_count = len(self.attendance)

    def attendance_button(self):
        return {
            "name": ("Attendance Sheet"),
            "view_mode": "tree,form",
            "res_model": "attendance.details",
            "type": "ir.actions.act_window",
            "domain": [("student", "=", self.rollNumber)],
        }
