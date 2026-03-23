import json

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings

from vineapp.models import Order, Product, ProductGalleryImage, customer


@override_settings(
	ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"],
	EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
	SHOP_ADMIN_EMAIL="admin@vinethrift.local",
)
class FeedbackApiTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_post_feedback_saves_to_database(self):
		payload = {
			"name": "Test User",
			"email": "testuser@example.com",
			"phone": "0712345678",
			"type": "feedback",
			"rating": "5",
			"product": "Nike Air Max",
			"message": "Great service",
		}

		response = self.client.post(
			"/api/feedback/",
			data=json.dumps(payload),
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(customer.objects.count(), 1)
		saved = customer.objects.first()
		self.assertEqual(saved.full_name, "Test User")
		self.assertEqual(saved.email, "testuser@example.com")
		self.assertEqual(saved.submission_type, "feedback")

	def test_feedback_sends_admin_and_customer_emails(self):
		"""Test that both admin and customer receive emails on feedback submission"""
		payload = {
			"name": "John Doe",
			"email": "john@example.com",
			"phone": "0712345678",
			"type": "feedback",
			"rating": "4",
			"product": "Nike Air Max",
			"message": "Very comfortable shoes",
		}

		response = self.client.post(
			"/api/feedback/",
			data=json.dumps(payload),
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 201)
		# Should send 2 emails: 1 to admin, 1 to customer
		self.assertGreaterEqual(len(mail.outbox), 2)
		# Check admin email
		admin_email = mail.outbox[0]
		self.assertIn("John Doe", admin_email.body)
		# Check customer acknowledgment email
		customer_email = mail.outbox[1]
		self.assertIn("john@example.com", customer_email.recipients())

	def test_issue_sends_admin_and_customer_emails(self):
		"""Test that both admin and customer receive emails when issue is reported"""
		payload = {
			"name": "Jane Smith",
			"email": "jane@example.com",
			"phone": "0722222222",
			"type": "issue",
			"rating": "",
			"product": "Adidas Ultraboost",
			"message": "Sole is starting to peel off",
		}

		response = self.client.post(
			"/api/feedback/",
			data=json.dumps(payload),
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 201)
		# Should send 2 emails: 1 to admin, 1 to customer
		self.assertGreaterEqual(len(mail.outbox), 2)
		# Check that customer email subject indicates issue is being worked on
		customer_email = mail.outbox[1]
		self.assertIn("Issue Report", customer_email.subject)

	def test_contact_form_sends_emails(self):
		"""Test that contact form submissions send both admin and customer emails"""
		payload = {
			"name": "Contact User",
			"email": "contact@example.com",
			"phone": "0700000000",
			"type": "contact",
			"rating": "",
			"product": "Partnership Inquiry",
			"message": "I'm interested in becoming a wholesale partner",
		}

		response = self.client.post(
			"/api/feedback/",
			data=json.dumps(payload),
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(customer.objects.count(), 1)
		# Should send 2 emails: 1 to admin, 1 to customer
		self.assertGreaterEqual(len(mail.outbox), 2)
		# Check admin email
		admin_email = mail.outbox[0]
		self.assertIn("Contact User", admin_email.body)
		# Check customer acknowledgment email
		customer_email = mail.outbox[1]
		self.assertIn("contact@example.com", customer_email.recipients())
		self.assertIn("received your message", customer_email.body.lower())

	def test_clear_feedback_removes_records(self):
		customer.objects.create(
			full_name="Jane",
			email="jane@example.com",
			phonenumber="0711111111",
			submission_type="issue",
			rating="",
			product_name="",
			message="Broken sole",
		)

		response = self.client.post(
			"/api/feedback/clear/",
			data="{}",
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(customer.objects.count(), 0)


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class ProductApiTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_products_api_returns_backend_products(self):
		uploaded_image = SimpleUploadedFile(
			"shoe.jpg",
			b"fake-image-content",
			content_type="image/jpeg",
		)
		gallery_image = SimpleUploadedFile(
			"shoe_gallery.jpg",
			b"fake-gallery-image",
			content_type="image/jpeg",
		)

		product = Product.objects.create(
			name="Nike Air Max 90",
			price=4500,
			size="UK 9",
			condition="Like New",
			tag="Trending",
			image=uploaded_image,
			images=["https://example.com/one.jpg", "https://example.com/two.jpg"],
			description="Quality thrift pair",
			is_featured=True,
		)

		ProductGalleryImage.objects.create(
			product=product,
			image=gallery_image,
			sort_order=1,
		)

		response = self.client.get("/api/products/")
		data = response.json()

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(data["products"]), 1)
		self.assertEqual(data["products"][0]["name"], "Nike Air Max 90")
		self.assertEqual(data["products"][0]["price"], 4500)
		self.assertGreaterEqual(len(data["products"][0]["images"]), 2)


@override_settings(
	ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"],
	EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
	SHOP_ADMIN_EMAIL="admin@vinethrift.local",
)
class OrdersApiTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.product = Product.objects.create(
			name="Test Shoe",
			price=5000,
			size="UK 8",
			condition="Like New",
			tag="Hot",
			image=SimpleUploadedFile("shoe.jpg", b"fake-image-content", content_type="image/jpeg"),
			description="Test pair",
		)

	def test_orders_api_creates_order_and_sends_email(self):
		payload = {
			"customer_name": "John Doe",
			"customer_email": "john@example.com",
			"phone_number": "0712345678",
			"delivery_location": "Nairobi CBD",
			"notes": "Call before delivery",
			"product_id": self.product.id,
			"product_name": self.product.name,
			"product_price": self.product.price,
			"delivery_fee": 300,
		}

		response = self.client.post(
			"/api/orders/",
			data=json.dumps(payload),
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(Order.objects.count(), 1)
		order = Order.objects.first()
		self.assertEqual(order.customer_name, "John Doe")
		self.assertEqual(order.total_amount, 5300)
		self.assertGreaterEqual(len(mail.outbox), 2)
