from django.forms.forms import Form
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown, markdown, markdown_path
from .forms import EditPage, NewPage, search_form
from django import forms
from random import choice

from . import util

def random(request):
    random_page = choice(util.list_entries())
    return HttpResponseRedirect("/wiki/" + random_page)

def index(request):
    search_entry = search_form()
    if request.method == 'GET':
        search_entry = search_form(request.GET)
        if search_entry.is_valid():
            input = search_entry.cleaned_data["search_entry"]
            if input != "": 
                pages = util.list_entries()
                input = str(input)
                for page in pages:
                    if input.upper() == page.upper():
                        return HttpResponseRedirect("/wiki/" + input)    
                possible_pages = []        
                for page in pages:
                    if input.upper() in page.upper():
                        possible_pages.append(page)
                if possible_pages != []:        
                    return render(request, "encyclopedia/search.html", {
                        "entries": possible_pages,
                        "search_entry" : search_entry,
                    }) 
                else:
                    return render(request, "encyclopedia/Noresult.html", {"search_entry" : search_entry})           
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries(),
                    "search_entry": search_entry,
                })    
 
        else:
            return HttpResponse("Bad")    

    search_entry = search_form()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    try:
        
        entry_name = util.get_entry(entry)
        markdowner = Markdown()
        body = markdowner.convert(entry_name)

        search_entry = search_form()
        if request.method == 'GET':
            search_entry = search_form(request.GET)
            if search_entry.is_valid():
                input = search_entry.cleaned_data["search_entry"]
                if input != "": 
                    pages = util.list_entries()
                    input = str(input)
                    for page in pages:
                        if input.upper() == page.upper():
                            return HttpResponseRedirect("/wiki/" + input)    
                    possible_pages = []        
                    for page in pages:
                        if input.upper() in page.upper():
                            possible_pages.append(page)
                    if possible_pages != []:        
                        return render(request, "encyclopedia/search.html", {
                            "entries": possible_pages,
                            "search_entry" : search_entry
                        }) 
                    else:
                        return render(request, "encyclopedia/Noresult.html")           
                else:
                    return render(request, "encyclopedia/entry.html", {
                        "entries": util.list_entries(),
                        "search_entry": search_entry,
                        "entry":entry,
                        "body" : body
                    })    
 

        return render(request, "encyclopedia/entry.html", {
            "entries": util.list_entries(),
            "body": body,
            "entry": entry,
            "search_entry" : search_entry
        })
    except(TypeError):
        search_entry = search_form()
        return render(request, "encyclopedia/error.html", {"search_entry" : search_entry, "error_message" : "The page doesn't exist"}) 

def new(request):
    new_page = NewPage()
    pages = util.list_entries()
    if request.method == 'POST':
        new_page = NewPage(request.POST)
        if new_page.is_valid():
            if new_page.cleaned_data["title"] != '':
                if util.get_entry(new_page.cleaned_data["title"]) != None:
                    return render(request, "encyclopedia/error.html", {
                        "error_message":"This document already exists"
                    })
                else:
                    util.save_entry(new_page.cleaned_data["title"], new_page.cleaned_data["content"])
                    return HttpResponseRedirect("/wiki/" + new_page.cleaned_data["title"])
    search_entry = search_form()
    if request.method == 'GET':
        search_entry = search_form(request.GET)
        if search_entry.is_valid():
            input = search_entry.cleaned_data["search_entry"]
            if input != "": 
                pages = util.list_entries()
                input = str(input)
                for page in pages:
                    if input.upper() == page.upper():
                        return HttpResponseRedirect("/wiki/" + input)    
                possible_pages = []        
                for page in pages:
                    if input.upper() in page.upper():
                        possible_pages.append(page)
                if possible_pages != []:        
                    return render(request, "encyclopedia/search.html", {
                        "entries": possible_pages,
                        "search_entry" : search_entry,
                    }) 
                else:
                    return render(request, "encyclopedia/error.html", {"search_entry" : search_entry, "error_message" : "The page doesn't exist"})           
            else:
                return render(request, "encyclopedia/NewPage.html", {
                "NewPage": new_page,
                "search_entry" : search_entry
                })
   
    return render(request, "encyclopedia/NewPage.html", {
        "NewPage": new_page
    })

def edit(request, entry):
    page = util.get_entry(entry)
    content = {"content" : page}
    page_edit = EditPage(content)
    
    if request.method == "POST":
        page_edit = EditPage(request.POST)
        if page_edit.is_valid():
            util.save_entry(entry, page_edit.cleaned_data["content"])
            return HttpResponseRedirect("/wiki/" + entry)
            
    if request.method == 'GET':
        search_entry = search_form(request.GET)
        if search_entry.is_valid():
            input = search_entry.cleaned_data["search_entry"]
            if input != "": 
                pages = util.list_entries()
                input = str(input)
                for page in pages:
                    if input.upper() == page.upper():
                        return HttpResponseRedirect("/wiki/" + input)    
                possible_pages = []        
                for page in pages:
                    if input.upper() in page.upper():
                        possible_pages.append(page)
                if possible_pages != []:        
                    return render(request, "encyclopedia/search.html", {
                        "entries": possible_pages,
                        "search_entry" : search_entry,
                    }) 
                else:
                    return render(request, "encyclopedia/error.html", {"search_entry" : search_entry, "error_message" : "The page doesn't exist"})           
            else:
                return render(request, "encyclopedia/edit.html", {
                    "body": page_edit,
                    "name" : entry,
                    "search_entry": search_entry
                })
    return render(request, "encyclopedia/edit.html", {
        "body": page_edit,
        "name" : entry,
        "search_entry": search_entry
    })