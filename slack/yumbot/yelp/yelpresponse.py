class YelpResponse(object):

    def __init__(self, id, name, image_url, is_closed, url, price,
                 rating, review_count, phone, photos, hours, categories,
                 location, transactions):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.is_closed = is_closed
        self.url = url
        self.price = price
        self.rating = rating
        self.review_count = review_count
        self.phone = phone
        self.photos = photos
        self.hours = hours
        self.categories = categories
        self.location = location
        self.transactions = transactions