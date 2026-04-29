def filter_pdf_links(links):
    return [l for l in links if ".pdf" in l.lower()]