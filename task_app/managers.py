from django.db import connection, transaction
import requests,json
from django.conf import settings

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