from django.db import models
from django.contrib.auth.models import AbstractUser

PAGES = [
    ("products", "Products List"),
    ("marketing", "Marketing List"),
    ("orders", "Order List"),
    ("mediaplans", "Media Plans"),
    ("offers", "Offer Pricing SKUs"),
    ("clients", "Clients"),
    ("suppliers", "Suppliers"),
    ("support", "Customer Support"),
    ("sales", "Sales Reports"),
    ("finance", "Finance & Accounting"),
]


class User(AbstractUser):
    is_super_admin = models.BooleanField(default=False)

class PagePermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="page_permissions")
    page = models.CharField(max_length=50, choices=PAGES)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "page")

class Comment(models.Model):
    page = models.CharField(max_length=50, choices=PAGES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentHistory(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="history")
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    previous_text = models.TextField()
    modified_at = models.DateTimeField(auto_now_add=True)