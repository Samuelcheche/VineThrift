from django.db import models

# Create your models here.
class customer(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField(default='noemail@example.com')
    phonenumber = models.CharField(max_length=20)
    submission_type = models.CharField(max_length=20)
    rating = models.CharField(max_length=10, blank=True)
    product_name = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    size = models.CharField(max_length=20)
    condition = models.CharField(max_length=30)
    tag = models.CharField(max_length=60, blank=True)
    image = models.ImageField(upload_to="products/")
    images = models.JSONField(default=list, blank=True)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductGalleryImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="products/gallery/")
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.name} - Gallery Image {self.id}"


class Order(models.Model):
    customer_name = models.CharField(max_length=140)
    customer_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    delivery_location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")
    product_name = models.CharField(max_length=140)
    product_price = models.PositiveIntegerField()
    delivery_fee = models.PositiveIntegerField(default=300)
    total_amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=40, default="mpesa")
    payment_status = models.CharField(max_length=30, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"