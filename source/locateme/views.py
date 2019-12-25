from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.core.files.storage import FileSystemStorage
import os, xlrd, requests, json, xlsxwriter


def get_time(original_func):
    import time
    def wrapper_func(*args, **kwargs):
        t1 = time.time()
        result = original_func(*args, **kwargs)
        t2 = time.time() - t1
        print ('{} function ran in {}'.format(original_func.__name__, t2))
        return result
    return wrapper_func

@get_time
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def get_addresses(request):
    myfile = request.FILES.get('addr_file', False)
    api_key = '{api_key_will_come_here}'
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    writing_header = ['Address', 'Longitude', 'Latitude']
    address_data = []
    address_data.append(writing_header)
    msg = ''
    uploaded_file_url = ''
    if myfile:
        base_dir = os.getcwd()
        fs = FileSystemStorage()
        if myfile.name.endswith('.xlsx') or myfile.name.endswith('.xls'):
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            file_path = str(base_dir) + str(uploaded_file_url)
            if os.path.exists(file_path):
                wb = xlrd.open_workbook(file_path)
                sheet = wb.sheet_by_index(0)
                sheet.cell_value(0, 0)
                for i in range(1, sheet.nrows):
                    addr_detail = []
                    address = sheet.cell_value(i, 0)
                    result = requests.get(url + 'address =' + address + '&key =' + api_key)
                    if result.status_code != 200:
                        msg = 'Need API key! Currently showing data over dummy data.'
                    else:
                        pass
                    # dummy result and address, need to be commented in case of havin API Key
                    # and further below code need to be put under else condition
                    result = {'results': [{'address_components': [{'long_name': 'Dehradun', 'short_name': 'Dehradun', 'types': ['locality', 'political']}, {'long_name': 'Dehradun', 'short_name': 'Dehradun', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Uttarakhand', 'short_name': 'UK', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'India', 'short_name': 'IN', 'types': ['country', 'political']}], 'formatted_address': 'Dehradun, Uttarakhand, India', 'geometry': {'bounds': {'northeast': {'lat': 30.4041936, 'lng': 78.1089305}, 'southwest': {'lat': 30.2466633, 'lng': 77.92533879999999}}, 'location': {'lat': 30.3164945, 'lng': 78.03219179999999}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 30.4041936, 'lng': 78.1089305}, 'southwest': {'lat': 30.2466633, 'lng': 77.92533879999999}}}, 'place_id': 'ChIJr4jIVsMpCTkRmYdRMsBiNUw', 'types': ['locality', 'political']}], 'status': 'OK'}
                    address = 'Dehradun, Uttarakhand, India'
                    geo_code_dataset = result.get('results', [])
                    if len(geo_code_dataset):
                        location = geo_code_dataset[0].get('geometry', {}).get('location', {})
                        lat = location.get('lat', None)
                        lng = location.get('lng', None)
                        addr_detail.append(address)
                        addr_detail.append(lng)
                        addr_detail.append(lat)
                        address_data.append(addr_detail)
                os.chdir(file_path[:file_path.rfind('/')+1])
                workbook = xlsxwriter.Workbook(filename)
                worksheet = workbook.add_worksheet("geocoder")
                row = 0
                col = 0
                for addr, lng, lat in (address_data):
                    worksheet.write(row, col, addr)
                    worksheet.write(row, col + 1, lng)
                    worksheet.write(row, col + 2, lat)
                    row += 1
                workbook.close()
        else:
            msg = 'Please upload the file with extension ".xlsx" and ".xls".'
        return Response({'msg': msg, 'file_location': uploaded_file_url}, template_name='get-address-template.html')
    else:
        msg = 'File need to be uploaded.'
        return Response({'msg': msg}, template_name='get-address-template.html')
