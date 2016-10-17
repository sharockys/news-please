import sys
import logging
from copy import deepcopy
from newscrawler.pipeline.km4_extractor.extractors.abstract_extractor import *
# Import Newspaper Article Extractor Library.
if sys.version_info[0] >= 3:
    from newspaper import Article


class Extractor(AbstractExtractor):
    """This class implements Newspaper as an article extractor. Newspaper is
    a subclass of ExtractorsInterface
    """

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.name = "newspaper"
        if sys.version_info[0] < 3:
            self.log.error("Newspaper doesn't support Python 2.X! The newspaper_extractor will be disabled.")


    def extract(self, item):
        """Creates an instance of Article without a Download and returns an ArticleCandidate with the results of
        parsing the HTML-Code.

        :param item: A NewscrawlerItem to parse.
        :return: ArticleCandidate containing the recovered article data.
        """
        article_candidate = ArticleCandidate()
        article_candidate.extractor = self._name()

        if sys.version_info[0] >= 3:
            article = Article('')
            article.set_html(deepcopy(item['spider_response'].body))
            article.parse()
            article_candidate.title = article.title
            article_candidate.description = article.meta_description
            article_candidate.text = article.text
            article_candidate.topimage = article.top_image
            article_candidate.author = article.authors
            if article.publish_date is not None:
                article_candidate.publish_date = article.publish_date.strftime('%Y-%m-%d %H:%M:%S')
            article_candidate.language = article.meta_lang

        return article_candidate