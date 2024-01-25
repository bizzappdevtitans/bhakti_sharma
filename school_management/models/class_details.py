from odoo import models, fields


class ClassDetails(models.Model):
    _name = "class.details"
    _description = "Class Information"
    _rec_name = "class_name"

    class_name = fields.Char(
        "Class name", help="Enter class name like -[10th-B]", default="10th-B"
    )
    class_teacher = fields.Many2one("teacher.details", "Class teacher")
    capacity = fields.Integer(
        "Capacity", help="Howmuch student capacity classroom have?"
    )
    room_number = fields.Integer("Room number", help="Enter room number")
    facilities = fields.Many2many(
        "facility.details", help="Facilities list that class have"
    )
    students = fields.One2many("student.details", "student_class", "Students")
    subject = fields.One2many("subject.details", "class_name", "Subjects")
    attendance = fields.One2many("attendance.details", "class_name", "Attendance")

    student_count = fields.Integer(compute="_compute_student_count")
    attendance_count = fields.Integer(compute="_compute_attendance_count")
    subject_count = fields.Integer(compute="_compute_subject_count")

    exam_count = fields.Integer(compute="_compute_exam_count")
    exams = fields.Many2many("exam.details")

    _sql_constraints = [
        ("unique_class", "unique(class_name)", "class name must be unique")
    ]

    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.students)

    def _compute_attendance_count(self):
        for record in self:
            record.attendance_count = len(record.attendance)

    def _compute_subject_count(self):
        for record in self:
            record.subject_count = len(record.subject)

    def _compute_exam_count(self):
        for record in self:
            record.exam_count = len(self.exams)

    def exam_button(self):
        for record in self:
            if record.exam_count > 1:
                return {
                    "name": ("Exam details"),
                    "view_mode": "tree,form",
                    "res_model": "exam.details",
                    "type": "ir.actions.act_window",
                    "domain": [("class_name", "=", self.class_name)],
                }
            else:
                return {
                    "name": ("Exam"),
                    "view_mode": "form",
                    "res_model": "exam.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.exams.id,
                }

    def attendance_button(self):
        for record in self:
            if record.attendance_count > 1:
                return {
                    "name": ("Attendance Sheet"),
                    "view_mode": "tree,form",
                    "res_model": "attendance.details",
                    "type": "ir.actions.act_window",
                    "domain": [("class_name", "=", self.class_name)],
                }
            else:
                return {
                    "name": ("Attendance Sheet"),
                    "view_mode": "form",
                    "res_model": "attendance.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.attendance.id,
                }

    def student_button(self):
        for record in self:
            if record.student_count > 1:
                return {
                    "name": ("Total Students"),
                    "view_mode": "tree,form",
                    "res_model": "student.details",
                    "type": "ir.actions.act_window",
                    "domain": [("student_class", "=", self.class_name)],
                }
            else:
                return {
                    "name": ("Student"),
                    "view_mode": "form",
                    "res_model": "student.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.students.id,
                }

    def subject_button(self):
        for record in self:
            if record.subject_count > 1:
                return {
                    "name": "Total subjects",
                    "view_mode": "tree,form",
                    "res_model": "subject.details",
                    "type": "ir.actions.act_window",
                    "domain": [("class_name", "=", self.class_name)],
                }
            else:
                return {
                    "name": "Subject",
                    "view_mode": "form",
                    "res_model": "subject.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.subject.id,
                }
