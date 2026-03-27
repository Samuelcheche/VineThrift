import json

from django.conf import settings
from django.db import DatabaseError, OperationalError
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.decorators.http import require_http_methods

from vineapp.models import Order, Product, customer
# Create your views here.
def index(request):
    return render(request, 'index.html' )

def checkout(request):
    return render(request, 'checkout.html' )

def contact(request):
    return render(request, 'contact.html')


def send_notification_email(subject, message, recipients):
    if not recipients:
        return False

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending error: {str(e)}")
        return False


@require_http_methods(["GET"])
def products_api(request):
    try:
        records = Product.objects.prefetch_related("gallery_images").order_by("-created_at", "-id")
    except (OperationalError, DatabaseError):
        return JsonResponse({"products": []})

    data = []
    fallback_image = request.build_absolute_uri(static("assets/image.png"))

    for record in records:
        image_name = str(record.image or "").strip()
        if image_name.startswith("http://") or image_name.startswith("https://"):
            main_image = image_name
        elif image_name:
            try:
                main_image = request.build_absolute_uri(record.image.url)
            except Exception:
                main_image = fallback_image
        else:
            main_image = fallback_image

        raw_gallery = record.images if isinstance(record.images, list) else []
        gallery = []
        for item in raw_gallery:
            if not isinstance(item, str) or not item.strip():
                continue

            item = item.strip()
            if item.startswith("http://") or item.startswith("https://"):
                gallery.append(item)
            else:
                gallery.append(request.build_absolute_uri(item))

        try:
            gallery_items = record.gallery_images.all()
        except (OperationalError, DatabaseError):
            gallery_items = []

        for gallery_item in gallery_items:
            if gallery_item.image:
                try:
                    image_url = request.build_absolute_uri(gallery_item.image.url)
                except Exception:
                    continue
                if image_url not in gallery:
                    gallery.append(image_url)

        if main_image and main_image not in gallery:
            gallery.insert(0, main_image)
        if not gallery and main_image:
            gallery = [main_image]

        data.append(
            {
                "id": record.id,
                "name": record.name,
                "price": record.price,
                "size": record.size,
                "condition": record.condition,
                "tag": record.tag,
                "image": main_image,
                "images": gallery,
                "description": record.description,
                "is_featured": record.is_featured,
            }
        )

    return JsonResponse({"products": data})


@require_http_methods(["GET", "POST"])
def feedback_api(request):
    if request.method == "GET":
        try:
            records = customer.objects.order_by("-id")[:20]
        except (OperationalError, DatabaseError):
            return JsonResponse({"records": []})

        data = [
            {
                "id": record.id,
                "name": record.full_name,
                "phone": record.phonenumber,
                "email": record.email,
                "type": record.submission_type,
                "rating": record.rating,
                "product": record.product_name,
                "message": record.message,
            }
            for record in records
        ]
        return JsonResponse({"records": data})

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request body."}, status=400)

    full_name = payload.get("name", "").strip()
    email = payload.get("email", "").strip()
    phone = payload.get("phone", "").strip()
    submission_type = payload.get("type", "").strip().lower()
    rating = payload.get("rating", "").strip()
    product_name = payload.get("product", "").strip()
    message = payload.get("message", "").strip()

    if not full_name or not email or not phone or not submission_type or not message:
        return JsonResponse({"error": "Please fill all required fields."}, status=400)

    if submission_type not in {"feedback", "issue", "contact"}:
        return JsonResponse({"error": "Invalid submission type."}, status=400)

    if submission_type == "issue":
        rating = ""

    record = customer.objects.create(
        full_name=full_name,
        email=email,
        phonenumber=phone,
        submission_type=submission_type,
        rating=rating,
        product_name=product_name,
        message=message,
    )

    # Send admin notification email
    send_notification_email(
        subject=f"New {submission_type.title()} From {record.full_name}",
        message=(
            f"Type: {record.submission_type}\n"
            f"Name: {record.full_name}\n"
            f"Email: {record.email}\n"
            f"Phone: {record.phonenumber}\n"
            f"Rating: {record.rating or 'N/A'}\n"
            f"Product: {record.product_name or 'Not specified'}\n\n"
            f"Message:\n{record.message}"
        ),
        recipients=[settings.SHOP_ADMIN_EMAIL],
    )

    # Send customer acknowledgment email
    if submission_type == "issue":
        customer_subject = "We Received Your Issue Report - We're On It!"
        customer_message = (
            f"Hi {record.full_name},\n\n"
            f"Thank you for reporting the issue with {record.product_name or 'your product'}.\n\n"
            f"We have received your report and our team is already looking into it. "
            f"We take all customer concerns seriously and will work to resolve this as quickly as possible.\n\n"
            f"Your Issue Details:\n"
            f"Product: {record.product_name or 'Not specified'}\n"
            f"Message: {record.message}\n\n"
            f"We will follow up with you within 24-48 hours via the contact details you provided.\n"
            f"You can also reach out to us on WhatsApp at our business number for faster support.\n\n"
            f"Best regards,\n"
            f"Vine Thrift Collection Team"
        )
    elif submission_type == "contact":
        customer_subject = "We Received Your Message - Thank You!"
        customer_message = (
            f"Hi {record.full_name},\n\n"
            f"Thank you for getting in touch with us! We have successfully received your message.\n\n"
            f"Your Message:\n"
            f"Subject: {record.product_name or 'General Inquiry'}\n"
            f"Message: {record.message}\n\n"
            f"Our team will review your message and get back to you within 24 hours. If your inquiry is urgent, "
            f"feel free to reach out to us directly via WhatsApp or call us.\n\n"
            f"Contact Information:\n"
            f"Email: support@vinethrift.com\n"
            f"WhatsApp: Available during business hours\n\n"
            f"Best regards,\n"
            f"Vine Thrift Collection Team"
        )
    else:
        customer_subject = "Thank You For Your Feedback - We Appreciate You!"
        customer_message = (
            f"Hi {record.full_name},\n\n"
            f"Thank you so much for taking the time to share your feedback about {record.product_name or 'our products'}!\n\n"
            f"Your thoughts are incredibly valuable to us. We're constantly working to improve our collections and customer experience, "
            f"and feedback like yours helps us become better.\n\n"
            f"Your Feedback:\n"
            f"Rating: {record.rating or 'Not specified'}/5\n"
            f"Product: {record.product_name or 'Not specified'}\n"
            f"Message: {record.message}\n\n"
            f"If you have any follow-up questions or would like to share more, feel free to contact us anytime.\n\n"
            f"Best regards,\n"
            f"Vine Thrift Collection Team"
        )

    send_notification_email(
        subject=customer_subject,
        message=customer_message,
        recipients=[record.email],
    )

    return JsonResponse(
        {
            "record": {
                "id": record.id,
                "name": record.full_name,
                "email": record.email,
                "phone": record.phonenumber,
                "type": record.submission_type,
                "rating": record.rating,
                "product": record.product_name,
                "message": record.message,
            }
        },
        status=201,
    )


@require_http_methods(["POST"])
def clear_feedback_api(request):
    customer.objects.all().delete()
    return JsonResponse({"success": True})


@require_http_methods(["POST"])
def orders_api(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request body."}, status=400)

    customer_name = payload.get("customer_name", "").strip()
    customer_email = payload.get("customer_email", "").strip()
    phone_number = payload.get("phone_number", "").strip()
    delivery_location = payload.get("delivery_location", "").strip()
    notes = payload.get("notes", "").strip()
    product_id = payload.get("product_id")
    product_name = payload.get("product_name", "").strip()
    product_price = int(payload.get("product_price", 0) or 0)
    delivery_fee = int(payload.get("delivery_fee", 300) or 300)

    if not customer_name or not customer_email or not phone_number or not delivery_location:
        return JsonResponse({"error": "Please fill all required delivery fields."}, status=400)

    if not product_name or product_price <= 0:
        return JsonResponse({"error": "Invalid product details for checkout."}, status=400)

    product = None
    if product_id:
        product = Product.objects.filter(id=product_id).first()

    total_amount = product_price + delivery_fee

    order = Order.objects.create(
        customer_name=customer_name,
        customer_email=customer_email,
        phone_number=phone_number,
        delivery_location=delivery_location,
        notes=notes,
        product=product,
        product_name=product_name,
        product_price=product_price,
        delivery_fee=delivery_fee,
        total_amount=total_amount,
        payment_method="mpesa",
        payment_status="stk_sent",
    )

    admin_email_sent = send_notification_email(
        subject=f"New Order #{order.id} - {order.product_name}",
        message=(
            f"Order ID: {order.id}\n"
            f"Customer: {order.customer_name}\n"
            f"Email: {order.customer_email}\n"
            f"Phone: {order.phone_number}\n"
            f"Location: {order.delivery_location}\n"
            f"Product: {order.product_name}\n"
            f"Amount: KES {order.total_amount}\n"
            f"Notes: {order.notes or 'None'}"
        ),
        recipients=[settings.SHOP_ADMIN_EMAIL],
    )

    customer_email_sent = send_notification_email(
        subject=f"Order Confirmation #{order.id} - Vine Thrift",
        message=(
            f"Hi {order.customer_name},\n\n"
            f"Your order has been received successfully.\n"
            f"Product: {order.product_name}\n"
            f"Total: KES {order.total_amount}\n"
            f"Delivery Location: {order.delivery_location}\n\n"
            f"We will contact you shortly on WhatsApp/Phone for delivery."
        ),
        recipients=[order.customer_email],
    )

    return JsonResponse(
        {
            "order": {
                "id": order.id,
                "customer_name": order.customer_name,
                "customer_email": order.customer_email,
                "product_name": order.product_name,
                "total_amount": order.total_amount,
            },
            "email": {
                "admin_sent": admin_email_sent,
                "customer_sent": customer_email_sent,
            },
        },
        status=201,
    )