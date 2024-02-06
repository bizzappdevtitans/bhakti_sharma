from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class TeacherDetails(models.Model):
    _name = "teacher.details"
    _description = "Information about teacher"
    _rec_name = "teacher_name"

    teacher_name = fields.Char(string="Teacher name")
    phone_number = fields.Text(string="Phone number", help="Enter phone number")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    dateOfBirth = fields.Date(string="Date Of Birth", help="date of birth")
    age = fields.Integer(string="Age", help="Enter age", compute="_compute_age")
    email = fields.Text(string="Email", help="enter email")
    address = fields.Html(string="Address", help="Enter address")
    assign_class_ids = fields.One2many(comodel_name="class.details", inverse_name="teacher_id", string="Class Assign")
    subject_data_ids = fields.One2many(
        comodel_name="subject.details", inverse_name="teacher_name_id", string="Subjects Details"
    )
    subject_count = fields.Integer(compute="_compute_subject_count")

    sequence_number = fields.Char(string="Number", required=True, readonly=True, default="New")

    @api.model
    def create(self, vals):
        if vals.get("sequence_number", "New") == "New":
            vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
                "teacher.details"
            )
            return super(TeacherDetails, self).create(vals)

    def capitalize_name(self):
        for record in self.read(["teacher_name"]):
            result = self.write({"teacher_name": record["teacher_name"].capitalize()})
            return result

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (
                    record.id,
                    "[%s]- [%s]" % (record.sequence_number, record.teacher_name),
                )
            )
        return result

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = ["|", ("gender", "ilike", "male"), ("gender", "ilike", "female")]
        return super(TeacherDetails, self).search_read(
            domain, fields, offset, limit, order
        )

    def _compute_subject_count(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("teacher_name", "=", self.id)]
            )

    def subject_button(self):
        for record in self:
            if not record.subject_count > 1:
                return {
                    "name": "Subject",
                    "view_mode": "form",
                    "res_model": "subject.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.subject_data_ids.id,
                }
            return {
                "name": "Total subjects",
                "view_mode": "tree,form",
                "res_model": "subject.details",
                "type": "ir.actions.act_window",
                "domain": [("teacher_name", "=", self.teacher_name)],
            }

    @api.constrains("dateOfBirth")
    def _validate_date(self):
        today = date.today()
        if self.dateOfBirth and self.dateOfBirth.year >= today.year:
            raise ValidationError(
                "Entered date is not valid ..please enter date of birth again"
            )

    @api.depends("dateOfBirth")
    def _compute_age(self):
        for record in self:
            computed_age = 0
            today = date.today()
            if record.dateOfBirth:
                computed_age = today.year - record.dateOfBirth.year
                record.update({"age": computed_age})
            else:
                record.update({"age": computed_age})

    @api.constrains("phone_number")
    def _validate_phoneNumber(self):
        if len(self.phone_number) != 10:
            raise ValidationError("Please add proper 10 digit phone number")
