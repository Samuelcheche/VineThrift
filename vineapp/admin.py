from django.contrib import admin
from django import forms
from django.utils.html import format_html

from vineapp.models import Order, Product, ProductGalleryImage, customer


@admin.register(customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"full_name",
		"email",
		"phonenumber",
		"submission_type",
		"rating",
		"created_at",
	)
	search_fields = ("full_name", "email", "phonenumber", "product_name")
	list_filter = ("submission_type", "rating", "created_at")
	readonly_fields = ("created_at",)
	fieldsets = (
		("Customer Info", {
			"fields": ("full_name", "email", "phonenumber")
		}),
		("Submission Details", {
			"fields": ("submission_type", "rating", "product_name", "message")
		}),
		("Metadata", {
			"fields": ("created_at",),
			"classes": ("collapse",)
		}),
	)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"customer_name",
		"customer_email",
		"phone_number",
		"product_name",
		"total_amount",
		"payment_status",
		"created_at",
	)
	search_fields = ("customer_name", "customer_email", "phone_number", "product_name")
	list_filter = ("payment_status", "created_at")


class ProductAdminForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = "__all__"
		widgets = {
			"image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
		}


class ProductGalleryImageInline(admin.TabularInline):
	model = ProductGalleryImage
	extra = 2
	fields = ("image", "sort_order", "preview")
	readonly_fields = ("preview",)

	def preview(self, obj):
		if not obj or not obj.image:
			return "No image"
		return format_html(
			'<img src="{}" style="max-height: 90px; border-radius: 8px; border: 1px solid #ddd;" />',
			obj.image.url,
		)

	preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	form = ProductAdminForm
	inlines = (ProductGalleryImageInline,)
	list_display = ("name", "price", "size", "condition", "is_featured", "created_at")
	list_filter = ("condition", "is_featured")
	search_fields = ("name", "description", "tag")
	readonly_fields = ("image_preview",)

	def image_preview(self, obj):
		if not obj or not obj.image:
			return "No image uploaded"
		return format_html(
			'<img src="{}" style="max-height: 140px; border-radius: 10px; border: 1px solid #ddd;" />',
			obj.image.url,
		)

	image_preview.short_description = "Image preview"