from django.core.paginator import Paginator, EmptyPage



def paginate(page: int, items, page_size: int):
    paginator = Paginator(items, per_page=page_size)
    try:
        paginated_items = paginator.page(page)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return {"items": paginated_items.object_list, "count": paginator.num_pages,
            "next": paginated_items.has_next(),
            "previous": paginated_items.has_previous()}
