from datetime import datetime
from blog.models import Post, Tag


def latest_post(request):
    return {
        'latest_post': Post.objects.latest('created')
    }


def tags(request):
    return {
        'tags': Tag.objects.order_by('name')
    }


def month_count(request):

    # Months to count the
    months = {
        'January': 0,
        'February': 1,
        'March': 2,
        'April': 3,
        'May': 4,
        'June': 5,
        'July': 6,
        'August': 7,
        'September': 8,
        'October': 9,
        'November': 10,
        'December': 11,
    }

    number_to_month = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'November',
        'December'
    ]
    month_count = {}
    current_year = datetime.today().year
    year_month_count = {}
    year_count = {}
    overall_array = []

    # Before Y2K, nothing existed
    # for year in range(2000, current_year + 1):  # + 1 because Python range is weird
    #     for month in range(0, 13):
    #         if Post.objects.filter(created__year=year).filter(created__month=month).count() > 0:
    #             # Create a tuple consisting of (YEAR, MONTH, MONTH_COUNT)
    #             # We need to have multiple data objects attached to one year. I like the idea of a dictionary inside of an array.
    #             # --> That way you can easily insert items
    #             overall_array.append(year_count[year] = [
    #                 year_month_count[month] = Post.objects.filter(created__year=year).filter(created__month=month).count()
    #             ])
    #         #     =  [{
    #         #
    #         #
    #         #             number_to_month[month]: Post.objects.filter(created__year=year).filter(created__month=month).count(),
    #         #         }]
    #         #     }
    #         # )


    for month in months:

        # Create key of 'month' with the value of the month count by filtering
        month_count[month] = Post.objects.filter(created__month=months[month]).count()

    return {

        'month_count': month_count,
        'year_count': year_count,
    }
