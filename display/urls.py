
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import userviews

urlpatterns = [
    path("", views.index_page, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/<int:item>", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
#     path("room/", views.room, name="room"),
    path("service/", views.service, name="service"),
    path("logout/", views.logouts, name='logout'),
    path("token/", views.token, name='token'),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('error/', views.error_page, name="error"),
    path("forget_pass/", views.forget_pass, name="forget_pass"),
    path("change_pass/<token>/", views.change_pass, name="change_pass"),
    path("reseterror/", views.reseterror, name="reseterror"),
    path("book_search/<int:item>", userviews.book_search, name="book_search"),
    path("addtowishlist/",
         userviews.addtowishlist, name="addtowishlist"),
    path("showwishlist/", userviews.showwishlist, name="showwishlist"),
    path('removewishlist/',
         userviews.removewishlist, name='removewishlist'),
    path('removewishlistpage/<int:id>',
         userviews.removewishlistpage, name='removewishlistpage'),
    path('profile/', userviews.profile, name='profile'),
    path('save_profile/', userviews.save_profile, name='save_profile'),
    path('postads/', userviews.postads, name="postads"),
    path('details/<int:item>', userviews.details, name="details"),
    path('uploadads/', userviews.uploadads, name="uploadads"),
    path('soldout/<int:item>',
         userviews.soldout, name='soldout'),
    path('getinformation/', userviews.getinformation, name="getinformation"),   

#     path('showcart/', userviews.showcart, name="showcart"),
#     path("addtocart/", userviews.addtocart, name="addtocart"),
#     path("removecartpage/<str:id>",
#          userviews.removecartpage, name="removecartpage"),
#     path("checkout/", userviews.checkout, name="checkout"),
#     path("payment/", userviews.payment, name='payment'),
#     path("updatequantity/", userviews.updatequantity, name='updatequantity'),
    path("myorders/", userviews.myorders, name='myorders'),
#     path("room/pricing/", userviews.pricing, name="pricing"),
#     path("room/purchase/", userviews.purchase, name="purchase"),
#     path("room/room_payment/", userviews.room_payment, name="room_payment"),
#     path("tableorder/", userviews.roomorder, name="roomorder"),
#     path("sortby/", userviews.sortby, name='sortby'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)