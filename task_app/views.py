from django.shortcuts import render
from rest_framework.decorators import api_view
from .managers import OMSManager
from .serializers import *
import requests
from rest_framework.response import Response
from rest_framework import status

OMSManager = OMSManager()

# Create your views here.
@api_view(['OPTIONS', 'POST','GET','PUT','DELETE'])
def task_organiser(request, format=None):
    try:
        if request.method == 'POST':

            result = OMSManager.create_task(request.data)

            if result is not None and result == 'successfully inserted' and 'error' not in result:
                return Response({"message":"Inserted successfully"}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
                    
            else:
                return Response({"error":"Something went wrong : {}".format(result), "error_desc":"Please try again after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})

        elif request.method == 'PUT':

            result = OMSManager.update_task(request.data)

            if result is not None and result == 'successfully updated' and 'error' not in result:
                return Response({"message":"Updated successfully"}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
                    
            else:
                return Response({"error":"Something went wrong : {}".format(result), "error_desc":"Please try again after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})

        elif request.method == 'DELETE':

            result = OMSManager.delete_task(request.data)

            if result is not None and result == 'successfully deleted' and 'error' not in result:
                return Response({"message":"Deleted successfully"}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
                    
            else:
                return Response({"error":"Something went wrong : {}".format(result), "error_desc":"Please try again after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})

        elif request.method == 'GET':
        
            result = OMSManager.get_task(request.query_params.get('user_id'),request.query_params.get('task_name'))

            if result != 0 and result != 'error_in_cursor':
                serializer = GetTaskSerializer(result[0], many=False)
                return Response(serializer.data, headers={"Access-Control-Allow-Origin":"*"})

            elif result is not None and (result == 0 or (len(result) == 0 and result != 'error_in_cursor')) :
                print("You are in create_get_min_order_value - elif block - 404 - : {}".format(result))
                return Response({"error":"invalid_min_order_id","error_desc":"No Minimum orders were found for your id"},status=status.HTTP_404_NOT_FOUND, headers={"Access-Control-Allow-Origin":"*"})

            else:
                print("You are in create_get_min_order_value - else block - 500 - : {} response, for request :{}".format(result, request.data))
                return Response({"error":"Some error occured in processing : {}".format(result),"error_desc":"Please try after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})

        else:
            return Response({"error":"request method is invalid", "error_desc":"Please try again after some time"},status=status.HTTP_400_BAD_REQUEST, headers={"Access-Control-Allow-Origin":"*"})

    except Exception as e:

        return Response({"error":"Something went wrong : {}".format(e), "error_desc":"Please try again after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})


@api_view(['OPTIONS', 'POST','GET','PUT','DELETE'])
def company_details(request, format=None):

    try:
        if request.method == 'POST':

            result = OMSManager.create_company(request.data)

            if result is not None and result == 'successfully inserted' and 'error' not in result:
                return Response({"message":"Inserted successfully"}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
            elif result is not None and result == 'company name & email_id should not be empty':
                return Response({"message":result}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
            else:
                return Response({"error":"Something went wrong : {}".format(result), "error_desc":"Please try again after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})

        elif request.method == 'PUT':

            result = OMSManager.update_company(request.data)
            if result is not None and result == 'successfully updated' and 'error' not in result:
                return Response({"message":"Updated successfully"}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
            elif 'failed' in result: 
                return Response({"message":result}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
            else:
                return Response({"error":"Something went wrong : {}".format(result), "error_desc":"Please try again after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})

        elif request.method == 'DELETE':

            result = OMSManager.delete_company(request.data)

            if result is not None and result == 'successfully deleted' and 'error' not in result:
                return Response({"message":"Deleted successfully"}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
            elif 'failed' in result: 
                return Response({"message":result}, status=status.HTTP_200_OK, headers={"Access-Control-Allow-Origin":"*"})
            else:
                return Response({"error":"Something went wrong : {}".format(result), "error_desc":"Please try again after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})

        elif request.method == 'GET':

            if request.query_params.get('limit') is None or request.query_params.get('offset') is None:
                default_limit = 10
                default_offset = 0
                result = OMSManager.get_company(request.query_params.get('company_id'), default_limit, default_offset)
            elif request.query_params.get('limit') is not None and request.query_params.get('offset') is not None and int(request.query_params.get('limit')) > 20:
                result = OMSManager.get_company(request.query_params.get('company_id'), int(request.query_params.get('limit')), int(request.query_params.get('offset')))

            if result != 0 and result != 'error_in_cursor':
                serializer = GetCompanySerializer(result[0], many=False)
                return Response(serializer.data, headers={"Access-Control-Allow-Origin":"*"})

            elif result is not None and (result == 0 or (len(result) == 0 and result != 'error_in_cursor')) :
                print("You are in create_get_min_order_value - elif block - 404 - : {}".format(result))
                return Response({"error":"invalid_min_order_id","error_desc":"No Minimum orders were found for your id"},status=status.HTTP_404_NOT_FOUND, headers={"Access-Control-Allow-Origin":"*"})

            else:
                print("You are in create_get_min_order_value - else block - 500 - : {} response, for request :{}".format(result, request.data))
                return Response({"error":"Some error occured in processing : {}".format(result),"error_desc":"Please try after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})

        else:
            return Response({"error":"request method is invalid", "error_desc":"Please try again after some time"},status=status.HTTP_400_BAD_REQUEST, headers={"Access-Control-Allow-Origin":"*"})

    except Exception as e:

        return Response({"error":"Something went wrong : {}".format(e), "error_desc":"Please try again after some time"},status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={"Access-Control-Allow-Origin":"*"})
