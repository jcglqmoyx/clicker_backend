import datetime

from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authenticate.models import Machine, Credential


@api_view(['POST'])
@require_http_methods(['POST'])
def index(request):
    activation_code = request.POST.get('activation_code')
    os = request.POST.get('os')
    machine_code = request.POST.get('machine_code')

    if activation_code == '123456':
        machines = Machine.objects.filter(machine_code=machine_code)
        if not machines:
            machine = Machine(machine_code=machine_code, os=os, first_login_time=datetime.datetime.now())
            machine.save()
            return Response({
                'result': 'trial started',
            })
        elif machines[0].activated:
            return Response({
                'result': 'success',
            })
        else:
            trial_expired_time = machines[0].first_login_time + datetime.timedelta(days=7)
            if datetime.datetime.now() >= trial_expired_time:
                return Response({
                    'result': 'failed',
                    'error_message': 'trial expired',
                })
            else:
                return Response({
                    'result': 'trial not expired',
                })
    else:
        credentials = Credential.objects.filter(code=activation_code)
        if not credentials:
            return Response({
                'result': 'failed',
                'error_message': 'invalid activation code',
            })
        credential = credentials[0]
        machines_with_this_credential = Machine.objects.filter(credential=credential)
        machines_with_this_machine_code = Machine.objects.filter(machine_code=machine_code)
        if not machines_with_this_machine_code:
            if len(machines_with_this_credential) >= 3:
                return Response({
                    'result': 'failed',
                    'error_message': 'activation code can not be used on more than 3 devices',
                })
            machine = Machine(machine_code=machine_code, os=os, credential=credential, activated=True,
                              first_login_time=datetime.datetime.now(), activation_time=datetime.datetime.now())
            machine.save()
            return Response({
                'result': 'success',
            })
        else:
            machine = machines_with_this_machine_code[0]
            machine.credential = credential
            machine.activated = True
            machine.activation_time = datetime.datetime.now()
            machine.save()
            return Response({
                'result': 'success',
            })
