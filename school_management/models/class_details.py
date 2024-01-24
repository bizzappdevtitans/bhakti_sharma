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
        return {
            "name": ("Exam details"),
            "view_mode": "tree,form",
            "res_model": "exam.details",
            "type": "ir.actions.act_window",
            "domain": [("class_name", "=", self.class_name)],
        }

    def attendance_button(self):
        return {
            "name": ("Attendance Sheet"),
            "view_mode": "tree,form",
            "res_model": "attendance.details",
            "type": "ir.actions.act_window",
            "domain": [("class_name", "=", self.class_name)],
        }

    def student_button(self):
        return {
            "name": ("Total Students"),
            "view_mode": "tree,form",
            "res_model": "student.details",
            "type": "ir.actions.act_window",
            "domain": [("student_class", "=", self.class_name)],
        }

    def subject_button(self):
        return {
            "name": "Total subjects",
            "view_mode": "tree,form",
            "res_model": "subject.details",
            "type": "ir.actions.act_window",
            "domain": [("class_name", "=", self.class_name)],
        }
