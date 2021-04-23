# -*- coding: utf-8 -*-


from ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
import json
import datetime
from django.http import HttpResponse
from reaspostweb.postcore import postcore
from django.core.serializers.json import DjangoJSONEncoder


try:
    postcore = postcore()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Start postcore process ")
    print("\n\n")
except:
    print("Process postcore Error")


def home(request):
    # Create links and OpenID form to the Login handler.
    return HttpResponse('''

        <h2>HELLO</h2>
        
        <form action="reaspostweb/apirequest" name="apirequest" method="post" enctype="multipart/form-data">
            <table>
                <tr>
                    <td>Access Token:</td>
                    <td><input type="text" name="access_token" value="" size="85"/></td>
                 </tr>
                <tr>
                    <td>Data:</td>
                    <td><textarea  id="post_data" name="post_data"  rows="13" cols="85"></textarea></td>
                </tr>
                <tr>
                    <td></td>
                    <td><input type="submit" value="Submit"></td>
                </tr>
            </table>
        </form>
            
            <table>
                <tr>
                    <td>JSON Content:</td>
                    <td><textarea id="json_content" name="json_content" rows="13" cols="85"></textarea></td>
                 </tr>
            </table>

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script type="text/javascript" src="static/jquery.base64.js"></script>
        <!-- <script type="text/javascript" src="http://yckart.github.io/jquery.base64.js/jquery.base64.js"></script> -->

        <script>

        $(document).ready(function(){

            
            $(function() {
                $('#json_content').on('input',function(e){
                    $.base64.utf8encode = true;
                    console.log('json_content Changed!');
                    b64encode = $.base64('encode', $('#json_content').val());
                    $('#post_data').val(b64encode);
                });
            });
            $(function() {
                $('#post_data').on('input',function(e){
                    $.base64.utf8encode = true;
                    console.log('post_data Changed!');
                    b64decode = $.base64('decode', $('#post_data').val()); 
                    $('#json_content').val(decodeURIComponent(escape(b64decode)));
                });
            });

        });
        </script>
    ''')


@csrf_exempt
@ratelimit(key='ip', rate='10/5m', method=['GET', 'POST'])
@sensitive_post_parameters('access_token', 'post_data')
def apirequest(request):

    time_start = datetime.datetime.utcnow()

    access_token = ''
    post_data = ''
    # get request
    if request.method == 'POST':
        if request.POST.get('access_token'):
            access_token = request.POST.get('access_token')
        if request.POST.get('post_data'):
            post_data = request.POST.get('post_data')
    if request.method == 'GET':
        if request.GET.get('access_token'):
            access_token = request.GET.get('access_token')
        if request.GET.get('post_data'):
            post_data = request.GET.get('post_data')

    # core worker
    response = postcore.coreworker(access_token, post_data)

    # response
    time_end = datetime.datetime.utcnow()
    time_usage = time_end-time_start
    response["usage_time"] = str(time_usage)
    response["start_time"] = str(time_start)
    response["end_time"] = str(time_end)

    # return
    return sboResponse(response)


def sboResponse(json_data):
    return HttpResponse(json.dumps(json_data, ensure_ascii=False, indent=1, cls=DjangoJSONEncoder).encode('utf8'), content_type="application/json")
