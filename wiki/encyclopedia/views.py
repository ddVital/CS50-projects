import markdown2, random, re
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", { "entries": util.list_entries() })


def search(request):
    entries = util.list_entries()
    find_entries = list()

    search_box = request.POST.get("q").capitalize()
    
    if search_box in entries:
       return HttpResponseRedirect(f"wiki/{search_box}")

    for entry in entries:
        if search_box in entry:
            find_entries.append(entry)
        else:
            print(f'{find_entries}')

    if find_entries:
        return render(request, "encyclopedia/search.html", {
           "search_result": find_entries,
           "search": search_box
        })

    else:
        return render(request, "encyclopedia/search.html", {"no_result": f"No results for {search_box}"})


def random_page(request):
    entries = util.list_entries() # list of wikis
    selected_page = random.choice(entries)
    return redirect('encyclopedia:wiki_page', page_title=selected_page)


def wiki_page(request, page_title):
    entries = util.list_entries()
    if page_title.capitalize() in entries:
        markdown_text = util.get_entry(page_title.capitalize())
        markdowner = markdown2.Markdown()
        html_content = markdowner.convert(markdown_text)
        return render(request, "encyclopedia/wiki.html", {
            "title": page_title,
            "page_title": page_title.capitalize(),
            "entry_content": html_content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": "Error",
            "error": "page was not found"
        })


def add_entry(request):
    if request.method == "POST":
        title = request.POST.get("title").capitalize()
        content = request.POST.get("content")
        if title not in util.list_entries():
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")
        else:
            return render(request, "encyclopedia/error.html", { "error": 'Entry already exists' })

    return render(request, "encyclopedia/add.html")


def edit_page(request, page_title):
    original_content = util.get_entry(page_title)
    try:
        if request.method == "POST":
            new_content = request.POST.get("edit-content")
            util.save_entry(page_title.capitalize(), new_content)

            return HttpResponseRedirect(f"http://127.0.0.1:8000/wiki/{page_title.capitalize()}")
    except:
        return render(request, "encyclopedia/error.html", {
            "error": "s"
        })

    return render(request, "encyclopedia/edit.html", {
        "page_title": page_title,
        "content": original_content
    })