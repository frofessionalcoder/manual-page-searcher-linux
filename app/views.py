from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os


MAX_RECENT_SEARCHES = 3


# Create your views here.


def manual(cmd):
	res=os.popen(f"man {cmd} | cat").read()
	if res!="":
		return res
	return "Command not found in manual page."



@csrf_exempt
def home(request):
	if request.method=='POST':
		if not "command" in request.POST:
			return render(render,'index.html', context={'results':'Invalid search', 'recents':request.session['recents']})

		cmd = request.POST.get("command")

		# Sanitize
		cmd = ''.join(i for i in cmd if i.isalnum())


		try:
			if not 'recents' in request.session:
				# request.session = {}
				request.session['recents'] = [cmd]
			else:
				recents = request.session['recents']
				if len(recents) == MAX_RECENT_SEARCHES:
					recents.pop(0)

				recents.append(cmd)
				request.session['recents'] = recents
		except:
			request.session.flush()
			request.session['recents'] = []

		return render(request, 'index.html', context={'results':manual(cmd), 'recents':request.session['recents']})


	try:
		if not "recents" in request.session:
			# request.session = {}
			request.session["recents"] = []
	except:
		request.session.flush()
		request.session["recents"] = []

	return render(request,'index.html',context={'recents':request.session['recents']})


def cookieTest(request):
	request.session['info1'] = {'testkey':'testval'}
	request.session['info2'] = ['a','b']

	return HttpResponse("Check cookies")


def todo(request):
	return render(request,'todo.html')
