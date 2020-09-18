from rest_framework import pagination


class ArticlePagination(pagination.PageNumberPagination):
    """Article pagination to display 10 objects on simple page.
    """
    page_size = 10