"""
图标
"""

import tkinter as tk


class Icons:
    """ 图标 """

    def __init__(self):
        """ 初始化 """
        self.titleIcon = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAcNJREFUeNrsVT9Lw0AUT0JHwZu7mG9gv4AYd8GO3ewiuNm5Q42uXeLkGr9Bv4Hn0KV0SCmCm3ET6pCQTYT4e/gOjmsuqZVuPni5y/tzv/fvErcsS2eX5Dk7pp0DtOjhum6AJfjLQSh1WCV3qQcAIOU1+GmLs33wAc5xbci0hD/b0vktN/m2bGFx2cINMyB7acglla2uyX3w8QYAqVFan/3S2hKBMvBEvRdFcT8ajW4hOwV3akpGmWS1JUK6FP0+AfB7BONLz/N0G4q6D3mqyVT0d033oAvO4RzDKcb+ioTtdvuZ9Td8UAK90PwGvEZWAHY4o+ix72A9Bz+QTgjxoc38CWcZGYEt9KzWesBRlHzxQt4L3Y51xAk1k3Vd1vWbxpTq/wal5FElw8ywebT45apvlSXiJh2aRiwniofD4cVqtVoQz+fzfDqdfs5msyNV1rVgjNQjXn2Wd/h9oqVNIyoBkEgpy+Vy+d7r9caqdGtjawBQcxJjrhWo5DoHmoyiFeyXVt4LA4B4YPneZJqNAvQZsNLPBiAsN1Ro0+Nr8rjOz5yiL/Armtr4AdJs9vjDlll/OKCXLf8FisbWQP5/+k30LcAA8GKmsnHde6EAAAAASUVORK5CYII='''
        )
        self.scanImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAfZJREFUeNqslr9PwkAUx6+XDjDRhEESBzvi1pmpbmya6GhiDQtx4j8g/BENG2LiH9DFhE3+hDLJ4NDFwYHknCAhFt+D1+Ys19JCX/Jyvfbd53vvcT/QNpsNy2OaplnQGNQVMM7PNRAF0hzM0XX9DcNUTt+cLIamygBma3POX8MwPK9UKqzZbDLTNJlh7BIQQrAgCNh8Pmer1YpB7BfE3gNrusdKCgDcgeYZwe12m1mWlVkB3/fZZDLZCoE9Am+cKoBwSNuFmeqdTue7Wq2Gecq8XC75aDQ6g8x+1+v1kywSC2BZoHkHn3W73c9Go3HLCthisfhwXZdBqS6hexWVi0sxqPoDbg+HwztoXwrwZ/V6vQXwFjHiDLhU9wvwHigLfNfv952cIjOcFMQLGttDFjF3JYKOh0HwbCRHDwYDnM3DIXhioWB/CrybqETX4J6KkJGJEk7mEZNx2qFo07QaKESy4DEL2Vza/kFWoSWRQ3CZtWXbtPXtrC1fxGUmZhDNxGTlWcQSXDoV7RIFbDpI/Sglj47gskqEVfHwmUvLqhZtjlOMGLV42UuqASkbJ8zcIEYQv1P88v4xIgT3kyty7wY7RiQB/3fDKa9JChSHrkMpXqjgSgGpXIEkNCaQTe7QuwgcpG3UPLPz0i59+lb80i/zb8ufAAMAWHWRBzMdNWwAAAAASUVORK5CYII='''
        )
        self.exportImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAWNJREFUeNpi/P//PwMMqEiKKQApBQbKwIM7z189gHEYQRYADRZgYWXd8uf3b2sGKgCgWUeBZvkALfrAAhUAG55XXMrAx8/H0FJXy1DT1Mygqa1DlIHXr16B6/n08RPDpN5ua5CZQCkbBmUJUQUg/j+xu+s/CJw4euQ/iA+i8QGQ/JoVy7HqAZkF4oPMZoKFubmVFUnBcPLYMYa1K1dglUMyC2wBTQHNLWAhV2NQeASDq6cn6Rbw8fODaVD4gsKZENi9fTvDk8ePUPTitQCUNDsnTGIoL8gjyUcgPdiSNdYgCgZ6H4SHdiSfPHaUJIPMrayJt6AsP5dh3aqVpKWqsHCGromTCVsAcjnI8GpguaJFZFl0DVgWtQLLIlC8ofsEZxCBDMfl7UEVyaMWEGXBA1j5Ti2AZNYDFlAFrSEnfRRUzUEKLD54NUgsgKkF0SDDgWaB6+Ubj54+oHmlz0jrZgtAgAEA7pPVPhTXuFcAAAAASUVORK5CYII='''
        )
        self.refreshImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAASRJREFUeNrUVsERgjAQJA5/KCEPC0gH4t+HJVCCJViCT5/agQX4oAQK8EEJsQK8cy4zBxySSJjRzKxAcrd7HpcLqm3bZMmxShYe6ZSBUkrDZQ8oADlNW0AFuEEGGmaLNg2fSzBFEmBoImkJjrSiezePz5p88OfY4RkhLxnJBWAEG0NrTrz0EmCGtUQ8IlSzfzQuQGmx5JB7kBeEHeBBAqdPAi7nk5GznPdx5jZpr1o2gCss1J5VuO09rwH3zgyL5hASvS/4RsNcPgOiD97JOb3c324V8C4rhCRgqabnDkNcAwFUzUDdzIgefTPiGlSRdq3h24phrUNH2WhCy3g3v2itgvm5CrQ8+iWaXTlYj9muRa6YB44ENXXohxyZov/ff1W8BBgABNaQeonnS/4AAAAASUVORK5CYII='''
        )
        self.openImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAASJJREFUeNrsVcERgjAQJAxPZ7QD6MASpAMtgRLsQP5+LIESKAE7wJ8/U0L8OxP3xsTJYBJIlJ83cxwEcrfZvRAmpUzmtDSZ2WYvkNGFMVYilN8kAtW1bZyRBihALw/wc0TuAp4jD3NVplC/bmUS6mNzMxcsRVs9cQX0fTcY74g2n8gVfDOhAB9QW6h53EsRTMDbCMpoJUI/pw56CP2SCoSojXkafTO2D3bwOxA0gR21V/HkLAAUK4RtKHoD2AXAuG8FlYpNID2UPDfRW0WG9dQBEeK2qjFW5nhqEWkdIe6bViQVvp/dh0gTzU2rSZHaHH0EPdxF63AFeYS4pVVcTxc1P6NHnweGPeA3oAopsFA/NuErcI08C7QdnRT+D/0xewowAGDZK3ctMBXjAAAAAElFTkSuQmCC'''
        )
        self.BImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAPFJREFUeNpiVJYQFWBgYDBgoA24wAI1fD+NLHBkgbGqm5oZtLR1qGLqtatXGFrrasFsuAUgw82trKnuBSYGGoNRCyi3ICwsjIGRkREFm5iYMMyaNYu6Pnj37h3D////wVhQUJAhPT2dYfXq1bQJovLycjB99uxZ2sYByCdUt+DevXsMnZ2dDEpKSgxpaWkE1bMQa7CQkBCKy0HBRFUfIEeyi4sLQ0VFBRjTJA5WrVoFDiJikirNI5mFHINBQQOK7JkzZ1LPB6BIhuVkUPoHGU6VVAQK70Fd2LEgV3PUAshmMQJbFQ60rvQvgBi0arYABBgApmlMDVbwwacAAAAASUVORK5CYII='''
        )
        self.KBImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAWVJREFUeNrsVlFKhUAUvYYLSOFB3/ZXfQQKQf0U6BJ0CboEhaiPHoEuQZegS1BoBcL7qP50Cy7BOpeMSXyPMZR+ujDM4My9Z+49Z5xRTk82x0R0SevYTv0K/rISwJ06jO6ftnR2frFI1Pe3V3p+fODxNwCCX13fLJ7CEa1s/wDzAeq6JkVRKIqiH98tyyJd13kePdaIzXEcnvtVBkEQsHOapmSaJn9D3/c9t6ZpqOs6BkE/C6AoCsqyjOI4Jtd1J9cYhsFzCF5VlTwAHFAq3/cpDEOpmmuaJg/geR7vDqWRydK2bW6iqfuc4IAMyrKcnB/EMBg4QabSJGMxnFCiMXFTJKM0yBjZSJcoz3Nq25YdD5lYxlkAgyOUAakuTjIM8oNEwUmSJHvVhg0g+FhtUgcNTlAH+ACQSDIaTjayhSDQH1TRQN7YRDVNqeXPfnaqeM0tZWIs5fNVcbv2pb/DYK1ny4cAAwASaZl4SoCW8AAAAABJRU5ErkJggg=='''
        )
        self.MBImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAWlJREFUeNrsVkFKhVAUvYYLSCFobLNqEDgIalKgS9Al6BIUoj8oGrgEXYIuQaEVCH9QzXQLLsE6l+7Hb+rv8xUadODxHvfdd8899/pU5ez05JiIrmgZrNXv4K8LEdyrsnp4eqbzi8tZon68v9HL6pHXGwIEv765nV3CES2Mf4L9CcIwJEVReO7Ctm22R1FEuq7zujuwX5blboK6rknTNMqybMtWFAXbm6Zhm2ma1LYtj6qq2A4S2Z8skWVZPCMoADLHcZhgCIZh8D6Cy5lRAskAB0RFkiTkeR4TQM0U+kkMEsBJCCQjUTUE+CEJ+PT91LEsUGNIR7ORfV8hGormCuDf9ZtssgAqEAhzn6DfZCTluu7Ww7HzHgRBwAGgRJo51uQ4jjflOuiiHdRkyJcm7wOc8X2fz0H1JMFvIU3GwM1GmfI8/1FGtV9L1HwMaZr+vZed2v3MzYVuLOXrr+Ju6Y/+Goulfls+BRgAHXykeSCfXGkAAAAASUVORK5CYII='''
        )
        self.GBImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAYpJREFUeNrsVsFKhFAUvQ5+QDMQtJ521SIYIahNgX6CfoJ+gkLUogj0E5xP0E+YRZuCFgqzqHa6LQicT3i98+iJTinOpNCiCxcfT985951zn6rs7+3uENExDRNL9Qv8fiCCC1WOLm9u6eDwqBfU15dnuru+EuOSAOAnp2e9b2FEA8c/wfYEcRyTZVmkKEqZnueJe5PJpDaPNAyD0jTtRhAEgQBHFEVBjDGR8h5iNpuV81mW0Wq1EiS41oKf5HOe7OnxgSGSJAESs22bNcV4PGacoDbn+75YF0WRwAImsEc/VY9wXXcrzTl5u0TQcTqdiuwa8Gs+n5Ou6yJbCaBhtQoYWzVT7hCFyDn4hTVc1s3blGsrjOTe1ObXTQYBiLCbVgIszPN8I90hZxiGpVytBNAQMkkpfmuyuv4Augf6ykPVpZtQkOM4AhzPf7y/tXvAe1loj+1KIzVNI9M0yy6pmoyTDZkWi8W37lObqkIlTdXjdP+Zl51a/cz1FVUsBe+LoT/6SwyG+m35FGAADijR/xh9Vf8AAAAASUVORK5CYII='''
        )
        self.ignoreCaseImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAXVJREFUeNrslsFKhEAcxv+KD5BC0Flv1SFQCOpS4D6CPoI+gkJshyLQR9BX8BEUuhR0EfZQHX0FH8H2GxoZbNpdaObWB4P/1Z3f5/+bYWcN7+T4iIguSI821jf8WZPBrcWru4dHOj07V0L9/Hinp/s1q2cDwC+vrpW3YJJm/Rv8zSDPczIMgxzHoXEc1Rs0TUNJkjA4aqUGXdfRMAyUZRm5rvvDoK5rWq1WrEOMIAjYvYMNAAQYA130fT/HhBrPi6KgaZrYsG2b0jRlzw42ABjyfZ/B+Rvic9u27MqFTnnnew0AB5ADwjBknSwni0IH0HIzmLviAZgLNV8XqCxLtrvENZDJWt7AGwCEKybKzGGCuKqqmmNE9jIT87d4kDFfQHEhYY7vID4Ol0Wz0wAgMR6uKIqYAeDoQowrjuP9BpgAAEAyiYuO2vM8FiPmYMtKtT0yb7Zjent9mVQJLDDB1v5jZ4nHnCqJLANt6D70Nyh0/W35EmAAUVYI2Y3rsN0AAAAASUVORK5CYII='''
        )
        self.notIgnoreCaseImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAblJREFUeNrsVrFqAkEQnQtbaBeFQEgghdclKQIWgaRJQD/AQmsr/QSFkCAJAf0Ff8HCVlCIQg5SKFjkrlPExtJSC2Gzb8guF1QS8a7Lg+Fmb3ffu5md3T3LPj46JKIrCgdD8U3+FpLAvdDew/MLnV9cBsLquZ/0+vTIvhEA+fXNbeAhHFDI+BfYT6BcLpNlWRSPx2k+nwcv0Gg0qFAoMDn8QAU6nQ6Nx2MqlUqUSCTWBGq1Gtm2zRHC0uk0DQaDvwuAEMQwRIHJOk0gh3i/3ycpJY1GI27ncrl1InUW3SmTH8679CMWi8lqtcp+u92WaqhpbwL6MEaJMhc4wS38Yt1ul83zPP5a13WpUqlwnxKker1Oi8ViY8SO4/ATkZydnpj3PwQmk4kRiEQiNJ1O2QC0MbnVapEQgv3ZbLbbIufzeWo2m7RarWi5XFKv1zOmyTKZDPdFo1GzBjCVor9VERYX6VF5N5O1IU2oLix4NpulZDK5e5lCAESpVGptMEghoIU0isUib8pfBZBXTATRJugvxt5AlHoPwN+Woq1lug/8ZRr6YSf811xQ8HNZCCPsS38IJ6zfli8BBgBLUF5+Jho7RQAAAABJRU5ErkJggg=='''
        )
        self.reImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAASpJREFUeNpiVJYQFWBgYDBgoA24wAI1fD+NLHBkgbGqm5oZtLR1qGLqtatXGFrrasFsuAUgw82trKnuBSYGGoNRC8izwMTEhIGRkREFp6enM7x//x4sv3r1agx5GAbJEeUDY2Njhv///4PxqlWrwBpdXV1R1HR0dMDVwHBoaCjpQQTSBMJnz55luHfv3hCM5FmzZoFxWloag5KSEnUsAAUHLOI6OzvB4T1z5kwUNRUVFRiRDNJHUiSfOXMGnHr27NmDoQZbJIP0kRREIA2goAFZAPIJTeKgvLycQVBQEBwPNLEAZDjIF6Akip6RqJZMYb5ADiZskYzuABZshoEiFpsv3r17B+eDIhQXOHnsKP0yGgtyNUctgGwWI7BV4UDrSv8CiEGrZgtAgAEAI1KGBIfso8gAAAAASUVORK5CYII='''
        )
        self.notReImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAYtJREFUeNpiVJYQFWBgYDBgoA24wAI1fD+NLHBkgbGqm5oZtLR1qGLqtatXGFrrasFsuAUgw82trKnuBSYGGoNRC8izwMTEhIGRkREFp6enM7x//x4sv3r1agx5GAbJEeUDY2Njhv///4PxqlWrwBpdXV1R1HR0dMDVwHBoaCjpQQTSBMJnz55luHfv3hCM5FmzZoFxWloag5KSEkkWsCBzHjx4wLBgwQKGZ8+eMTx//hwcaSAgKCjI4OLiwiApKcnQ0NDAcO3aNbB4RUUFGCODM2fO4Lbgw4cPDAcOHGD48uULAy8vL4ORkRHD58+fGS5dugQO/9+/f4PVvX79GkyDfCMrK4uROE4eO4oQABbXDkD8/8TRI/9hAKgIjGGgvLz8P1Dpf2CqAfOBqQqFjw5AZoHMBJlNVBwALQAHEygeaBLJIMNBEQxKougZiWrJFOaLzs5OuBgoggnlZBZshqGnBJgv3r17B+eDci0ugBzJNM9oLMjVHLUAslmMoKRE60r/AohBq2YLQIABALWXzB5FczH6AAAAAElFTkSuQmCC'''
        )
        self.searchImage = tk.PhotoImage(
            data='''iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAABCcAAAQnAEmzTo0AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAVRJREFUeNpi/P//PwMtAQu5GlUkxRxg7DvPXx3ApY6RFB8ADRUAUhNYWFlD//z+zQV3JSvrNyB/NZBZALTsA1kWAA03YGZmPvz3718eFw8PBlcPLwYZWVmGJ48fM+zesY1hz44dDED5L0B5W6AlF+AaQRYQwsoSogJq0hKf9VWV/p04euQ/NgASB8mD1IHUw/QSa8ECIP6Py3BkS0DqQOpJskBdVuprekLsf2IASB1IPUwvEzGpBRShoDAnBoDUgdTDUhkTsSkIFKHkqCPaAlBqIUcdQQtAmQiUzkFJkRgAUgdSD898pKSilUsW0yYVATUsA2kERhxOS3DlA4I5GWjoAiAVjyxGSk7GawEWw5cD8S+qlEVYDF8I1JxAldKUkOGkACZaGo5hAbUNR7GAFobDLQAaXkALw5F9AHL9RWobjlJUgHIfEBcQk7NJwYy0brYABBgAK29DZvg8pMMAAAAASUVORK5CYII='''
        )
