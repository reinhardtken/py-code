#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests

class FakeSpider():

    def __init__(self):
        self.__task_list = []




    def crawl(self, url, **kwargs):
        if isinstance(url, str):
            self.__task_list.append((url, kwargs))
        elif isinstance(url, list):
            for u in url:
                self.__task_list.append((u, kwargs))
        else:
            return



    def Run(self):
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
                    header = None
                    url = task[0]
                    if task[1].get('callback'):
                        callback = task[1]['callback']
                    if task[1].get('headers'):
                        header = task[1]['headers']


                    response = s.get(url, headers=header, timeout=10)
                    #response = s.get(task[0], timeout=10)
                    if response.status_code == 200:
                        try:
                            callback(response.content)
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
