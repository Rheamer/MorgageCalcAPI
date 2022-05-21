from rest_framework.routers import DefaultRouter
import calculator.views as views

router = DefaultRouter()
router.register("offer", views.OfferApiView, basename='offer')
router.register("offer/<int:id>/", views.OfferDetailApiView, basename='offerid')
