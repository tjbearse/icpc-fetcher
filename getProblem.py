#!/usr/bin/env python
import lxml.html
import os
import re
import sys
import urllib2

def clean_up_name(string):
    words = map(str.title, string.split())
    return "".join(words)

num_problems = 5184
problem_page_base = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem="
pdf_base = "https://icpcarchive.ecs.baylor.edu/" #external/71/7172.pdf
problem_base_path = os.path.dirname(os.path.realpath(__file__))
def download_problem(num):
    num = int(num)
    assert(num <= num_problems)
    problem_page_url = problem_page_base + str(num)
    problem_page_resp = urllib2.urlopen(problem_page_url).read()
    problem_page = lxml.html.fromstring(problem_page_resp)
    print problem_page

    problem_name = clean_up_name(problem_page.cssselect("h3")[0].text)
    print problem_name
    for el in problem_page.cssselect('table table a'):
        match = re.match(r"external/\d{2}/\d{4}.pdf", el.attrib['href'])
        if match:
            print match.group()
            pdf_url = match.group()

    pdf_url = pdf_base + pdf_url
    pdf_resp = urllib2.urlopen(pdf_url)

    folder = os.path.join(problem_base_path, problem_name)
    os.makedirs(folder)
    
    with open(os.path.join(folder, problem_name + ".pdf"), 'w') as pdf:
        pdf.write(pdf_resp.read())

download_problem(sys.argv[1])
