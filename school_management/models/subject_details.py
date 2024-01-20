from odoo import models, fields


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Information about subject"
    _rec_name = "subject_name"

    subject_name = fields.Char("Subject name")
