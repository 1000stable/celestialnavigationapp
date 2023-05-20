
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from calculations import meridian_altitude

# Create your views here.
class PlotView(TemplateView):
    template_name = 'plot.html'

    def get(self, request):
        today_passage = meridian_altitude.Meridian_Altitude("test", "lower", "1209", 12, "0009", "1149", 175.46)
        celestial_body = today_passage.celestial_body
        

        context={"celestial_body":celestial_body}

        return render(request, self.template_name, context)

    def post(self, request):
        return redirect(request, self.template_name)

"""  def hello(request):
    #template = loader.get_template('app/hello.html')
    list = ["alpha","beta"]
    temp = TempClass()
    age = 55
    is_authenicated = True
    context={"name":"Django", "first_list":list, "temp_object":temp, 
            "age": age, "is_authenicated": is_authenicated}
    return render(request, "app/hello.html", context)
    #return HttpResponse(template.render(context, request)) """