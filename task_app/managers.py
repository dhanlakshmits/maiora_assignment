from django.db import connection, transaction
import requests,json
from django.conf import settings
from random import randint

class OMSManager():

    @staticmethod
    @transaction.atomic
    def create_task(data):

        try:
            user_id=data.get('user_id')
            task_name=data.get('task_name')
            task_duration=data.get('task_duration')
            task_start_date=data.get('task_start_date')
            task_end_date=data.get('task_end_date')
            with connection.cursor() as cursor:
                cursor.execute("SELECT masterdata.create_task(%s,%s,%s,%s,%s)",
                [user_id,task_name,task_duration,task_start_date,task_end_date])
                res = cursor.fetchone()[0]

        except Exception as e:
            print("error_in_cursor in create_min_order_value method Exception: {}".format(e))
            return "error_in_cursor"

        return res
    

    @staticmethod
    @transaction.atomic
    def update_task(data):
        try:
            user_id=data.get('user_id')
            task_name=data.get('task_name')
            task_duration=data.get('task_duration')
            task_start_date=data.get('task_start_date')
            task_end_date=data.get('task_end_date')
            with connection.cursor() as cursor:
                cursor.execute("SELECT masterdata.update_task(%s,%s,%s,%s,%s)",
                [user_id,task_name,task_duration,task_start_date,task_end_date])
                res = cursor.fetchone()[0]

        except Exception as e:
            print("error_in_cursor in create_min_order_value method Exception: {}".format(e))
            return "error_in_cursor"

        return res
    
    @staticmethod
    @transaction.atomic
    def delete_task(data):
        try:
            user_id=data.get('user_id')
            task_name=data.get('task_name')
            with connection.cursor() as cursor:
                cursor.execute("SELECT masterdata.delete_task(%s,%s)",
                [user_id,task_name])
                res = cursor.fetchone()[0]

        except Exception as e:
            print("error_in_cursor in create_min_order_value method Exception: {}".format(e))
            return "error_in_cursor"

        return res
    
    @staticmethod
    @transaction.atomic
    def get_task(user_id,task_name,format=None):
        try:
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT masterdata.get_task(%s,%s)",[user_id,task_name])
                    cursor.execute('fetch all in taskrefcursor')
                    get_data_res = cursor.fetchall()
                
        except Exception as e:
            return "error_in_cursor"
        if (get_data_res is None or len(get_data_res) == 0):
            return "inventries is empty"

        full_data_list = []

        from .models import Get_tasks
        res = Get_tasks()
        if get_data_res is not None and len(get_data_res) != 0:
            for data in get_data_res:
                task_data = Get_tasks()
                task_data.task_name = data[0]
                task_data.task_duration = data[1]
                task_data.user_id = data[2]
                task_data.task_start_date = data[3]
                task_data.task_end_date = data[4]
                full_data_list.append(task_data.__dict__) 

            return full_data_list
        

    @staticmethod
    @transaction.atomic
    def create_company(data):

        try:
            company_name = data.get('company_name')
            email_id = data.get('email_id')
            company_code = data.get('company_code')
            strength = int(data.get('strength'))
            website = data.get('website')
            if company_name!='' and email_id!='' and company_name is not None and email_id is not None:
                com_char='I'
                def random_with_N_digits(n):
                    range_start = 10**(n-1)
                    range_end = (10**n)-1
                    return randint(range_start, range_end)
                final=[com_char,random_with_N_digits(10)]
                
                company_id=''
                for i in final:
                    company_id=company_id+str(i)

                with connection.cursor() as cursor:
                    cursor.execute("SELECT masterdata.create_company(%s,%s,%s,%s,%s,%s)",[company_name,email_id,company_code,strength,website,company_id])
                    res = cursor.fetchone()[0]
            else:
                return 'company name & email_id should not be empty'

        except Exception as e:
            print("error_in_cursor in create_company method Exception: {}".format(e))
            return "error_in_cursor"

        return res
    

    @staticmethod
    @transaction.atomic
    def update_company(data):
        try:
            company_name = data.get('company_name')
            email_id = data.get('email_id')
            company_code = data.get('company_code')
            website = data.get('website')
            company_id=data.get('company_id')
            if company_id !='' and company_id is not None:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT masterdata.update_company(%s,%s,%s,%s,%s)",[company_name,email_id,company_code,website,company_id])
                    res = cursor.fetchone()[0]
            else:
                return 'failed : company_id should not be empty'

        except Exception as e:
            print("error_in_cursor in create_min_order_value method Exception: {}".format(e))
            return "error_in_cursor"

        return res
    
    @staticmethod
    @transaction.atomic
    def delete_company(data):
        try:
            company_id=data.get('company_id')
            if company_id != '' and company_id is not None:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT masterdata.delete_company(%s)",
                    [company_id])
                    res = cursor.fetchone()[0]
            else:
                return 'failed : company_id should not be empty'

        except Exception as e:
            print("error_in_cursor in create_min_order_value method Exception: {}".format(e))
            return "error_in_cursor"

        return res
    
    @staticmethod
    @transaction.atomic
    def get_company(company_id,limit,offset,format=None):
        try:
            import pdb;pdb.set_trace();
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT masterdata.get_company(%s,%s,%s)",[company_id,limit,offset])
                    cursor.execute('fetch all in companyrefcursor')
                    get_data_res = cursor.fetchall()
                
        except Exception as e:
            return "error_in_cursor"
        if (get_data_res is None or len(get_data_res) == 0):
            return "companies are empty"

        full_data_list = []

        from .models import Get_company
        res = Get_company()
        if get_data_res is not None and len(get_data_res) != 0:
            for data in get_data_res:
                company_data = Get_company()
                company_data.company_id = data[0]
                company_data.company_name = data[1]
                company_data.email_id = data[2]
                company_data.company_code = data[3]
                company_data.strength = data[4]
                company_data.website = data[5]
                full_data_list.append(company_data.__dict__) 

            return full_data_list
        