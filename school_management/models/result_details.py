from odoo import models, fields, api


class ResultDetails(models.Model):
    _name = "result.details"
    _description = "Information about results"
    _rec_name = "result_name"

    result_name = fields.Char(string="Result name")
    class_name_id = fields.Many2one(comodel_name="class.details", string="Class name")
    student_name_id = fields.Many2one(comodel_name="student.details", string="Student name")
    total_marks = fields.Integer(string="Total marks", default=1)
    obtained_marks = fields.Integer(string="Obtained marks")
    percentage = fields.Float(string="Percentage", compute="_compute_percentage")
    grade = fields.Char(
        string="Grade",
        compute="_compute_grade",
    )
    sequence_number = fields.Char(string="Number", required=True, readonly=True, default="New")

    @api.model
    def create(self, vals):
        if vals.get("sequence_number", "New") == "New":
            vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
                "result.details"
            )
            vals["result_name"] = vals["result_name"].upper()
            return super(ResultDetails, self).create(vals)

    def write(self, vals):
        if "result_name" in vals and vals["result_name"]:
            vals["result_name"] = vals["result_name"].upper()
        return super(ResultDetails, self).write(vals)

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, "[%s]-[%s]" % (record.sequence_number, record.result_name))
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
                ("class_name_id", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    @api.onchange("class_name_id")
    def _change_student_name_id(self):
        result = {}
        result["domain"] = {
            "student_name_id": [("student_class", "=", self.class_name_id.id)]
        }
        return result

    @api.depends("total_marks", "obtained_marks")
    def _compute_percentage(self):
        for record in self:
            record.percentage = (record.obtained_marks / record.total_marks) * 100

    @api.depends("percentage")
    def _compute_grade(self):
        for record in self:
            if record.percentage >= 75:
                record.grade = "A+"
            elif record.percentage >= 45:
                record.grade = "B+"
            else:
                record.grade = "Fail"
