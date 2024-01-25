from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Students Details"
    _rec_name = "rollNumber"
    _sql_constraints = [
        ("Students", "unique(rollNumber)", "ROLL NUMBER MUST BE UNIQUE"),
    ]

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
    exam_count = fields.Integer(compute="_compute_exam_count")
    exams = fields.Many2many("exam.details")

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
        for record in self:
            if record.exam_count > 1:
                return {
                    "name": ("Attendance Sheet"),
                    "view_mode": "tree,form",
                    "res_model": "attendance.details",
                    "type": "ir.actions.act_window",
                    "domain": [("student", "=", self.rollNumber)],
                }
            else:
                return {
                    "name": ("Attendance Sheet"),
                    "view_mode": "form",
                    "res_model": "attendance.details",
                    "type": "ir.actions.act_window",
                    "domain": [("student", "=", self.rollNumber)],
                }

    def _compute_exam_count(self):
        for record in self:
            record.exam_count = len(self.exams)

    def exam_button(self):
        for record in self:
            if record.exam_count > 1:
                # print(record.exam_count)
                return {
                    "name": ("Exam details"),
                    "view_mode": "tree,form",
                    "res_model": "exam.details",
                    "type": "ir.actions.act_window",
                    "domain": [("student_names", "=", self.rollNumber)],
                }
            else:
                return {
                    "name": ("Exam"),
                    "view_type": "form",
                    "view_mode": "form",
                    "res_model": "exam.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.exams.id,
                }
