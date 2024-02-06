from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ClassDetails(models.Model):
    _name = "class.details"
    _description = "Class Information"
    _rec_name = "class_name"

    class_name = fields.Char(
        string="Class name", help="Enter class name like -[10th-B]", default="9th-B"
    )
    teacher_id = fields.Many2one(comodel_name="teacher.details", string="Class teacher")
    capacity = fields.Integer(
        string="Capacity", help="Howmuch student capacity classroom have?"
    )
    room_number = fields.Integer(string="Room number", help="Enter room number")
    facility_ids = fields.Many2many(
        comodel_name="facility.details", help="Facilities list that class have"
    )
    student_ids = fields.One2many(
        comodel_name="student.details", inverse_name="student_class_id", string="Students"
    )
    subject_ids = fields.One2many(
        comodel_name="subject.details", inverse_name="class_name_id", string="Subjects"
    )
    attendance_ids = fields.One2many(
        comodel_name="attendance.details",
        inverse_name="class_name_id",
        string="Attendance",
    )
    result_ids = fields.One2many(
        comodel_name="result.details", inverse_name="class_name_id", string="Result"
    )
    student_count = fields.Integer(compute="_compute_student_count")
    attendance_count = fields.Integer(compute="_compute_attendance_count")
    subject_count = fields.Integer(compute="_compute_subject_count")
    exam_count = fields.Integer(compute="_compute_exam_count")
    exam_ids = fields.Many2many(comodel_name="exam.details")

    sequence_number = fields.Char(
        string="Number", required=True, readonly=True, default="New"
    )

    _sql_constraints = [
        ("unique_class", "unique(class_name)", "class name must be unique")
    ]

    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)

    def student_button(self):
        for record in self:
            if not record.student_count > 1:
                return {
                    "name": ("Student"),
                    "view_mode": "form",
                    "res_model": "student.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.student_ids.id,
                }
            return {
                "name": ("Total Students"),
                "view_mode": "tree,form",
                "res_model": "student.details",
                "type": "ir.actions.act_window",
                "domain": [("student_class", "=", self.class_name)],
            }

    def _compute_attendance_count(self):
        for record in self:
            record.attendance_count = len(record.attendance_ids)

    def attendance_button(self):
        for record in self:
            if not record.attendance_count > 1:
                return {
                    "name": ("Attendance Sheet"),
                    "view_mode": "form",
                    "res_model": "attendance.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.attendance_ids.id,
                }
            return {
                "name": ("Attendance Sheet"),
                "view_mode": "tree,form",
                "res_model": "attendance.details",
                "type": "ir.actions.act_window",
                "domain": [("class_name", "=", self.class_name)],
            }

    def _compute_subject_count(self):
        for record in self:
            record.subject_count = len(record.subject_ids)

    def subject_button(self):
        for record in self:
            if not record.subject_count > 1:
                return {
                    "name": "Subject",
                    "view_mode": "form",
                    "res_model": "subject.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.subject_ids.id,
                }
            return {
                "name": "Total subjects",
                "view_mode": "tree,form",
                "res_model": "subject.details",
                "type": "ir.actions.act_window",
                "domain": [("class_name", "=", self.class_name)],
            }

    def _compute_exam_count(self):
        for record in self:
            record.exam_count = self.env["exam.details"].search_count(
                [("class_name", "=", self.id)]
            )

    def exam_button(self):
        for record in self:
            if not record.exam_count > 1:
                return {
                    "name": ("Exam"),
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
                "domain": [("class_name", "=", self.class_name)],
            }

    @api.model
    def create(self, vals):
        vals["sequence_number"] = self.env["ir.sequence"].next_by_code("class.details")
        vals["class_name"] = vals["class_name"].upper()
        available_rooms = (
            self.env["ir.config_parameter"].get_param("available_rooms", "").split(",")
        )

        available_rooms = list(map(lambda x: int(x), available_rooms))

        if int(vals["room_number"]) not in available_rooms:
            raise ValidationError("This room not available")
        return super(ClassDetails, self).create(vals)

    def write(self, vals):
        if "class_name" in vals and vals["class_name"]:
            vals["class_name"] = vals["class_name"].upper()
        return super(ClassDetails, self).write(vals)

    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += [
                "|",
                (self._rec_name, operator, name),
                ("teacher_id", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, "[%s]- [%s]" % (record.room_number, record.class_name))
            )
        return result

    @api.onchange("class_name")
    def _validate_capacity(self):
        if "10" in self.class_name:
            self.write({"capacity": 50})

    def unlink(self):
        if not self.subject_ids:
            return super(ClassDetails, self).unlink()
        raise UserError(
            "You can not delete the record which already have subject details."
        )
