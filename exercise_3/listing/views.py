from functools import reduce
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Router
from .serializers import RouterSerializer
from .utils import StandardResponse,InputValidation,InputDetails
from django.utils import timezone
import operator
from django.db.models import Q
from ipaddress import ip_address


def index(request):
    """Login function for home page of site."""
    return render(request, 'login.html')

def router(request):
    """View function for home page of site."""
    return render(request, 'index.html')

class RouterMain(RetrieveAPIView):
    """
    View to list all Routers and create new router entry in the system.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RouterSerializer
    def get(self, request, format=None):
        """
        Return a list of routers.
        """
        device_type = request.query_params.get("devicetype")
        ip_range = request.query_params.getlist('ip_range')
        # could not find valid format for sapid hence applying logic is sap_id is 1/1/12:1 then 12 is filter value for device type if ag1 then range 1 to 6 else device type is assumed css
        rangeVal = []
        print(device_type)
        if device_type=="ag1":
            rangeVal = [i for i in range(6)]
        else:
            rangeVal = [i for i in range(7,13)]    
        try:
            print(rangeVal)
            if device_type:
                if len(ip_range)==0:
                    routers = Router.objects.filter(reduce(operator.or_, (Q(sap_id__contains="/"+str(val)+":") for val in rangeVal)),deleted_at=None).order_by("-created_at")
                else:
                    # ip_addresses = self.findIPs(ip_range[0],ip_range[1])
                    routers = Router.objects.filter(reduce(operator.or_, (Q(sap_id__contains="/"+str(val)+":") for val in rangeVal)),loopback__gte=ip_range[0], loopback__lte=ip_range[1], deleted_at=None).order_by("-created_at")    
            else:
                if len(ip_range)==0:
                    routers = Router.objects.filter(deleted_at=None).order_by("-created_at")
                else:
                    # print(ip_range)
                    # ip_addresses = self.findIPs(ip_range[0],ip_range[1])
                    # print(ip_addresses)
                    routers = Router.objects.filter(loopback__gte=ip_range[0], loopback__lte=ip_range[1],deleted_at=None).order_by("-created_at")
            routerSerializer = RouterSerializer(routers, many=True)

        except Exception as e:
            return StandardResponse.Response(False,"Routers not found ",str(e))    
        return StandardResponse.Response(True,"Router list ",routerSerializer.data)
    

    # def findIPs(self, start, end):
    #     start = ip_address(start)
    #     end = ip_address(end)
    #     result = []
    #     while start <= end:
    #         result.append(str(start))
    #         start += 1
    #     return result

    def post(self, request, format=None):
        """
        Save a router.
        """
        # validation Rules
        reqDataDetails = {
            "sap_id":       InputDetails(required=True, inType="string", minLength=7, maxLength=18),
            "hostname":     InputDetails(required=True, inType="string", minLength=3, maxLength=14),
            "loopback":     InputDetails(required=True, inType="string", minLength=9, maxLength=15, inPattern="^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$"),
            "mac_address":  InputDetails(required=True, inType="string", minLength=17, maxLength=17, inPattern="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|([0-9a-fA-F]{4}\\.[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4})$")
        }
        #Check if input data is valid or not
        IsDataValid, message = InputValidation.Response(request.data, reqDataDetails)
        if not IsDataValid:
            return StandardResponse.Response(False, message+" Router could not be created.")

        #Input parameters are valid, save the data
        serializer = RouterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return StandardResponse.Response(True,"Router saved successfully.",serializer.data)    
        emessage=serializer.errors
        return StandardResponse.Response(False,"Router could not be saved.",emessage)


class RouterDetail(RetrieveAPIView):
    """
    View to get a router entry, delete, update router by ID in the system.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RouterSerializer
    def get_object(self,ip):
        """
        Function to get router object by ID.
        """
        try:
            return Router.objects.filter(loopback=ip).first()
        except Router.DoesNotExist:
            return Http404

    def get(self, request, ip, format=None):
        """
        Function to get router by ID.
        """
        try:            
            RouterObj= Router.objects.filter(loopback=ip).first()
            serializer = RouterSerializer(RouterObj)
        except Exception as e :
            return StandardResponse.Response(False,"Router Not found",str(e))
        return StandardResponse.Response(True,"Router Object",serializer.data)

    def delete(self, request, ip, format=None):
        """
        Function to delete router by ID.
        """
        try:
            RouterObj = self.get_object(ip)
            print(RouterObj.deleted_at)
            if RouterObj.deleted_at != None:
                return StandardResponse.Response(False,"Router Not found")    
            RouterObj.deleted_at = timezone.now()
            RouterObj.save()
        except Exception as e :
            return StandardResponse.Response(False,"Router Not found")    
        return StandardResponse.Response(True,"Router Deleted Successfully")
        
    def patch(self, request, ip, format=None):
        """
        Function to partially update router by ID.
        """
        try:
            #Check if input data is valid or not
            # validation Rules
            reqDataDetails = {
                "sap_id":       InputDetails(required=True, inType="string", minLength=7, maxLength=18),
                "hostname":     InputDetails(required=True, inType="string", minLength=3, maxLength=14),
                # "loopback":     InputDetails(required=True, inType="string", minLength=9, maxLength=15, inPattern="^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$"),
                "mac_address":  InputDetails(required=True, inType="string", minLength=17, maxLength=17, inPattern="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|([0-9a-fA-F]{4}\\.[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4})$")
            }
            #Check if input data is valid or not
            IsDataValid, message = InputValidation.Response(request.data, reqDataDetails)
            if not IsDataValid:
                return StandardResponse.Response(False, message+" Router could not be updated.")
            
            # Data is valid, update router
            RouterObj = self.get_object(ip)
            request.data._mutable = True
            del request.data["loopback"]
            request.data._mutable = False
            serializer = RouterSerializer(RouterObj,data=request.data, partial=True)        
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            return StandardResponse.Response(False,"Router update unsuccessful",str(e)) 
        
        return StandardResponse.Response(True,"Router update successful.",serializer.data)        
