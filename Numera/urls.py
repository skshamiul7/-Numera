"""
URL configuration for Numera project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),

    # Original 6 tools
    path('EvenOdd/', views.evenodd, name='evenodd'),
    path('factorial/', views.factorial, name='factorial'),
    path('fibonacci/', views.fibonacci, name='fibonacci'),
    path('prime/', views.prime, name='prime'),
    path('gcd/', views.gcd, name='gcd'),
    path('palindrome/', views.palindrome, name='palindrome'),

    # 38 new tools
    path('lcm/', views.lcm, name='lcm'),
    path('perfect/', views.perfect, name='perfect'),
    path('armstrong/', views.armstrong, name='armstrong'),
    path('prime-factor/', views.prime_factor, name='prime_factor'),
    path('sieve/', views.sieve, name='sieve'),
    path('twin-prime/', views.twin_prime, name='twin_prime'),
    path('coprime/', views.coprime, name='coprime'),
    path('digital-root/', views.digital_root, name='digital_root'),
    path('digit-ops/', views.digit_ops, name='digit_ops'),
    path('sum-series/', views.sum_series, name='sum_series'),
    path('ap/', views.ap, name='ap'),
    path('gp/', views.gp, name='gp'),
    path('power/', views.power, name='power'),
    path('roots/', views.roots, name='roots'),
    path('mod-exp/', views.mod_exp, name='mod_exp'),
    path('pascal/', views.pascal, name='pascal'),
    path('collatz/', views.collatz, name='collatz'),
    path('area-perimeter/', views.area_perimeter, name='area_perimeter'),
    path('volume-area/', views.volume_area, name='volume_area'),
    path('pythagorean/', views.pythagorean, name='pythagorean'),
    path('distance/', views.distance, name='distance'),
    path('midpoint/', views.midpoint, name='midpoint'),
    path('slope/', views.slope, name='slope'),
    path('stats/', views.stats, name='stats'),
    path('variance/', views.variance, name='variance'),
    path('minmax/', views.minmax, name='minmax'),
    path('quartiles/', views.quartiles, name='quartiles'),
    path('combinatorics/', views.combinatorics, name='combinatorics'),
    path('base-converter/', views.base_converter, name='base_converter'),
    path('binary-decimal/', views.binary_decimal, name='binary_decimal'),
    path('roman/', views.roman, name='roman'),
    path('unit-converter/', views.unit_converter, name='unit_converter'),
    path('temperature/', views.temperature, name='temperature'),
    path('random-number/', views.random_number, name='random_number'),
    path('dice-coin/', views.dice_coin, name='dice_coin'),
    path('prime-counter/', views.prime_counter, name='prime_counter'),
    path('happy/', views.happy, name='happy'),
    path('kaprekar/', views.kaprekar, name='kaprekar'),
]