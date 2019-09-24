FROM registry.cn-beijing.aliyuncs.com/lefeng/python_3.7-anaconda_5.3:1.0
LABEL maintainer="liuqingping"
RUN mkdir -p /letv/logs/
RUN chmod 777 /letv/logs/
RUN /root/anaconda3/bin/pip install grpcio -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
RUN /root/anaconda3/bin/pip install protobuf -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
RUN /root/anaconda3/bin/pip install tushare -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
ADD pyStockCrawl /letv/app/