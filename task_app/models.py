from django.db import models

# Create your models here.

class Get_tasks:
    def __init__(self):

        self.task_name = None
        self.task_duration = None
        self.user_id = None
        self.task_start_date = None
        self.task_end_date = None


class Get_company:
    def __init__(self):

        self.company_id = None
        self.company_name = None
        self.email_id = None
        self.company_code = None
        self.strength = None
        self.website = None

