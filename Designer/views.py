from django.shortcuts import render, redirect, get_object_or_404
from Designer.models import userDB, projectDB, divisionDB, imageDB, inputDB, textDB, inheritanceDB, styleDB
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import default_storage
from django.conf import settings
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import StyleSerializer

# Create your views here.


def filemanager(request):
    userdata = userDB.objects.get(email=request.session['email'])
    projectname = request.session.get('projectname')
    if projectname:
        del request.session['projectname']
    projectdata = projectDB.objects.filter(email=request.session['email'])

    return render(request, 'filemanage.html', {'userdata':userdata,'projectdata':projectdata})
def settingspage(request):
    userdata = userDB.objects.get(email=request.session.get('email'))
    projectname = request.session.get('projectname')
    if projectname:
        del request.session['projectname']
    return render(request, 'settings.html', {'userdata':userdata})
def createdesign(request):
    email = request.session.get('email')
    if not email:
        return redirect("authorization")
    ProjectName = request.session.get('projectname')
    if not ProjectName:
        return redirect("/filemanager/")
    divnames = divisionDB.objects.filter(email=email, projectname=ProjectName)
    inputnames = inputDB.objects.filter(email=email, projectname=ProjectName)
    textnames = textDB.objects.filter(email=email, projectname=ProjectName)
    imagenames = imageDB.objects.filter(email=email, projectname=ProjectName)

    try:
        project = projectDB.objects.get(email=email, projectname=ProjectName)
    except projectDB.DoesNotExist:
        messages.error(request, "Project not found.")
        return redirect("/filemanager/")

    return render(request, 'create.html', {'project': project, 'divnames': divnames, 'textnames':textnames, 'inputnames':inputnames, 'imagenames':imagenames,})

def openproject(request, projectname):
    email = request.session.get('email')
    if not email:
        return redirect("authorization")

    if not projectname:
        return redirect("/filemanager/")
    request.session['projectname'] = projectname
    return redirect('/createdesign/')




def profilepage(request):
    userdata = userDB.objects.get(email=request.session.get('email'))
    projectname = request.session.get('projectname')
    if projectname:
        del request.session['projectname']
    return render(request, 'profile.html', {'userdata':userdata})

def authorization(request):
    skip_transition = request.GET.get("skip_transition") == "true"
    request.session.pop('projectname', None)
    request.session.pop('email', None)
    return render(request, 'sign.html', {"skip_transition": skip_transition})


def signup(request):

    if request.method == "POST":
        nameup = request.POST.get("name-up")
        emailup = request.POST.get("email-up")
        passwordup = request.POST.get("password-up")
        repasswordup = request.POST.get("repassword-up")
        designationup = request.POST.get("designation-up")
        if designationup == None:
            designationup = "Add Designation"
        errors = False
        if not nameup:
            messages.error(request, "Name is required.", extra_tags="name")
            errors = True



        if not emailup:
            messages.error(request, "Email is required.", extra_tags="email")
            errors = True
        elif userDB.objects.filter(email = emailup).exists():
            messages.error(request, "Email already exists", extra_tags="email")
            errors = True

        if len(passwordup) < 8:
            messages.error(request, "Password must be at least 8 characters long.", extra_tags="password")
            errors = True

        if " " in passwordup:
            messages.error(request, "Password cannot contain spaces.", extra_tags="password")
            errors = True

        if passwordup != repasswordup:
            messages.error(request, "Passwords do not match.", extra_tags="repassword")
            errors = True


        if errors:
            return redirect("/authorization/?skip_transition=true")

        signupdetails = userDB(username=nameup, email=emailup, password=passwordup, designation=designationup)
        signupdetails.save()
        request.session['email'] = emailup

        return redirect("/filemanager/")

    return redirect('/authorization/?skip_transition=true')

def redirect_to_authorization(request):
    return redirect('authorization')

def loggingin(request):
    if request.method == "POST":
        emailin = request.POST.get('email-in')
        passwordin = request.POST.get('password-in')
        if userDB.objects.filter(email = emailin).exists():
            userdata = userDB.objects.get(email = emailin)
            if passwordin == userdata.password:
                request.session['email'] = emailin
                return redirect("/filemanager/")
            else:
                messages.error(request, "email and password does not match", extra_tags="datamismatch")
                return redirect("authorization")
        else:
            messages.error(request, "The email you entered is not registered", extra_tags="email!exist")
            return redirect("authorization")

    return redirect("/authorization/")

def saveproject(request):

    if request.method == "POST":

        emailc = request.session.get('email')
        if not emailc:
            return redirect("/authorization/")
        projectname = request.POST.get('projectname')
        if projectDB.objects.filter(projectname=projectname, email = emailc).exists():
            messages.error(request, "Project already exist", extra_tags="projectname")
            return redirect("/filemanager/")

        else:
            projectdetails = projectDB(projectname=projectname, email=emailc)
            projectdetails.save()
            request.session['projectname'] = projectname
            return redirect("/createdesign/")

def loggingout(request):
    email = request.session.get('email')
    if email:
        del request.session['email']

    return redirect("/authorization/")

def divdetails(request):
    if request.method == "POST":

        email = request.session.get('email')
        if not email:
            return redirect("authorization")
        ProjectName = request.session.get('projectname')
        if not ProjectName:
            return redirect("/filemanager/")
        divname = request.POST.get('divname')
        if not divname:
            messages.error(request, "Divname cannot be empty", extra_tags="divname")
            return redirect("/createdesign/")
        elif divisionDB.objects.filter(projectname = ProjectName , email=email, divname = divname).exists() or imageDB.objects.filter(projectname = ProjectName , email=email, imagename = divname).exists() or inputDB.objects.filter(projectname = ProjectName , email=email, inputname = divname).exists() or textDB.objects.filter(projectname = ProjectName , email=email, textname = divname).exists():
            messages.error(request, "Name already exists", extra_tags="divname")
            return redirect("/createdesign/")
        positionattrib = request.POST.get('positionattrib')
        bgcolor = request.POST.get('bgcolor')



        if bgcolor:
            style = styleDB(email=email, projectname=ProjectName, LHS= "background-color", RHS=bgcolor, classname = divname, Animation = "None")
            style.save()
        if positionattrib:
            style = styleDB(email=email, projectname=ProjectName, LHS="position", RHS=positionattrib, classname = divname, Animation = "None")
            style.save()
        if positionattrib in ["relative", "absolute", "fixed", "sticky"]:
            leftp = request.POST.get('left')
            topp = request.POST.get('top')
            if leftp:
                unitl = request.POST.get('unitl')
                style = styleDB(email=email, projectname=ProjectName, LHS="left", RHS=leftp+unitl, classname = divname, Animation = "None")
                style.save()
            if topp:
                unitt = request.POST.get('unitt')
                style = styleDB(email=email, projectname=ProjectName, LHS="top", RHS=topp + unitt, classname = divname, Animation = "None")
                style.save()
        height = request.POST.get('heightd')
        width = request.POST.get('widthd')
        if height:
            unithd = request.POST.get('unithd')
            style = styleDB(email=email, projectname=ProjectName, LHS="height", RHS=height + unithd, classname = divname, Animation = "None")
            style.save()
        if width:
            unitwd = request.POST.get('unitwd')
            style = styleDB(email=email, projectname=ProjectName, LHS="width", RHS=width + unitwd, classname = divname, Animation = "None")
            style.save()

        parent = request.POST.get('parents')
        if parent == "None" or not parent:
            parent = "noparent"


        divisiondetails = divisionDB(divname=divname, email=email,  projectname=ProjectName)
        inheritance = inheritanceDB(email=email,  projectname=ProjectName, child = divname, parent = parent)
        inheritance.save()
        divisiondetails.save()

        return redirect("/generatecode/")
# def navdetails(request):
#     if request.method == "POST":
#
#         email = request.session.get('email')
#         if not email:
#             return redirect("authorization")
#         ProjectName = request.session.get('projectname')
#         if not ProjectName:
#             return redirect("/filemanager/")
#         navname = request.POST.get('navname')
#         if not navname:
#             messages.error(request, "Divname cannot be empty", extra_tags="navname")
#             return redirect("/createdesign/")
#         elif divisionDB.objects.filter(projectname=ProjectName, email=email,
#                                        divname=divname).exists() or imageDB.objects.filter(projectname=ProjectName,
#                                                                                            email=email,
#                                                                                            imagename=divname).exists() or inputDB.objects.filter(
#                 projectname=ProjectName, email=email, inputname=divname).exists() or textDB.objects.filter(
#                 projectname=ProjectName, email=email, textname=divname).exists():
#             messages.error(request, "Name already exists", extra_tags="divname")
#             return redirect("/createdesign/")
#         positionattrib = request.POST.get('positionattrib')
#         bgcolor = request.POST.get('bgcolor')
#
#         styling = "." + divname + "{"
#         if bgcolor:
#             styling += "background-color:" + bgcolor + ";"
#         if positionattrib:
#             styling += "position:" + positionattrib + ";"
#         if positionattrib in ["relative", "absolute", "fixed", "sticky"]:
#             leftp = request.POST.get('left')
#             topp = request.POST.get('top')
#             if leftp:
#                 unitl = request.POST.get('unitl')
#                 styling += "left:" + leftp + unitl + ";"
#             if topp:
#                 unitt = request.POST.get('unitt')
#                 styling += "top:" + topp + unitt + ";"
#         height = request.POST.get('heightd')
#         width = request.POST.get('widthd')
#         if height:
#             unithd = request.POST.get('unithd')
#             styling += "height:" + height + unithd + ";"
#         if width:
#             unitwd = request.POST.get('unitwd')
#             styling += "width:" + width + unitwd + ";"
#
#         styling += "}"
#
#         parent = request.POST.get('parents')
#         if parent == "None" or not parent:
#             parent = "noparent"
#         code = '<div class ="' + divname + '">'
#         code += "</div>"
#
#         divisiondetails = divisionDB(divname=divname, email=email, projectname=ProjectName, styling=styling, codes=code)
#         inheritance = inheritanceDB(email=email, projectname=ProjectName, child=divname, parent=parent)
#         inheritance.save()
#         divisiondetails.save()
#
#         return redirect("/generatecode/")


def generatecode(request):
    email = request.session.get("email")
    if not email:
        return redirect("authorization")

    projectname = request.session.get("projectname")
    if not projectname:
        return redirect("/filemanager/")

    divisions = divisionDB.objects.filter(email=email, projectname=projectname)
    images = imageDB.objects.filter(email=email, projectname=projectname)
    inputs = inputDB.objects.filter(email=email, projectname=projectname)
    texts = textDB.objects.filter(email=email, projectname=projectname)
    inheritance = inheritanceDB.objects.filter(email=email, projectname=projectname)


    styles = ""
    for link in inheritance:
        classname = link.child
        styles += f".{classname}{{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname):
            styles += f"{style.LHS}:{style.RHS};"
        styles += "}"
    for link in inheritance:
        classname = link.child
        styles += "." + classname + ":hover{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname, Animation = "hover"):
            styles += style.LHS + ":" + style.RHS + ";"
        styles += "}"
    for link in inheritance:
        classname = link.child
        styles += "." + classname + ":Active{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname, Animation = "active"):
            styles += style.LHS + ":" + style.RHS + ";"
        styles += "}"


    children = {}
    for link in inheritance:
        parent = link.parent
        child = link.child
        children.setdefault(parent, []).append(child)


    elements = {}

    for div in divisions:
        elements[div.divname] = f'<div class="{div.divname}"></div>'

    for img in images:
        img_class = getattr(img, "imagename", "image")
        img_url = img.image.url if img.image else ""
        elements[img_class] = f'<img class="{img_class}" src="{img_url}" />'

    for text in texts:
        elements[text.textname] = f'<p class="{text.textname}">{text.textcontent or ""}</p>'

    for inp in inputs:
        elements[inp.inputname] = f'<input class="{inp.inputname}" type="{inp.inputtype or "text"}" placeholder="{inp.placeholder or ""}" />'


    def build_html(parent):
        html = ""
        for child in children.get(parent, []):
            content = elements.get(child, "")
            nested = build_html(child)
            if nested:
                if "</div>" in content:
                    content = content.replace("</div>", nested + "</div>")
                elif "</p>" in content:
                    content = content.replace("</p>", nested + "</p>")
                elif ">" in content:
                    content = content.replace(">", ">" + nested, 1)
            html += content
        return html

    final_html = build_html("noparent")

    if not final_html:

        all_elements = set(elements.keys())
        child_elements = set(link.child for link in inheritance)
        root_elements = all_elements - child_elements
        for root in root_elements:
            final_html += elements.get(root, "") + build_html(root)


    project, created = projectDB.objects.get_or_create(
        email=email,
        projectname=projectname,
        defaults={"htmlcode": final_html, "cssstyle": styles}
    )

    if not created:
        project.htmlcode = final_html
        project.cssstyle = styles
        project.save()

    print("Generated HTML:\n", final_html)
    print("Generated CSS:\n", styles)

    return redirect("/createdesign/")



def saveandexit(request):

    email = request.session.get("email")
    if not email:
        return redirect("authorization")

    projectname = request.session.get("projectname")
    if not projectname:
        return redirect("/filemanager/")

    divisions = divisionDB.objects.filter(email=email, projectname=projectname)
    images = imageDB.objects.filter(email=email, projectname=projectname)
    inputs = inputDB.objects.filter(email=email, projectname=projectname)
    texts = textDB.objects.filter(email=email, projectname=projectname)
    inheritance = inheritanceDB.objects.filter(email=email, projectname=projectname)


    styles = ""
    for link in inheritance:
        classname = link.child
        styles += f".{classname}{{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname):
            styles += f"{style.LHS}:{style.RHS};"
        styles += "}"
    for link in inheritance:
        classname = link.child
        styles += "." + classname + ":hover{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname, Animation = "hover"):
            styles += style.LHS + ":" + style.RHS + ";"
        styles += "}"
    for link in inheritance:
        classname = link.child
        styles += "." + classname + ":active{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname, Animation = "active"):
            styles += style.LHS + ":" + style.RHS + ";"
        styles += "}"

    children = {}
    for link in inheritance:
        parent = link.parent
        child = link.child
        children.setdefault(parent, []).append(child)


    elements = {}

    for div in divisions:
        elements[div.divname] = f'<div class="{div.divname}"></div>'

    for img in images:
        img_class = getattr(img, "imagename", "image")
        img_url = img.image.url if img.image else ""
        elements[img_class] = f'<img class="{img_class}" src="{img_url}" />'

    for text in texts:
        elements[text.textname] = f'<p class="{text.textname}">{text.textcontent or ""}</p>'

    for inp in inputs:
        elements[
            inp.inputname] = f'<input class="{inp.inputname}" type="{inp.inputtype or "text"}" placeholder="{inp.placeholder or ""}" />'


    def build_html(parent):
        html = ""
        for child in children.get(parent, []):
            content = elements.get(child, "")
            nested = build_html(child)
            if nested:
                if "</div>" in content:
                    content = content.replace("</div>", nested + "</div>")
                elif "</p>" in content:
                    content = content.replace("</p>", nested + "</p>")
                elif ">" in content:
                    content = content.replace(">", ">" + nested, 1)
            html += content
        return html

    final_html = build_html("noparent")

    if not final_html:
        # fallback for rootless elements
        all_elements = set(elements.keys())
        child_elements = set(link.child for link in inheritance)
        root_elements = all_elements - child_elements
        for root in root_elements:
            final_html += elements.get(root, "") + build_html(root)


    project, created = projectDB.objects.get_or_create(
        email=email,
        projectname=projectname,
        defaults={"htmlcode": final_html, "cssstyle": styles}
    )

    if not created:
        project.htmlcode = final_html
        project.cssstyle = styles
        project.save()
    del request.session["projectname"]

    return redirect("/filemanager/")

def deleteproject(request, projectname):
    email = request.session.get("email")
    if not email:
        return redirect("authorization")
    project = get_object_or_404(projectDB, projectname=projectname, email=email)

    divisionDB.objects.filter(email=email, projectname=projectname).delete()
    textDB.objects.filter(email=email, projectname=projectname).delete()
    inputDB.objects.filter(email=email, projectname=projectname).delete()
    imageDB.objects.filter(email=email, projectname=projectname).delete()



    project.delete()
    return redirect('/filemanager/')



def projects(request):
    email = request.session.get("email")
    if not email:
        return redirect("authorization")

    projectname = request.session.get("projectname")
    if not projectname:
        return redirect("/filemanager/")

    project = projectDB.objects.get(email=email, projectname=projectname)


    return render(request,'project.html', {'project':project})

def deleteaccount(request):

    email = request.session['email']
    if not email:
        return redirect('authorization')
    project = projectDB.objects.filter(email=email)
    user = userDB.objects.filter(email=email)
    divisionDB.objects.filter(email=email).delete()
    textDB.objects.filter(email=email).delete()
    inputDB.objects.filter(email=email).delete()
    imageDB.objects.filter(email=email).delete()
    project.delete()
    user.delete()
    return redirect('authorization')

def codepage(request):
    email = request.session.get("email")
    if not email:
        return redirect("authorization")

    projectname = request.session.get("projectname")
    if not projectname:
        return redirect("/filemanager/")
    try:
        code = projectDB.objects.get(email=email, projectname=projectname)
    except projectDB.DoesNotExist:
        messages.error(request, "Project not found.")
        return redirect("/filemanager/")



    return render(request, 'code.html', {'code':code})


def imagedetails(request):
    if request.method == "POST":
        email = request.session.get('email')
        if not email:
            return redirect("authorization")

        ProjectName = request.session.get('projectname')
        if not ProjectName:
            return redirect("/filemanager/")

        img = request.FILES.get('image')
        if not img:
            messages.error(request, "Import an Image", extra_tags="img")
            return redirect("/createdesign/")

        imgname = request.POST.get('imgname')
        if not imgname:
            messages.error(request, "Image name cannot be empty", extra_tags="imgname")
            return redirect("/createdesign/")
        elif divisionDB.objects.filter(projectname=ProjectName, email=email, divname=imgname).exists() or \
                imageDB.objects.filter(projectname=ProjectName, email=email, imagename=imgname).exists() or \
                inputDB.objects.filter(projectname=ProjectName, email=email, inputname=imgname).exists() or \
                textDB.objects.filter(projectname=ProjectName, email=email, textname=imgname).exists():
            messages.error(request, "Name already exists", extra_tags="imgname")
            return redirect("/createdesign/")

        imgwidth = request.POST.get('widthimg')
        unitwimg = request.POST.get('unitwimg')
        heightimg = request.POST.get('heightimg')
        unithimg = request.POST.get('unithimg')

        parent = request.POST.get('parents')
        if parent == "None" or not parent:
            parent = "noparent"


        img_path = default_storage.save(f'images/{img.name}', img)
        img_url = os.path.join(settings.MEDIA_URL, img_path)


        if imgwidth:
            style = styleDB(email=email, projectname=ProjectName, LHS="width", RHS=imgwidth + unitwimg, classname=imgname, Animation = "None")
            style.save()
        if heightimg:
            style = styleDB(email=email, projectname=ProjectName, LHS="height", RHS=heightimg + unithimg, classname=imgname, Animation = "None")
            style.save()


        imgdetails = imageDB(email=email, projectname=ProjectName, image=img, imagename=imgname)
        inheritance = inheritanceDB(email=email, projectname=ProjectName, child=imgname, parent=parent)
        inheritance.save()
        imgdetails.save()

        return redirect("/generatecode/")


def textdetails(request):
    if request.method == "POST":
        email = request.session.get('email')
        if not email:
            return redirect("authorization")
        ProjectName = request.session.get('projectname')
        if not ProjectName:
            return redirect("/filemanager/")
        textname = request.POST.get('textname')
        if not textname:
            messages.error(request, "Text name cannot be empty", extra_tags="textname")
            return redirect("/createdesign/")
        elif divisionDB.objects.filter(projectname = ProjectName , email=email, divname = textname).exists() or imageDB.objects.filter(projectname = ProjectName , email=email, imagename = textname).exists() or inputDB.objects.filter(projectname = ProjectName , email=email, inputname = textname).exists() or textDB.objects.filter(projectname = ProjectName , email=email, textname = textname).exists():
            messages.error(request, "Name already exists", extra_tags="textname")
            return redirect("/createdesign/")

        textcontent = request.POST.get('content')
        fontsize = request.POST.get('fontsize')
        fontunit = request.POST.get('unitfont')
        fontfamily = request.POST.get('fonttype')
        textcolor = request.POST.get('textcolor')
        if not textcontent:
            textcontent = ""
        parent = request.POST.get('parentstext')


        code = '<p class = "' + textname + '">' + textcontent + "</p>"

        if fontsize:
            style = styleDB(email=email, projectname=ProjectName, LHS="font-size", RHS=fontsize + fontunit,
                            classname=textname, Animation = "None")
            style.save()
        if fontfamily:
            style = styleDB(email=email, projectname=ProjectName, LHS="font-family", RHS=fontfamily,
                            classname=textname, Animation = "None")
            style.save()
        if textcolor:
            style = styleDB(email=email, projectname=ProjectName, LHS="color", RHS=textcolor,
                            classname=textname, Animation = "None")
            style.save()

        if parent == "None" or not parent:
            parent = "noparent"

        textdetails = textDB( email = email, projectname = ProjectName, textname = textname, textcontent = textcontent)
        textdetails.save()
        inheritance = inheritanceDB(email=email, projectname=ProjectName, child=textname, parent=parent)
        inheritance.save()
        return redirect("/generatecode/")

def inputdetails(request):
    if request.method == "POST":
        email = request.session.get('email')
        if not email:
            return redirect("authorization")
        ProjectName = request.session.get('projectname')
        if not ProjectName:
            return redirect("/filemanager/")
        placeholder = request.POST.get('placeholder')
        if not placeholder:
            placeholder = ""
        inputname = request.POST.get('inputname')
        if not inputname:
            messages.error(request, "Name cannot be empty", extra_tags="inputname")
            return redirect("/createdesign/")
        elif divisionDB.objects.filter(projectname = ProjectName , email=email, divname = inputname).exists() or imageDB.objects.filter(projectname = ProjectName , email=email, imagename = inputname).exists() or inputDB.objects.filter(projectname = ProjectName , email=email, inputname = inputname).exists() or textDB.objects.filter(projectname = ProjectName , email=email, textname = inputname).exists():
            messages.error(request, "Name already exists", extra_tags="inputname")
            return redirect("/createdesign/")
        inputwidth = request.POST.get('inputwidth')
        unitwinput = request.POST.get('unitwinput')
        heightinput = request.POST.get('heightinput')
        unithinput = request.POST.get('unithinput')
        inputtype = request.POST.get('inputtype')

        if inputwidth:
            style = styleDB(email=email, projectname=ProjectName, LHS="width", RHS=inputwidth + unitwinput,
                    classname=inputname, Animation = "None")
            style.save()
        if heightinput:
            style = styleDB(email=email, projectname=ProjectName, LHS="height", RHS=heightinput + unithinput,
                            classname=inputname, Animation = "None")
            style.save()

        parent = request.POST.get('parent')
        if parent == "None" or not parent:
            parent = "noparent"

        inputdetails = inputDB(email = email, projectname = ProjectName, inputname = inputname, placeholder = placeholder, inputtype = inputtype)
        inputdetails.save()
        inheritance = inheritanceDB(email=email, projectname=ProjectName, child=inputname, parent=parent)
        inheritance.save()

        return redirect("/generatecode/")

@api_view(['GET'])
def get_styles_api(request):
    divname = request.GET.get('divname')
    email = request.session.get('email')
    projectname = request.session.get('projectname')

    if not divname:
        return Response({"error": "Missing divname"}, status=400)
    if not email:
        return Response({"error": "Missing email"}, status=400)
    if not projectname:
        return Response({"error": "Missing projectname"}, status=400)

    styles = styleDB.objects.filter(classname=divname, email=email, projectname=projectname, Animation="None")



    data = [{"lhs": s.LHS, "rhs": s.RHS} for s in styles]
    return Response(data)

class StyleViewSet(viewsets.ModelViewSet):
    queryset = styleDB.objects.all()
    serializer_class = StyleSerializer

@api_view(['POST'])
def add_style_api(request):
    divname = request.data.get('divname')
    lhs = request.data.get('lhs')
    rhs = request.data.get('rhs')
    animation = request.data.get('animation', "None")
    email = request.session.get('email')
    projectname = request.session.get('projectname')

    if not all([divname, lhs, rhs, email, projectname]):
        return Response({"error": "Missing data"}, status=400)

    styleDB.objects.create(
        classname=divname,
        LHS=lhs,
        RHS=rhs,
        email=email,
        projectname=projectname,
        Animation=animation
    )

    return Response({"success": True})



@api_view(['GET', 'POST'])
def regenerate_code_api(request):
    email = request.session.get("email")
    projectname = request.session.get("projectname")

    if not email or not projectname:
        return Response({"error": "Missing session data"}, status=400)

    divisions = divisionDB.objects.filter(email=email, projectname=projectname)
    images = imageDB.objects.filter(email=email, projectname=projectname)
    inputs = inputDB.objects.filter(email=email, projectname=projectname)
    texts = textDB.objects.filter(email=email, projectname=projectname)
    inheritance = inheritanceDB.objects.filter(email=email, projectname=projectname)

    styles = ""
    for link in inheritance:
        classname = link.child
        styles += "." + classname + "{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname, Animation = "None"):
            styles += style.LHS + ":" + style.RHS + ";"
        styles += "}"
    for link in inheritance:
        classname = link.child
        styles += "." + classname + ":hover{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname, Animation = "hover"):
            styles += style.LHS + ":" + style.RHS + ";"
        styles += "}"
    for link in inheritance:
        classname = link.child
        styles += "." + classname + ":active{"
        for style in styleDB.objects.filter(email=email, projectname=projectname, classname=classname, Animation = "active"):
            styles += style.LHS + ":" + style.RHS + ";"
        styles += "}"

    children = {}
    for link in inheritance:
        parent = link.parent
        child = link.child
        if parent not in children:
            children[parent] = []
        children[parent].append(child)

    elements = {}

    for div in divisions:
        elements[div.divname] = '<div class="' + div.divname + '"></div>'

    for img in images:
        img_class = getattr(img, "imagename", "image")
        img_url = img.image.url if img.image else ""
        elements[img_class] = '<img class="' + img_class + '" src="' + img_url + '" />'

    for text in texts:
        elements[text.textname] = '<p class="' + text.textname + '">' + (text.textcontent or "") + '</p>'

    for inp in inputs:
        inputname = inp.inputname
        inputtype = inp.inputtype or "text"
        placeholder = inp.placeholder or ""
        elements[inputname] = '<input class="' + inputname + '" type="' + inputtype + '" placeholder="' + placeholder + '" />'

    def build_html(parent):
        html = ""
        for child in children.get(parent, []):
            content = elements.get(child, "")
            nested = build_html(child)
            if nested:
                if "</div>" in content:
                    content = content.replace("</div>", nested + "</div>")
                elif "</p>" in content:
                    content = content.replace("</p>", nested + "</p>")
                elif ">" in content:
                    content = content.replace(">", ">" + nested, 1)
            html += content
        return html

    final_html = build_html("noparent")

    if not final_html:
        all_elements = set(elements.keys())
        child_elements = set(link.child for link in inheritance)
        root_elements = all_elements - child_elements
        for root in root_elements:
            final_html += elements.get(root, "") + build_html(root)

    project, created = projectDB.objects.get_or_create(
        email=email,
        projectname=projectname,
        defaults={"htmlcode": final_html, "cssstyle": styles}
    )

    if not created:
        project.htmlcode = final_html
        project.cssstyle = styles
        project.save()

    return Response({
        "html": final_html,
        "css": styles
    })

@api_view(['POST'])
def delete_style_api(request):
    divname = request.data.get('divname')
    lhs = request.data.get('lhs')
    rhs = request.data.get('rhs')
    email = request.session.get('email')
    projectname = request.session.get('projectname')

    if not all([divname, lhs, rhs, email, projectname]):
        return Response({"error": "Missing required parameters"}, status=400)

    deleted, _ = styleDB.objects.filter(
        classname=divname,
        LHS=lhs,
        RHS=rhs,
        email=email,
        projectname=projectname
    ).delete()

    if deleted == 0:
        return Response({"error": "Style not found"}, status=404)

    return Response({"success": True})


@api_view(['GET'])
def get_hover_styles_api(request):
    divname = request.GET.get('divname')
    email = request.session.get('email')
    projectname = request.session.get('projectname')

    if not divname:
        return Response({"error": "Missing divname"}, status=400)
    if not email:
        return Response({"error": "Missing email"}, status=400)
    if not projectname:
        return Response({"error": "Missing projectname"}, status=400)

    styles = styleDB.objects.filter(
        classname=divname,
        email=email,
        projectname=projectname,
        Animation = "hover"
    )

    data = [
        {
            "lhs": s.LHS,
            "rhs": s.RHS,
            "animation": s.Animation
        }
        for s in styles
    ]

    return Response(data)

@api_view(['GET'])
def get_active_styles_api(request):
    divname = request.GET.get('divname')
    email = request.session.get('email')
    projectname = request.session.get('projectname')

    if not divname:
        return Response({"error": "Missing divname"}, status=400)
    if not email:
        return Response({"error": "Missing email"}, status=400)
    if not projectname:
        return Response({"error": "Missing projectname"}, status=400)

    styles = styleDB.objects.filter(
        classname=divname,
        email=email,
        projectname=projectname,
        Animation = "active"
    )

    data = [
        {
            "lhs": s.LHS,
            "rhs": s.RHS,
            "animation": s.Animation
        }
        for s in styles
    ]

    return Response(data)
