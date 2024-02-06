from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    title_page_text = fields.Char(
        string="Title Page Text",
        config_parameter="school.title_page_text",
        default="Page Title Information",
    )
    allowed_students = fields.Char(
        string="Allowed Students", config_parameter="allowed_students"
    )

    deleted_students = fields.Char(
        string="Deleted students", config_parameter="school.deleted_students", default=0
    )

    available_rooms = fields.Char(
        string="Available Room", config_parameter="class.available_rooms",default=0
    )
