import wikipedia

subject = "jwkleds"

wikipage= wikipedia.page(subject)
wikiurl = wikipage.url

print wikiurl