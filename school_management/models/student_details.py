from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError, UserError


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Students Details"
    _rec_name = "rollNumber"

    student_name = fields.Char(string="Student name", help="Enter student name")
    father_name = fields.Char(string="Father name", help="Enter father name")
    mother_name = fields.Char(string="Mother name", help="Enter mother name")
    rollNumber = fields.Char(string="Roll number", help="Enter roll number")
    sequence_number = fields.Char(
        string="Number",
        required="True",
        readonly=True,
        default="New",
    )
    address = fields.Html(string="Address", help="Enter address")
    dateOfBirth = fields.Date("Date Of Birth", help="date of birth")
    age = fields.Integer("Age", help="Enter age", compute="_compute_age")
    email = fields.Text(string="Email", help="enter email")
    phone_number = fields.Text(string="Phone Number", help="Enter phone number")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], "Gender", help="Select gender"
    )
    student_class_id = fields.Many2one(
        comodel_name="class.details",
        string="Class name",
        help="Enter class name in format like - [10th-A]",
    )
    attendance_ids = fields.Many2many(comodel_name="attendance.details")
    attendance_count = fields.Integer(compute="_compute_attendance_count")
    exam_count = fields.Integer(compute="_compute_exam_count")
    exam_ids = fields.Many2many(comodel_name="exam.details")
    result_ids = fields.One2many(comodel_name="result.details", inverse_name="student_name_id", string="Results")
    result_count = fields.Integer(compute="_compute_result_count")

    @api.model
    def create(self, vals):
        vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
            "student.details"
        )
        vals["student_name"] = vals["student_name"].upper()

        allowed_students = (
            self.env["ir.config_parameter"].get_param("allowed_students", "").split(",")
        )

        allowed_students = list(map(lambda x: int(x), allowed_students))

        if int(vals["rollNumber"]) not in allowed_students:
            raise ValidationError(
                "You are only allowed to create the rollnumber 1,2,3,4,5,6,7,8,9,10"
            )
        else:
            return super(StudentDetails, self).create(vals)

    def write(self, vals):
        if "student_name" in vals and vals["student_name"]:
            vals["student_name"] = vals["student_name"].upper()
        return super(StudentDetails, self).write(vals)

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, "[%s] - [%s]" % (record.rollNumber, record.student_name))
            )
        return result

    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += [
                "|",
                (self._rec_name, operator, name),
                ("rollNumber", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = ["|", ("gender", "ilike", "male"), ("gender", "ilike", "female")]
        return super(StudentDetails, self).search_read(
            domain, fields, offset, limit, order
        )

    def unlink(self):
        if self.student_class_id or self.exam_ids:
            raise UserError(
                "You can not delete those records which have class and exams details"
            )
        else:
            deleted = (
                int(
                    self.env["ir.config_parameter"].get_param(
                        "school.deleted_students", "0"
                    )
                )
                + 1
            )
            self.env["ir.config_parameter"].set_param(
                "school.deleted_students", deleted
            )
            return super(StudentDetails, self).unlink()

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
            if not record.dateOfBirth:
                record.write({"age": computed_age})
            computed_age = today.year - record.dateOfBirth.year
            record.write({"age": computed_age})

    def read(self, fields=None, load="_classic_read"):
        self.check_access_rule("read")
        return super(StudentDetails, self).read(fields=fields, load=load)

    @api.constrains("phone_number")
    def _validate_phoneNumber(self):
        for record in self:
            if len(record.phone_number) != 10:
                raise ValidationError("Please add proper 10 digit phone number")

    def _compute_attendance_count(self):
        for record in self:
            record.attendance_count = len(self.attendance_ids)

    def attendance_button(self):
        for record in self:
            if not record.exam_count > 1:
                return {
                    "name": ("Attendance Sheet"),
                    "view_mode": "form",
                    "res_model": "attendance.details",
                    "type": "ir.actions.act_window",
                    "domain": [("student", "=", self.rollNumber)],
                    "res_id": record.attendance_ids.id,
                }
            return {
                "name": ("Attendance Sheet"),
                "view_mode": "tree,form",
                "res_model": "attendance.details",
                "type": "ir.actions.act_window",
                "domain": [("student", "=", self.rollNumber)],
            }

    def _compute_exam_count(self):
        for record in self:
            record.exam_count = len(self.exam_ids)

    def exam_button(self):
        for record in self:
            if not record.exam_count > 1:
                return {
                    "name": ("Exam"),
                    "view_type": "form",
                    "view_mode": "form",
                    "res_model": "exam.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.exam_ids.id,
                }
            return {
                "name": ("Exam details"),
                "view_mode": "tree,form",
                "res_model": "exam.details",
                "type": "ir.actions.act_window",
                "domain": [("student_names", "=", self.rollNumber)],
            }

    def _compute_result_count(self):
        for record in self:
            record.result_count = self.env["result.details"].search_count(
                [("student_name", "=", self.id)]
            )

    def result_button(self):
        for record in self:
            if not record.result_count > 1:
                return {
                    "name": ("Result"),
                    "view_type": "form",
                    "view_mode": "form",
                    "res_model": "result.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.result_ids.id,
                }
            return {
                "name": ("Results"),
                "view_mode": "tree,form",
                "res_model": "result.details",
                "type": "ir.actions.act_window",
                "domain": [("student_name", "=", self.id)],
            }
