from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Student Information"
    _rec_name = "student_name"

    # string fields
    student_name = fields.Char(string="Student name")
    school_name = fields.Selection(
        [
            ("durga", "DURGA HIGH SCHOOL"),
            ("j.l", "J.L.HIGH SCHOOL"),
            ("other", "Other"),
        ],
        "School name",
    )
    feedback = fields.Text(string="Feedback")
    address = fields.Html(string="Address")

    # date and time
    date = fields.Date("Date")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    age = fields.Integer("Age", compute="_compute_age")
    datetime = fields.Datetime(
        "Date and Time", default=lambda self: fields.Datetime.now()
    )

    # numeric fileds
    marks = fields.Integer(string="Marks", default=0)
    percentage = fields.Float("Percentage", (3, 2))

    image = fields.Binary("Image")
    active = fields.Boolean(string="Student active", default=True)

    parent_field_id = fields.Many2one("parent.details", string="Parent Id")

    priority = fields.Selection(
        [("0", "Normal"), ("1", "Low"), ("2", "High"), ("3", "Very Hiigh")],
        string="Priority",
    )
    color = fields.Integer("Color")
    website_url = fields.Char(string="website Url", help="add website url")
    state = fields.Selection(
        [("in_progress", "In Progress"), ("done", "Done")],
        string="State",
        default="in_progress",
        required=True,
    )
    progress = fields.Integer("Progress", compute="_compute_progress")
    email = fields.Char(string="Email")
    subjects = fields.Many2many("student.subject.details", string="Subject")

    @api.depends("date")
    def _compute_age(self):
        for record in self:
            today = date.today()
            if record.date:
                record.age = today.year - record.date.year
            else:
                record.age = 0

    @api.constrains("student_name")
    def validate_name(self):
        for record in self:
            if len(record.student_name) < 4:
                raise ValidationError("STUDENT NAME MUST BE MORE THAN 4 CHARACTER")

    @api.depends("state")
    def _compute_progress(self):
        for record in self:
            if record.state == "done":
                record.progress = 100
            elif record.state == "in_progress":
                record.progress = 50
            else:
                record.progress = 0


class StudentSubjectDetails(models.Model):
    _name = "student.subject.details"
    _description = "Information about subject which student give exam"
    _rec_name = "subject_name"

    students = fields.Many2many("student.details", string="Student")
    subject_name = fields.Selection(
        [("maths", "Maths"), ("english", "English")], "Select Subject"
    )
