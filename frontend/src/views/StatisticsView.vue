<template>
  <div class="bg-gray-50 min-h-screen py-12">
    <div class="max-w-6xl mx-auto px-4">
      <h1 class="text-3xl font-bold text-center text-gray-900 mb-8 font-roboto">Database Statistics</h1>

      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <div class="text-red-600 mb-2">
          <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-red-800 mb-2">Failed to load statistics</h3>
        <p class="text-red-600">{{ error }}</p>
        <button @click="loadStatistics"
          class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">
          Retry
        </button>
      </div>

      <!-- 成功状态 -->
      <div v-else-if="stats" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <!-- Compounds 卡片 -->
        <div
          class="rounded-2xl p-6 border border-gray-300 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg"
          style="background-color: #F9FAFB;">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <div class="w-12 h-12 rounded-full flex items-center justify-center mr-4"
                style="background-color: #16A34A1A;">
                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="none"
                  version="1.1" width="14" height="16" viewBox="0 0 14 16">
                  <path
                    d="M9,32L5,32L9,32L4,32Q3.5625,32,3.28125,31.71875Q3,31.4375,3,31Q3,30.5625,3.28125,30.28125Q3.5625,30,4,30L4,25.84375Q4,25.28125,3.71875,24.8125L0.3125,19.3125Q0,18.78125,0,18.15625Q0.03125,17.25,0.625,16.625Q1.25,16.03125,2.15625,16L11.84375,16Q12.75,16.03125,13.375,16.625Q13.96875,17.25,14,18.15625Q14,18.78125,13.6875,19.3125L10.3125,24.8125Q10,25.28125,10,25.84375L10,30Q10.4375,30,10.71875,30.28125Q11,30.5625,11,31Q11,31.4375,10.71875,31.71875Q10.4375,32,10,32L9,32ZM6,25.84375L6,30L6,25.84375L6,30L8,30L8,25.84375Q8,24.71875,8.59375,23.75L9.6875,22L4.34375,22L5.40625,23.75Q6,24.71875,6,25.84375Z"
                    fill="#16A34A" fill-opacity="1" style="mix-blend-mode:passthrough"
                    transform="matrix(1,0,0,-1,0,32)" />
                </svg>
              </div>
              <div class="text-4xl font-bold" style="color: #000000; font-family: 'Roboto', sans-serif;">
                {{ formatNumber(stats.Compounds) }}
              </div>
            </div>
          </div>
          <div class="text-lg" style="color: #4B5563; font-family: 'Roboto', sans-serif;">
            Documented Compounds
          </div>
        </div>

        <!-- Mushroom 卡片 -->
        <div
          class="rounded-2xl p-6 border border-gray-300 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg"
          style="background-color: #F9FAFB;">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <div class="w-12 h-12 rounded-full flex items-center justify-center mr-4"
                style="background-color: #16A34A1A;">
                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="none"
                  version="1.1" width="24" height="24" viewBox="0 0 24 24">
                  <defs>
                    <pattern x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse" id="master_svg0_7_6185">
                      <image x="0" y="0" width="24" height="24"
                        xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJAAAACQCAYAAADnRuK4AAAAAXNSR0IArs4c6QAAAARzQklUCAgICHwIZIgAABG9SURBVHic7Z19kFxVmcaf53TPTBITM5OZ7iwfrpbgikiE4Mr6gRgUyHSHhBCTWZN0T2TBsnbVKnXXUtTCoLJYu5Zs7WrtIiCmu8dsTWJMiOnuJKARUNmyJCrg6kpYFdClezIzMZDJzHTfZ/+YREyYhD63753uGc7vv5m+7znPvf32Ofec8573AA6Hw+FwOBwOh8PhmDrYaAEA0N6XfGWkgouM0espngfoLIFnEOoSMRvArGOXHqUwInCA0O8BPi3qF57HxzyM7R/acO9vG3wrz7MRJnZOcgOgXoivmfinHhWRHThQ2IyN8BqsMBAa4kBz+xOx2WNKwmMC4KUkzgqiXEFPQfg+jApHTcuuw+t2DgRRri1z+xOx2aMsEHjjZJ9LenBkFlY921MoT726YJkyB+q6a8U8to2vgYdegG8nYcKsT4IH6AEYZNA60l/u2fdsmPX9kdvf2BKbs/BHBC58EYGPVQzeOpgq/GFKdIVE6A7UtSn5F4b6CMBeEHPCrm9SpOcAZBWpfKm8fu+vwqyqK5N4nyG/WpMsqFBum7scPVuqYWoKk9AcqCOz7IIWep+VeE3YrU2tSPBI7RiXuWmod9ejYdQRyya+S3CJhcltpXT+o2FomQoCd6AFucTZUfFWCeuaxXFORoJHoK9i9MnBVOGpIMuOZ5NlAF12erwbyr3Fu4LUMVUE9wVvhIllkh+IePw5gFSzOg8AkDAg0hHhsXiu+++gQH9IVs5zTNG/d2US7whQw5QRyINbsPmqV0Qq0RyBy4Iob6oRcH81WkkNrt3zZL1lxbNJ+ROhg4yYS55Zv+uJejVMJXW3Ep3ZxMpIJfrT6eo8mPgVXRYdj/ykM5tY2TgR7JTn7VyQS7y8YRp84N+BBMYziZsNsI1AR6CqGgG5wADb4pnEzQF3aTYizo942IyNzdv9n4y/B5VPtMUOso/AuwNX1AQI2lruRArJwqitre8u7ES+VErn/z6AckLH2tNj/UvmxgeQn6nOAwAEV8cPYlesf8ncBkn4aCyX+JsG1W2FVQsU618yl6Oz9wJ8c+BKpEEAPwHxsCfuF3AA0cohMxodLi/UEJ4ZYQxz2r22Sjsq0fkEzjHUYggXA7gI5IIQNP1Qs0auspnFDqgFAoAxoXpFOb37gYDKC4XaHejuJbNikTl5EpcHVfmxtautpNlSSu36IQifIxgwnlv2FslbA2I1wbOD0gjpO6UuJGvtzgJ0IAAYGFXlkkO9e/43wDIDpTYHEhjPJb4J8NogKhW0R9CtA6ni93w7zakLZ1eu+x0EbyR4VSBFCtvK6fzqWrQG7ECA8Kg3Hn3rwPX3HA603ICo6R0olkt8PgjnkbSzSu+ScrqwdCBd3Be48wAAoYF0cV85XVhapXeJpJ11F0msimUTnwtGoG3luICtlaYdmb1oCxTLJVZT3FJPJRKeBnFDOZ0v1lOOX2LZZDeEO+sNGxG1ppwqbD3dNYG3QM/X/sVSuvCxcMr2z2m9ur0v+UoId9ZXhfrGq0cuaJTzAEA5nS+OV49cAKivroI83tHel3xlYMKs4D/EMsn3NqbuU3NqB9oI0+rhGwTn+ylY0jigDaV0ITV83b7hOjQGwvB1+4ZL6UIK0IYJbfaQaG+pKteo7oTE7bFN3Zc2ou5TccoHEXt18oMA3uqnUEGHPKC7lC5k6lIXAqV0IeMZJQT5CuQieWns3MQHgldWE60kt7Vv7n5Vg+p/AZM60IJc4mwAn/dToKDfVci3H+wtfKdudSFxMFW8r0JeKuh3vgrweMuxZzT1kLHWCu/pumvFvIbUfxKTOlBU+AIJa4GCDlXI7qFU/pFA1IXIUCr/SIXs9tMSkZgXFW8NR1lNChaxZbyvGUZmLxDQkUsukrjWtiBJ456wajo4z3GGUvlHPGqVn3ciCes6MssuqFeD31aQ5PKuc5JfqLf+enmBA7VIN/sJBiN4fTN3W6fiYKp4H4kbbO1ImBZ6n623fo9aCWDEj60BPhbLdW+oV0M9nOAosb4rXyPxGh/l5Eq9+WxwsqaWiZd9+yG+xGtifVe+pp66D6aKP/Lk+V44pcxX47nE2+rRUA8nOJC86EdsWx8JT49VjnwocGVTzFhl5IMSnraxIWHgtXy43roHeov/KfobtABohYdtjZqfet5Zdi6fQzFlWwDhXd8M8zz1MnzdvmH46MogpLFzed3blcrr8zdJ2ObLmIy3etrZiPCTPzpQfLiy2nbkJWlnqbe4OxRlDaCczhclfNvGhsS8+FC1/tgoQgaVXgE/8VnAIo7OnvKR2Z9UZt/6VA3+MWA9DadqdIutjSjrZzcZz/Tuea4arawA8Iy/Ergidk5iSr8TAwAd/VfMl2SzGQ4SvjuYKjwUmrIGMZgqPCRon5WRcHlQwfCDa/c8WfG8ayFZh9NiYjT88XgmmQ5CSy0YAIiOtXSTbLExpFHD5yDCgrK7N5ItEbE7qPoHNxR/CPB9/kvQHQs2db8lKD2nY6IL83ilpd0zpccL94aiqAkoPVHc66MbsX2Gp9fQm8960j/5MibbosZ8q2PTFX8epKbJmHAgymqFV8A3Z0p+m0nZCM+D7EZEQuCr5ANPFG6sIyBuYdS03rMwc9XLApZ1Ambepnd1EnytjZHg1RVgNi0wxuoeSZw3b9O7OgPVsBGexlvWQ/CVCILAhWIkF+Y+N9PK1tPnsTkJQX8YOFC8PyxBzcJAy5z7bRda26Kz3hC4juvvOTzW4i0H4DNZFlfGsknrkWWtGGPweisLYf+M7r6O07OlCtBqToaeZ/csa2R4bfHXQnUVgDE/9iRu7Mx1BzLVcDIG4nl2YvhwGEKaE+23u56vC0tJOb37AVF/69c+4vHOBblE4Pv5DKRXWFkIlg91+kLA6sdCKNQgs3Kq8DUAt/kyJtui4vYFm6+y+75fBAPLnQoVo1BTxDUTFc/uXgUGkiz0dJTaXvYxAX43KCyMVKKBjswMhJiNAU112i+c1goZsbtXKR6amOP0bKlW2sbeI+G//ZgTuEiMZIMamRmAVguoZjT6EnKgit29klOyGj7Uc+8hsLriWD4BH/Daic2i9WMAWTVnZRx5yTjQQGV0yMpAmrJwinJ69+NexKwWVPFjT/CTXdnE+np1NDwoeyZBMqRdqZMzsH7Xdyn6DuYzwp2dmeRf1aPBAHzOxiCGOe31VDid6Iq2WWVeE2D1LIOg1Jv/Dwlf8WVMzjLA9nq2KBlAVlkfvLbKS8aBpKjdvUpTkw3/JMqvOPJhCL4Wt0n8WcTDPX6jKg0Iq/Ma5EVeQg5UtbtXshSamNNx+b7KaIQ9AnxNsZBcHBuq+hqZGVgGkkc91rULYToRNXb3SsjqWQbJofW7hgRvuQRfgxwSq2J9SettSgakXW5kYrFtJdMVARfbXc9As97bMpAu/pJGfy3A19kbFD7dlU1abSo1oH5hYyDJ6qFOb2j5Y5Gvyb0gKaUKeyD4PnvDSF/r7Ft6Sc3Xex4es6qBWNwMe7JDp39NBNBFNiYyxu5ZhkS5N/+vkO7wZUzOMp7Z3rnp6pqWZcxYNPozq/LBl3ed0z1ts9LXStf4kcsIWgXKj1aOWj3LMCmNlD5gvTngGATPMKZa08jMHF63c0DC/9hVYNb4ETat8DyrexT0y8Mb7jsYniBL3v/j8aPe2GoAvs7eIHhxbLiy6cVGZse7IqtcxATePaO7sY0wBlxlZSM+GJYcvxzecN/BCrVcgq8MrwRXx7OJjae7ZsIJjPZalr0wfm7iCj+ipgPxV3dfCWChlRGxJzRBdTCYKvxcrK6dOALUB+RNXZnu95zqYwMAldbxom2OHHn8hC9B0wDR7t4kjVfaxpp2i/dAevcuUh/3a29ovtaZ637TpJ/hWHgASasXLhKXhxEi2WgW5BJvtjyyEiT3DfXceyg8VfVTShe+KOHrPs1nG3HSkdmfvMcoZ1tqxMMnfQpqWiIeP2VtJEyL3EjlWS97v6Dv+7EleKYx3g70v2X2n/7/jw5Uao9utX3ZIrk8nule6kdQMxLLJrtJXG1jI+FwqSPyzfBUBUjPlrERVVcB+I0fcwJvjB3tOGFk9nwLtHznEdG+FRLMXe13L5n2C6ztdy9p95VUnchi+c4joYgKgWd795TgeSsEf5EDJNbEc8nPHP/7hKE4TeU227d1Eme1Ruf8mx8xzURrdPaXbY9CkODBjP9LeKrCobSh+DPPY0qQrwA4QTfFsskenOxA5fV7f0Vqh48yU1OZUiRo4tlEL0Dr8E5SO8rr907LXSoHN+R3QD7e9ybeh0jg612Z5F++YDJwnPyMnzkDQXd1ZhLv9COokXRmEu+Uj65LgjdOfqaGS5uWcm/+1jrOD5lNascLHGgolX+E1Gbb0ki2GGJbRy65yKegKacjl1xkiG22uZEw0XV/YzrlxD4VpcrIDRD+y48twTMnXY6oEJ/wM/1NcH5UKk4HJ+rIJRdFpaKfw2QkHK5QN4ajbIq5bt9RVbFSkK9YpkkdaDBVeArAp/0USPDMqPRAM3dnnZnEO6PSAwTP9FWA0aeOPaMZQfm6/P8J3jUQrEeTp1wQLT+R/zKAH/gRRHC+AYrN+GIdzyTTBvDV8mBi2eLB8uMFf7sgmpiB9O6HZbTBdmR2uvPCvDGDdYJ8TdGTbAGRiWeT2WaYJ2q/e0l7PJvMgsj4eefBRNc1PB5haqamtymnClsJ3mxjc9qQjOH1+d9AqiPZIwAg1RKZ82gjZ6zjme6lLZE5jwKoL0eO0fuG1+d9zeJOF0qp/GcF9Nd6/YvG9JR7i1sE1ZV7mMRZoCnGs4kdp1rVDYPOXPeb4tnEDtAU6z4vVbrlxc5LnREQKrcNvVfAj2u7vBaCPvZb2i3g1oF04f5Qjv3OJi4jcCPJQFq9MI/9LqXzoeUvrIfOTVefZUz1RwTPON11tYu/e8msWGROnsTlQQjEhCM9SXJrxfO2DPYWH/LtTAIXZLrfHDVmjaA1BINL9CR9p9SFJJKFmhJ/zxQHAoDOvqWXRKrmeyBnneoaK/Gx/iVzOTp7L8Dg44CkQRD7PfBhAPslPEF6wyYyPlxqbx0GgPjwWLtXbWmXTDuJVwNYbKCLISwGuSBwTdBDahu5styzr+aFx5nkQADQlUmuM8QpZ6utxcf6l8zl0dk7QDbtPE8w6D61jay0cR7MQAcCgFg2cQvBSWO/rAPjyz37ni11ISlgesTA+EDQ1lInltk6z0ylnCp8GtC3JvvM386KZGG0nMqvAfS5esU1ExOTaPpcOVXoqfWd5yUBIaqaFvDTkz/yvzWHUClduAn0Vgmwy+TVhAgY8oBVE/cU8MhwBvBM757nKt7YCkgnZCCpe29XKVX8VjVauVCWe8uaCQH3V6OVCw+mC9sbraWZGdpw729Bc8JRVIFsDhxcu+fJ8oH8EkEf8ruJrRFIOCzhg+UD+csH1+6xy1LyEqWU3vUDGb3/+N/B7S7dCK+cLny5anQ+oD7fG9mmgAlt6qsanV/uzX8l0LUtmxVtacpT4gVBOVXc5AH/jDCSbA6mCk+V0oVUxeAiQNv9xt2GwbGX5O0V8MJSupAKJyRDj1tcfCD4+qeGgQP5T0j4dmj724dS+UdK6cK1gl4H4HY/sSaBMVH37fJ4XilduHaod5ev45NqpPb3KHLSofG0YCM8jUfXTdkkVtddK+axZawHNBsgvM32fHpbJHggHoS8jMZb+weuv2dK3s3m9y3raK16PyV52jMpJD05Xh15w3Q/Mr0hs6Bz+xOx2aO8GtJSgJfWu1J+HAlPA3oQ5O6RNn372Z6CVQLRoOjIJRdFPe06lRNJerJiuGwmxFQ3xTR6++buV7VWsVgezyf4WgFnAziDRBeEOSLaMHEY7lGQIxIGAPyewFOCfkmjn49FsH94bfHXjb6X48zvW9bRVvU+DGAlwHMn/qvHAWwfq47cNt1bHofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcDofD4XA4HA6Hw+FwOBwOh8PhcDgcjpnF/wMZsNsg+hIeWwAAAABJRU5ErkJggg==" />
                    </pattern>
                  </defs>
                  <rect x="0" y="0" width="24" height="24" rx="0" fill="#000000" fill-opacity="0"
                    style="mix-blend-mode:passthrough" />
                  <rect x="0" y="0" width="24" height="24" rx="0" fill="url(#master_svg0_7_6185)" fill-opacity="1"
                    style="mix-blend-mode:passthrough" />
                </svg>
              </div>
              <div class="text-4xl font-bold" style="color: #000000; font-family: 'Roboto', sans-serif;">
                {{ formatNumber(stats.Mushroom) }}
              </div>
            </div>
          </div>
          <div class="text-lg" style="color: #4B5563; font-family: 'Roboto', sans-serif;">
            Toxic Mushroom Species
          </div>
        </div>

        <!-- Toxicity 卡片 -->
        <div
          class="rounded-2xl p-6 border border-gray-300 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg"
          style="background-color: #F9FAFB;">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <div class="w-12 h-12 rounded-full flex items-center justify-center mr-4"
                style="background-color: #16A34A1A;">
                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/2000/svg" fill="none"
                  version="1.1" width="14" height="16" viewBox="0 0 14 16">
                  <path
                    d="M3,32Q1.71875,31.96875,0.875,31.125Q0.03125,30.28125,0,29L0,19Q0.03125,17.71875,0.875,16.875Q1.71875,16.03125,3,16L12,16L13,16Q13.4375,16,13.71875,16.28125Q14,16.5625,14,17Q14,17.4375,13.71875,17.71875Q13.4375,18,13,18L13,20Q13.4375,20,13.71875,20.28125Q14,20.5625,14,21L14,31Q14,31.4375,13.71875,31.71875Q13.4375,32,13,32L12,32L3,32ZM3,20L11,20L3,20L11,20L11,18L3,18Q2.5625,18,2.28125,18.28125Q2,18.5625,2,19Q2,19.4375,2.28125,19.71875Q2.5625,20,3,20ZM4,27.5Q4.03125,27.96875,4.5,28L10.5,28Q10.96875,27.96875,11,27.5Q10.96875,27.03125,10.5,27L4.5,27Q4.03125,27.03125,4,27.5ZM4.5,26L10.5,26L4.5,26L10.5,26Q10.96875,25.96875,11,25.5Q10.96875,25.03125,10.5,25L4.5,25Q4.03125,25.03125,4,25.5Q4.03125,25.96875,4.5,26Z"
                    fill="#16A34A" fill-opacity="1" style="mix-blend-mode:passthrough"
                    transform="matrix(1,0,0,-1,0,32)" />
                </svg>
              </div>
              <div class="text-4xl font-bold" style="color: #000000; font-family: 'Roboto', sans-serif;">
                {{ formatNumber(stats.Toxicity) }}
              </div>
            </div>
          </div>
          <div class="text-lg" style="color: #4B5563; font-family: 'Roboto', sans-serif;">
            Toxicity Experiment Records
          </div>
        </div>
      </div>

      <!-- 统计图表区域 -->
      <div class="mt-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 font-roboto">Statistical Analysis</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Fig.1 -->
          <div class="bg-white rounded-2xl shadow-lg p-6 border">
            <div class="w-full flex justify-center">
              <img 
                src="/src/assets/figs/fig1.png" 
                alt="Fig.1: Compound Distribution"
                class="w-full h-full object-contain rounded-lg"
              />
            </div>
          </div>

          <!-- Fig.2 -->
          <div class="bg-white rounded-2xl shadow-lg p-6 border">
            <div class="w-full flex justify-center">
              <img 
                src="/src/assets/figs/fig2.png" 
                alt="Fig.2: Toxicity Types Distribution"
                class="w-full h-full object-contain rounded-lg"
              />
            </div>
          </div>

          <!-- Fig.3 -->
          <div class="bg-white rounded-2xl shadow-lg p-6 border">
            <div class="w-full flex justify-center">
              <img 
                src="/src/assets/figs/fig3.png" 
                alt="Fig.3: Molecular Weight Distribution"
                class="w-full h-full object-contain rounded-lg"
              />
            </div>
          </div>

          <!-- Fig.4 -->
          <div class="bg-white rounded-2xl shadow-lg p-6 border">
            <div class="w-full flex justify-center">
              <img 
                src="/src/assets/figs/fig4.png" 
                alt="Fig.4: Toxic Mushroom Genera Distribution"
                class="w-full h-full object-contain rounded-lg"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ref, onMounted } from 'vue'
import * as api from '../api'

const stats = ref(null)
const loading = ref(false)
const error = ref(null)

const loadStatistics = async () => {
  try {
    loading.value = true
    error.value = null

    // 使用统一的API调用方式
    const response = await api.getStatistics()

    // API返回的数据在response.data中
    const data = response.data

    stats.value = {
      Compounds: data.Compounds || data.compounds || 678,
      Mushroom: data.Mushroom || data.mushroom || data.Fungus || data.fungus || 235,
      Toxicity: data.Toxicity || data.toxicity || 915
    }

  } catch (err) {
    console.error('Failed to load statistics:', err)
    // 根据axios的错误结构调整错误处理
    error.value = err.response?.data?.message || err.message || 'Unable to load statistics. Please check if the backend server is running.'

    // 使用默认值作为后备
    stats.value = {
      Compounds: 678,
      Mushroom: 235,
      Toxicity: 915
    }
  } finally {
    loading.value = false
  }
}

const formatNumber = (num) => {
  if (num === undefined || num === null) return '0'
  return num.toLocaleString()
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
/* 图表容器的响应式调整 */
@media (max-width: 768px) {
  .aspect-video {
    aspect-ratio: 4/3;
  }
}

/* 卡片悬停效果 */
.hover\:scale-\[1\.02\]:hover {
  transform: scale(1.02);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 加载动画 */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

/* 图片显示优化 */
img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
/* 图片显示优化 */
img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>