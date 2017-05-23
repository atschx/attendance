# -*- coding: utf-8 -*-
import scrapy
from urlparse import urlparse
from urlparse import parse_qs


class OnlinesjtuSpider(scrapy.Spider):
    name = "onlinesjtu"
    allowed_domains = ["onlinesjtu.com"]

    # 287 程序设计（C） 2017 春 吴玉萍 已上传23讲
    # 345 计算机网络 2017 春 谷红亮 已上传18讲
    # 2220 大学英语（一）  2017 春 萧瑜 已上传12讲
    # 2299 计算机应用基础（二） 王德俊 已上传10讲

    # base_url = 'http://onlinesjtu.com/learningspace/learning/student/downloadlist.asp?'
    # base_params = 'term_identify=2017_1&userid=717101010167&username=&'
    # 登录完成之后直接进入redirectTo main.asp?.4591333=.6945416
    # 'http://onlinesjtu.com/learningspace/learning/enterbridge.asp?UserID=717101010167&Password=34e7720320bc35e8&UserType=0&IsOpen=1'
    base_url = 'http://onlinesjtu.com/learningspace/learning/student/downloadlist.asp'
    start_urls = [
        '%s?term_identify=2017_1&userid=717101010167&username=&courseid=287&ishd=1' % base_url,
        '%s?term_identify=2017_1&userid=717101010167&username=&courseid=345&ishd=1' % base_url,
        '%s?term_identify=2017_1&userid=717101010167&username=&courseid=2220&ishd=1' % base_url,
        '%s?term_identify=2017_1&userid=717101010167&username=&courseid=2299&ishd=1' % base_url,
    ]

    def parse(self, response):
        print response
        for test in scrapy.Selector(response).xpath("//html/body/table/tbody/tr/td[1]/div"):
            # response.url
            base_url = "http://onlinesjtu.com/learningspace/learning/student/"
            base_query_str = test.xpath("./a[2]/@href").extract_first()

            download_url = base_url + base_query_str
            urlparse1 = urlparse(download_url)
            query_str = urlparse1.query
            data = parse_qs(query_str, keep_blank_values=True)
            term_identify_ = data.get("term_identify")[0]
            courseid_ = data.get("courseid")[0]
            resourceid_ = data.get("resourceid")[0]

            download_command = "wget -c %s -o %s_%s-%s.mp4 && " % (download_url, term_identify_, courseid_, resourceid_)
            # self.log(download_command)

            filename = 'onlinesjtu-%s_%s_%s.sh' % (term_identify_, "717101010167", courseid_)
            with open(filename, 'a') as f:
                f.writelines(download_command + "\n")
