from generics.spiders import JAVSpider
from generics.utils import extract_a

from . import pagen, get_type
from . import get_article, article_json

desc_xp = './/div[@class="tx-work mg-b12 left"]/text()'


class SeriesSpider(JAVSpider):
    name = 'dmm.series'

    start_urls = (
        'http://www.dmm.co.jp/digital/videoa/-/series/',
        'http://www.dmm.co.jp/mono/dvd/-/series/',
    )

    def parse(self, response):
        for cell in response.xpath('//td'):
            try:
                l = extract_a(cell)
                next(l)
                url, t = next(l)
            except StopIteration:
                continue
            if not t or '=' not in url:
                continue

            a = get_article(url, t)
            if a is None:
                continue

            desc = ''.join(cell.xpath(desc_xp).extract()).strip()
            if desc:
                a['description'] = desc

            article_json(a)
            yield a

        if get_type(response.url) == 'mono':
            pn = pagen
        else:
            pn = '(//div[@class="paginationControl"])[1]'

        for url, t in extract_a(response.xpath(pn)):
            try:
                yield response.follow(url, meta={'page': int(t)})
            except ValueError:
                pass
