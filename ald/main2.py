# -*- coding: utf-8 -*-


# pip3 install requests -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
# pip3 install pyquery -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
# pip3 install selenium -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
# pip3 install pymongo -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
# pip3 install scrapy -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
#nohub mongod --config /root/usr/mongodb-linux-x86_64-4.0.0/mongodb.conf


# sys
import datetime
import spiders.toplist2
import spiders.toplist_camera
import spiders.toplist_content
import spiders.toplist_dict
import spiders.toplist_game
import spiders.toplist_life
import spiders.toplist_shopping
import spiders.toplist_social
import spiders.toplist_tools



if __name__ == '__main__':
  spiders.toplist2.run()
  spiders.toplist_camera.run()
  spiders.toplist_content.run()
  spiders.toplist_dict.run()
  spiders.toplist_game.run()
  spiders.toplist_life.run()
  spiders.toplist_shopping.run()
  spiders.toplist_social.run()
  spiders.toplist_tools.run()