#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from fake_spider import cwsj



if __name__ == '__main__':
    gpfh = cwsj.Handler()
    gpfh.on_start()
    gpfh.run()