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
    subject_data = fields.One2many(
        "subject.details", "teacher_name", "Subjects Details"
    )
    subject_count = fields.Integer(compute="_compute_subject_count")

    sequence_number = fields.Char("Number", required=True, readonly=True, default="New")

    # generate unique number for Teacher record
    @api.model
    def create(self, vals):
        if vals.get("sequence_number", "New") == "New":
            vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
                "teacher.details"
            )
            return super(TeacherDetails, self).create(vals)

    # count the number of subjects
    def _compute_subject_count(self):
        for record in self:
            record.subject_count = len(record.subject_data)

    def subject_button(self):
        for record in self:
            if record.subject_count > 1:
                return {
                    "name": "Total subjects",
                    "view_mode": "tree,form",
                    "res_model": "subject.details",
                    "type": "ir.actions.act_window",
                    "domain": [("teacher_name", "=", self.teacher_name)],
                }
            else:
                return {
                    "name": "Subject",
                    "view_mode": "form",
                    "res_model": "subject.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.subject_data.id,
                }

    # validate the date
    @api.constrains("dateOfBirth")
    def _validate_date(self):
        for record in self:
            today = date.today()
            if record.dateOfBirth and record.dateOfBirth.year >= today.year:
                raise ValidationError(
                    "Entered date is not valid ..please enter date of birth again"
                )

    # compute the age according to date
    @api.depends("dateOfBirth")
    def _compute_age(self):
        for record in self:
            computed_age = 0
            today = date.today()
            if record.dateOfBirth:
                computed_age = today.year - record.dateOfBirth.year
                record.write({"age": computed_age})
            else:
                record.age = computed_age

    # validate the phone number
    @api.constrains("phone_number")
    def _validate_phoneNumber(self):
        for record in self:
            if len(record.phone_number) != 10:
                raise ValidationError("Please add proper 10 digit phone number")
