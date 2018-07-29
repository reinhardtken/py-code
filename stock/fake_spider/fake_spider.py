#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import pyquery


class Response:
    def __init__(self):
        self.ok = False
        self.content = None
        self.url = None
        self.save = {}


    def doc(self, k):
        pq = pyquery.PyQuery(self.content)
        if not k:
            return pq
        else:
            return pq(k)



class FakeSpider():

    def __init__(self):
        self.__task_list = []
        self.project_name = 'FakeSpider'



    def crawl(self, url, **kwargs):
        if isinstance(url, str):
            self.__task_list.append((url, kwargs))
        elif isinstance(url, list):
            for u in url:
                self.__task_list.append((u, kwargs))
        else:
            return


    def send_message(self, project, msg, url=None):
        self.on_message(project, msg)



    def run(self):
        while(True):
            notEmpty = False
            tempTaskList = self.__task_list.copy()
            self.__task_list.clear()
            for task in tempTaskList:
                notEmpty = True
                s = requests.Session()
                s.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
                s.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))
                try:
                    callback = None
                    save = {}
                    header = None
                    url = task[0]
                    if task[1].get('callback'):
                        callback = task[1]['callback']
                    if task[1].get('headers'):
                        header = task[1]['headers']
                    if task[1].get('save'):
                        save = task[1].get('save')

                    r = s.get(url, headers=header, timeout=10)

                    response = Response()
                    response.url = url

                    if r.status_code == 200:
                        try:
                            response.ok = True
                            response.content = r.content
                            response.save = save
                            callback(response)
                        except Exception as e:
                            print(e)
                    else:
                        print('net Error', response.status_code)

                except requests.ConnectionError as e:
                    print('Error', e.args)

            if notEmpty and len(self.__task_list):
                continue
            else:
                break



    #########################################################################
    def on_start(self):
        self.crawl(self.url(), headers=self.header(), callback=self.processFirstPage)
